# -*- coding: utf-8 -*-
import os
import sys
import sqlalchemy as db
import subprocess

from pyramid.paster import get_appsettings, setup_logging
from ..models import City, Station, Node, Portal, TrainStop, Line, TrainLine, Obstacle, OBSTACLE_TYPE  
from pyramid.scripts.common import parse_vars
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


class UploadError(Exception):
    pass


def delete_tables(engine, schema, tables):
    sql = 'DROP TABLE IF EXISTS %s' % (
        ','.join(['.'.join([schema, t]) for t in tables]))
    engine.execute(sql)


def get_translation(obj, langs):
    translation = dict()
    for lang in langs:
        lang_attr = 'name_%s' % lang
        if hasattr(obj, lang_attr):
            translation[lang_attr] = getattr(obj, lang_attr)
    return translation

def get_geom_real_point(obj):
    geom_real = 'POINT(%s %s)' % (
        obj.lon,
        obj.lat
    ) if (
        obj.lon is not None and
        obj.lat is not None
    ) else None
    return geom_real


def main(argv=sys.argv):
    config_uri = argv[-1]
    options = parse_vars(argv[1:-1])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    dataset_files = settings['dataset_files'].split()
    langs = settings['langs'].split(',')
    dataset_city = settings['city']
    storage_path = settings['path']
    storage_files = os.listdir(storage_path)

    db_settings = (
        settings['db.user'],
        settings['db.password'],
        settings['db.host'],
        settings['db.name'])

    assert set(dataset_files).issubset(set(storage_files)), 'Incomplete dataset'

    pg_string = 'PG:user=%s password=%s host=%s dbname=%s' % db_settings
    sa_url = 'postgresql+psycopg2://%s:%s@%s/%s' % db_settings
    engine = db.create_engine(sa_url)

    # create temporary tables
    temp_schema = 'temporary'
    temp_tables = []
    for dataset_file in dataset_files:
        try:
            table = '%s_%s' % (dataset_city, dataset_file.split('.')[0])
            cmd = [
                'ogr2ogr', '-lco', 'SCHEMA=%s' % temp_schema, '-lco', 'OVERWRITE=YES',
                '-f', 'PostgreSQL', pg_string, os.path.join(storage_path, dataset_file), '-nln',
                table
            ]
            subprocess.check_call(cmd)
            temp_tables.append(table)

        except subprocess.CalledProcessError:
            if temp_tables:
                delete_tables(
                    engine,
                    schema=temp_schema,
                    tables=temp_tables)

            raise UploadError('Error of temporary tables creation')

    Session = sessionmaker(bind=engine)
    session = Session()

    sql = 'select * from %s.%s_%s'

    # obstacles
    for otype in OBSTACLE_TYPE:
        tablename = '%ss' % otype if otype not in ['stairs', 'rails_stairs'] else otype
        obstacles = engine.execute(sql % (temp_schema, dataset_city, tablename))
        for o in obstacles:
            obstacle = Obstacle(
                obstacle_type=otype,
                geom_local=o.wkb_geometry,
                oneway=db.sql.cast(o.oneway, db.Boolean)
            )

            if otype in ['door', 'turnstile', 'escalator', 
                         'elevator', 'ramp', 'wheelchair_platform']:
                obstacle.min_width = 0
                obstacle.max_width = o.width

            if otype in ['rails_stairs']:
                obstacle.min_width=o.min_width
                obstacle.max_width=o.max_width

            if otype in ['elevator', 'wheelchair_platform']:
                obstacle.closed = db.sql.cast(o.outoforder, db.Boolean)

            if otype in ['passage', 'wheelchair_platform']:
                obstacle.length = o.length

            if otype in ['elevator']:
                obstacle.cab_width = o.cab_width
                obstacle.cab_length = o.cab_length

            if otype in ['stairs', 'rails_stairs']:
                obstacle.steps = o.steps

            if otype in ['stairs', 'rails_stairs', 'ramp']:
                obstacle.railing_exist = db.sql.cast(o.railing, db.Boolean)
                if otype != 'ramp':
                    obstacle.railing_count = o.railing

            if otype in ['ramp', 'rails_stairs']:
                obstacle.slope = o.slope

            session.add(obstacle)

    # cities
    cities = engine.execute(sql % (temp_schema, dataset_city, 'cities'))
    city = cities.fetchone()
    cityobj = City(translation=get_translation(city, langs))
    session.add(cityobj)

    # station
    stations = engine.execute(sql % (temp_schema, dataset_city, 'stations'))
    station_idx = dict()
    for s in stations:
        station = Station(
            osm_id=s.osm_id,
            geom_local=s.wkb_geometry,
            geom_real=get_geom_real_point(s),
            translation=get_translation(s, langs))
        station.city = cityobj

        if s.id is not None:
            idx = str(s.id)
            if idx in station_idx.keys():
                raise UploadError('Found stations with the same id')
            station_idx[idx] = station
        
        session.add(station)

    # portal
    portals = engine.execute(sql % (temp_schema, dataset_city, 'portals'))
    for p in portals:
        portal = Portal(
            direction=p.direction,
            closed = db.sql.cast(p.closed, db.Boolean),
            geom_local=p.wkb_geometry,
            geom_real=get_geom_real_point(p),
            translation=get_translation(p, langs)
        )

        # station_portal
        for station_col in ['id_st_%s' % id for id in range(1,4)]:
            if hasattr(p, station_col):
                id = getattr(p, station_col)
                if id is not None:
                    idx = str(id)
                try:
                    station = station_idx[idx]
                except KeyError:
                    UploadError('Portal refers to non existed station')

                portal.stations.append(station)

        session.add(portal)

    # nodes
    nodes = engine.execute(sql % (temp_schema, dataset_city, 'nodes'))
    for n in nodes:
        node = Node(geom_local=n.wkb_geometry)
        session.add(node)
  
    # train_stops
    train_stops = engine.execute(sql % (temp_schema, dataset_city, 'train_stops'))
    for ts in train_stops:
        train_stop = TrainStop(
            osm_id=ts.osm_id,
            geom_local=ts.wkb_geometry,
            geom_real=get_geom_real_point(ts))

        if ts.id_station is not None:
            idx = str(ts.id_station)
        try:
            station = station_idx[idx]
        except KeyError:
            UploadError('Train stop refers to non existed station')
        train_stop.station = station
        session.add(train_stop)

    ## lines
    line_idx = dict()
    lines = engine.execute(sql % (temp_schema, dataset_city, 'lines'))
    for l in lines:
        line = Line(
            color=l.color,
            translation=get_translation(l, langs))
        session.add(line)
    #     # TODO: Создать индекс линий

    ## train_lines
    train_lines = engine.execute(sql % (temp_schema, dataset_city, 'train_lines'))
    for tl in train_lines:
        train_line = TrainLine(
            oneway=db.sql.cast(tl.oneway, db.Boolean),
            time=tl.time,
            geom_local=tl.wkb_geometry)
        # TODO: Привязать перегон к линии
        session.add(train_line)

    # update node_id for stations and obstacles
    session.flush()
    upd = Station.__table__.update().values(node_id=Node.__table__.c.id).\
        where(db.func.st_within(Station.__table__.c.geom_local, Node.__table__.c.geom_local))
    session.execute(upd)

    upd = Obstacle.__table__.update().values(node_id=Node.__table__.c.id).\
        where(db.func.st_within(Obstacle.__table__.c.geom_local, Node.__table__.c.geom_local))
    session.execute(upd)

    session.commit()

    # delete_tables(engine, schema=temp_schema, tables=temp_tables)
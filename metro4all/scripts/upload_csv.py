# -*- coding: utf-8 -*-
import csv
import json
import os
import sys
import sqlalchemy as db

from pyramid.paster import get_appsettings
from ..models import City, Station, Node 
from pyramid.scripts.common import parse_vars
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

# upload_csv stations=/home/rykov/git/metro4all/data development.ini
def main(argv=sys.argv):
    config_uri = argv[-1]
    options = parse_vars(argv[1:-1])
    settings = get_appsettings(config_uri, options=options)

    db_settings = (
        settings['db.user'],
        settings['db.password'],
        settings['db.host'],
        settings['db.name'])

    pg_string = 'PG:user=%s password=%s host=%s dbname=%s' % db_settings
    sa_url = 'postgresql+psycopg2://%s:%s@%s/%s' % db_settings
    engine = db.create_engine(sa_url)

    Session = sessionmaker(bind=engine)
    session = Session()

    cities_path = settings.get('cities')
    if cities_path is not None:
        with open(cities_path) as cities_file:
            cities = json.load(cities_file)
            for c in cities.get('packages'):
                old_keyname = c.get('path')
                translation = dict()
                for fld in c:
                    if fld.startswith('name'):
                        translation[fld] = c.get(fld)
                city = City(translation=translation, old_keyname=old_keyname)
                session.add(city)

        session.flush()
        session.commit()

    spath = settings.get('stations')
    query = session.query(City)
    for q in query:
        city = q.old_keyname
        city_obj = session.query(City).filter_by(old_keyname=city).one()
        if city in os.listdir(spath):
            csv_path = os.path.join(spath, city, "stations.csv")
            if (os.path.isfile(csv_path)):
                stations_csv = csv.DictReader(open(csv_path), delimiter=";")
                for row in stations_csv:
                    id_station = row.get("id_station")
                    id_node = row.get("id_node")
                    try:
                        station = session.query(Station).filter_by(
                            old_city_keyname=city,
                            old_id=id_station
                        ).one()
                    except NoResultFound:
                        try:
                            node = session.query(Node).filter_by(
                                old_city_keyname=city,
                                old_id=id_node
                            ).one()
                        except NoResultFound:
                            node = Node(
                                old_id=id_node,
                                old_city_keyname=city
                            )
                            session.add(node)
                            session.flush()

                        translation = {key: row[key] for key in row if key.startswith("name")}
                        station = Station(
                            old_id=id_station,
                            old_city_keyname=city,
                            city_id=city_obj.id,
                            node_id=node.id,
                            translation=translation
                        )
                        session.add(station)
                        session.flush()
        session.commit()
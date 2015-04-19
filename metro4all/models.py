from sqlalchemy import (
    Column,
    Index,
    Integer,
    BigInteger,
    Unicode,
    Enum,
    Boolean,
    ForeignKey,
    Table,
    )

from sqlalchemy.dialects.postgresql import HSTORE

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.ext.mutable import MutableDict

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relation
    )

from geoalchemy2 import Geometry

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

PORTAL_DIRECTION = ('in', 'out', 'both')
TRANSPORT_TYPE = ('subway', 'railway', 'tramway')
OBSTACLE_TYPE = ('passage', 'door', 'turnstile',
                 'ramp', 'rails_stairs', 'stairs',
                 'escalator', 'elevator', 'wheelchair_platform')

station_portal = Table('station_portal', Base.metadata,
    Column('station_id', Integer, ForeignKey('station.id')),
    Column('portal_id', Integer, ForeignKey('portal.id'))
)

class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    translation = Column(MutableDict.as_mutable(HSTORE))

    stations = relation('Station', backref='city')


class Station(Base):
    __tablename__ = 'station'

    id = Column(Integer, primary_key=True)
    osm_id = Column(BigInteger)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    node_id = Column(Integer, ForeignKey('node.id'))
    geom_real = Column(Geometry('POINT'))
    geom_local = Column(Geometry('POINT'))
    translation = Column(MutableDict.as_mutable(HSTORE))

    portals = relation('Portal', secondary=station_portal, backref='stations')
    train_stops = relation('TrainStop', backref='station')


class Node(Base):
    __tablename__ = 'node'

    id = Column(Integer, primary_key=True)
    geom_local = Column(Geometry('POLYGON'))

    stations = relation('Station', backref='node')
    obstacles = relation('Obstacle', backref='node')


class Portal(Base):
    __tablename__ = 'portal'

    id = Column(Integer, primary_key=True)
    osm_id = Column(BigInteger)
    direction = Column(Enum(*PORTAL_DIRECTION, native_enum=False), nullable=False, default='both')
    closed = Column(Boolean)
    geom_real = Column(Geometry('POINT'))
    geom_local = Column(Geometry('POINT'))
    translation = Column(MutableDict.as_mutable(HSTORE))


class TrainStop(Base):
    __tablename__ = 'train_stop'

    id = Column(Integer, primary_key=True)
    osm_id = Column(BigInteger)
    geom_real = Column(Geometry('POINT'))
    geom_local = Column(Geometry('POINT'))
    station_id = Column(Integer, ForeignKey('station.id'), nullable=False)


class Line(Base):
    __tablename__ = 'line'

    id = Column(Integer, primary_key=True)
    color = Column(Unicode(6))
    transport_type = Column(Enum(*TRANSPORT_TYPE, native_enum=False), default='subway')
    translation = Column(MutableDict.as_mutable(HSTORE))

    train_lines = relation('TrainLine', backref='line')


class TrainLine(Base):
    __tablename__ = 'train_line'

    id = Column(Integer, primary_key=True)
    osm_id = Column(BigInteger)
    geom_real = Column(Geometry('LINESTRING'))
    geom_local = Column(Geometry('LINESTRING'))
    time = Column(Integer)
    oneway = Column(Boolean)
    line_id = Column(Integer, ForeignKey('line.id')) #nullable
    train_stop_from_id = Column(Integer, ForeignKey('train_stop.id')) #nullable
    train_stop_to_id = Column(Integer, ForeignKey('train_stop.id')) #nullable


class Obstacle(Base):
    __tablename__ = 'obstacle'

    id = Column(Integer, primary_key=True)
    node_id = Column(Integer, ForeignKey('node.id'))
    obstacle_type = Column(Enum(*OBSTACLE_TYPE, native_enum=False))
    oneway = Column(Boolean)
    geom_local = Column(Geometry('LINESTRING'))
    min_width = Column(Integer)
    max_width = Column(Integer)
    length = Column(Integer)
    cab_width = Column(Integer)
    cab_length = Column(Integer)
    closed = Column(Boolean, default=False)
    slope = Column(Integer)
    steps = Column(Integer)
    railing_count = Column(Integer)   
    railing_exist = Column(Boolean)
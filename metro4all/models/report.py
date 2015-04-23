# -*- coding: utf-8 -*-
import datetime 

from .main import Base, Node
from ..utils import JsonifyMixin

from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import Column, Integer, Unicode, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class ReportCategory(Base):
    __tablename__ = 'report_category'

    id = Column(Integer, primary_key=True)
    translation = Column(MutableDict.as_mutable(HSTORE))


class ReportPhoto(Base, JsonifyMixin):
    __tablename__ = 'report_photo'

    id = Column(Integer, primary_key=True)
    photo = Column(Unicode(32), nullable=False)
    report = Column(ForeignKey('report.id'), nullable=False)


class Report(Base, JsonifyMixin):
    __tablename__ = 'report'

    id = Column(Integer, primary_key=True)
    device_lang = Column(Unicode(2), nullable=False)
    data_lang = Column(Unicode(2), nullable=False)
    schema_x = Column(Integer, nullable=True)
    schema_y = Column(Integer, nullable=True)
    report_on = Column(DateTime(timezone=False))
    receive_on = Column(DateTime(timezone=False), default=datetime.datetime.now)
    package_version = Column(Integer, nullable=False)
    message = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=True)
    preview = Column(Unicode(32), nullable=True)
    fixed = Column(Boolean, default=False)
    city = Column(Unicode(4), nullable=False)

    node_id = Column(ForeignKey('node.id'), nullable=True)
    node = relationship(Node)
    category = Column(ForeignKey('report_category.id'), nullable=False)
    photos = relationship(ReportPhoto, cascade="all, delete-orphan")

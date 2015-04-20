# -*- coding: utf-8 -*-

from .main import Base

from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import Column, Integer, Unicode, DateTime, ForeignKey, Boolean

class ReportCategory(Base):
    __tablename__ = 'report_category'

    id = Column(Integer, primary_key=True)
    display_name = Column(MutableDict.as_mutable(HSTORE))


class ReportPhoto(Base):
    __tablename__ = 'report_photo'

    id = Column(Integer, primary_key=True)
    report = Column(ForeignKey('report.id'), nullable=False)
    photo = Column(Unicode(32), nullable=False)


class Report(Base):
    __tablename__ = 'report'

    id = Column(Integer, primary_key=True)
    device_lang = Column(Unicode(2), nullable=False)
    data_lang = Column(Unicode(2), nullable=False)
    schema_x = Column(Integer, nullable=True)
    schema_y = Column(Integer, nullable=True)
    report_on = Column(DateTime(timezone=False))
    package_version = Column(Integer, nullable=False)
    message = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=True)
    preview = Column(Unicode(32), nullable=True)
    fixed = Column(Boolean, default=False)

    category = Column(ForeignKey('report_category.id'), nullable=False)
    city = Column(Unicode(4), nullable=False)
    node = Column(Integer, nullable=True)
# -*- coding: utf-8 -*-
from datetime import datetime
from collections import OrderedDict
import base64
import json
import os
import uuid

from pyramid.response import Response
from pyramid.view import view_config

from .models import (
    DBSession,
    City,
    ReportCategory,
    Report,
    ReportPhoto,
    Node
    )

from sqlalchemy.orm import joinedload


@view_config(route_name='home', renderer='home.mako')
def home(request):
    return {'one': '1', 'project': 'metro4all'}


@view_config(route_name='reports', renderer='reports.mako', request_method='GET')
def reports(request):
    session = DBSession()
    return {
        'cities': session.query(City).order_by(City.translation['name_ru']),
        'categories': session.query(ReportCategory).order_by(ReportCategory.translation['name_ru'])
    }


@view_config(route_name='reports_list', renderer='json')
def reports_list(request):
    session = DBSession()

    start_index = int(request.GET['jtStartIndex'])
    page_size = int(request.GET['jtPageSize'])
    sorting = request.GET['jtSorting']

    reports_count = session.query(Report).count()

    reports_from_db = session.query(Report, ReportCategory.translation['name_ru'], City.translation['name_ru'])\
        .options(joinedload('photos'))\
        .options(joinedload('node'))\
        .options(joinedload('node.stations'))\
        .join(ReportCategory, Report.category == ReportCategory.id)\
        .join(City, Report.city == City.old_keyname)\
        .slice(start_index, page_size) \
        .all()

    result = []
    for report_entity in reports_from_db:
        report = report_entity[0]
        result_entity = report.as_json_dict()
        result_entity['photos'] = [photo.as_json_dict() for photo in report.photos]
        result_entity['category_name'] = report_entity[1]
        result_entity['city_name'] = report_entity[2]
        result_entity['node_name'] = '/'.join([station.translation['name_ru'] for station in report.node.stations])
        result_entity['report_on'] = report.report_on.strftime('%Y/%m/%d %H:%M')
        result.append(result_entity)

    return {
        'Result': 'OK',
        'Records': result,
        'TotalRecordCount': reports_count
    }


def upload(path, base64str):
    id = str(uuid.uuid4().hex)
    full_path = os.path.join(path, "%s.jpg" % id)
    
    with open(full_path, 'wb') as img:
        img.write(base64.b64decode(base64str))
    
    return id


@view_config(route_name='reports', request_method='POST')
def create_report(request):
    
    body = request.json_body

    device_lang = body.get("lang_device")
    data_lang = body.get("lang_data")
    schema_x = body.get("coord_x")
    schema_y = body.get("coord_y")
    report_on = datetime.fromtimestamp(body.get("time")/1000.0)
    package_version = body.get("package_version")
    message = body.get("text")
    email = body.get("email")
    category = body.get("cat_id")
    city = body.get("city_name")
    node_old_id = body.get("id_node")
    screenshot = body.get("screenshot")
    photos = body.get("photos")

    node = DBSession.query(Node)\
        .filter(Node.old_id == node_old_id)\
        .filter(Node.old_city_keyname == city)\
        .one()

    report = Report(**OrderedDict((
        ("device_lang", device_lang),
        ("data_lang", data_lang),
        ("schema_x", schema_x),
        ("schema_y", schema_y),
        ("report_on", report_on),
        ("package_version", package_version),
        ("message", message),
        ("email", email),
        ("category", category),
        ("city", city),
        ("node", node),
    )))

    path = request.registry.settings.get("upload_path")
    if screenshot is not None:
        spath = upload(path, screenshot)
        report.preview = spath

    DBSession.add(report)
    DBSession.flush()

    if photos is not None:
        for photo in photos:
            ppath = upload(path, photo)
            report_photo = ReportPhoto(report=report.id, photo=ppath)
            DBSession.add(report_photo)

    DBSession.commit()

    return Response(
        json.dumps(dict(id=report.id)),
        content_type=b'application/json')
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
    ReportPhoto
    )


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
    return {
        'Result': 'OK',
        'Records': [
            {'Id': 1, 'City': 'Benjamin Button', 'Station': 17, 'Text': 'fadgdsfgsdfg sfsdasdf wfsdfsadfasdfs fsadfsadfasfasda ewfwqefsadfasdfasdfsdf qwefsdfsadfsadasdafsdafs', 'Category': 'Good', 'CreatedDate': '\/Date(1320259705710)\/'},
            {'Id': 2, 'City': 'Douglas Adams', 'Station': 42, 'Text': '\/Date(1320259705710)\/', 'Category': 'Good', 'CreatedDate': '\/Date(1320259705710)\/'},
            {'Id': 3, 'City': 'Isaac Asimov', 'Station': 26, 'Text': '\/Date(1320259705710)\/', 'Category': 'Good', 'CreatedDate': '\/Date(1320259705710)\/'},
            {'Id': 4, 'City': 'Thomas More', 'Station': 65, 'Text': '\/Date(1320259705710)\/', 'Category': 'Good', 'CreatedDate': '\/Date(1320259705710)\/'}
        ],
        'TotalRecordCount': 100
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
    node = body.get("id_node")
    screenshot = body.get("screenshot")
    photos = body.get("photos")

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
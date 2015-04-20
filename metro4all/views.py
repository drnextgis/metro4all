# -*- coding: utf-8 -*-
from datetime import datetime
from collections import OrderedDict

from pyramid.response import Response
from pyramid.view import view_config

import transaction


from .models import (
    DBSession,
    Report
    )


@view_config(route_name='home', renderer='home.mako')
def home(request):
    return {'one': '1', 'project': 'metro4all'}


@view_config(route_name='reports', renderer='reports.mako', request_method='GET')
def reports(request):
    return {
        'one': '1', 'project': 'metro4all'
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

@view_config(route_name='create_report', request_method='POST')
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

    with transaction.manager:
        DBSession.add(report)

    return Response('OK')


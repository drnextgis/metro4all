# -*- coding: utf-8 -*-
from datetime import datetime
from collections import OrderedDict
import base64
import json
import os
import uuid

from pyramid.response import Response

from pyramid.view import (
    view_config,
    forbidden_view_config,
    HTTPFound
)

from pyramid.security import (
    remember, forget
)

from pyramid.security import authenticated_userid

from .security import USERS

from .models import (
    DBSession,
    City,
    ReportCategory,
    Report,
    ReportPhoto,
    Node
)

from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload


@view_config(route_name='home', renderer='home.mako')
def home(request):
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

    sorting = request.GET['jtSorting'].split()
    order_direction = 'desc' if sorting[1] == 'DESC' else 'asc'
    column_sorted = getattr(map_report_fields(sorting[0]), order_direction)()

    reports_count = session.query(Report).count()

    query = session.query(Report, ReportCategory.translation['name_ru'], City.translation['name_ru']) \
        .options(joinedload('photos')) \
        .options(joinedload('node')) \
        .options(joinedload('node.stations')) \
        .join(ReportCategory, Report.category == ReportCategory.id) \
        .join(City, Report.city == City.old_keyname)

    clauses = _build_filter(request)
    if clauses:
        query = query.filter(or_(*clauses))

    query = query.order_by(column_sorted).slice(start_index, start_index + page_size)

    reports_from_db = query.all()

    result = []
    for report_entity in reports_from_db:
        report = report_entity[0]
        result_entity = report.as_json_dict()
        result_entity['photos'] = [photo.as_json_dict() for photo in report.photos]
        result_entity['category_name'] = report_entity[1]
        result_entity['city_name'] = report_entity[2]

        if report.node:
            station_names = []
            for station in report.node.stations:
                if 'name_ru' in station.translation:
                    station_names.append(station.translation['name_ru'])
                elif 'name_en' in station.translation:
                    station_names.append(station.translation['name_en'])
            result_entity['node_name'] = '/'.join(station_names)

        result_entity['report_on'] = report.report_on.strftime('%Y/%m/%d %H:%M')
        result.append(result_entity)

    return {
        'Result': 'OK',
        'Records': result,
        'TotalRecordCount': reports_count
    }


def _build_filter(request):
    clauses = []

    for parameter in request.POST:
        value = request.POST[parameter]
        if value:
            item_clause = [map_report_fields(parameter) == value]
            clauses.append(and_(*item_clause).self_group())

    return clauses


def map_report_fields(view_field):
    return {
        'id': Report.id,
        'city_name': City.translation['name_ru'],
        'report_on': Report.report_on,
        'category_name': ReportCategory.translation['name_ru'],
        'fixed': Report.fixed,
        'category_id': ReportCategory.id,
        'city_id': City.id
    }.get(view_field, None)


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
    report_on = datetime.fromtimestamp(body.get("time") / 1000.0)
    package_version = body.get("package_version")
    message = body.get("text")
    email = body.get("email")
    category = body.get("cat_id")
    city = body.get("city_name")
    node_old_id = body.get("id_node")
    screenshot = body.get("screenshot")
    photos = body.get("photos")

    if node_old_id:
        node = DBSession.query(Node) \
            .filter(Node.old_id == node_old_id) \
            .filter(Node.old_city_keyname == city) \
            .one()
    else:
        node = None

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


@view_config(route_name='change_report_state', renderer='json', request_method='POST',
             permission='edit')
def change_report_state(request):
    state = request.POST['state']
    report_id = request.matchdict['id']

    session = DBSession()
    report = session.query(Report).filter(Report.id == report_id).one()
    report.fixed = state
    session.commit()
    auth = 'true' if authenticated_userid(request) else 'false'
    return {
        'id': report.id,
        'fixed': report.fixed,
        'auth': auth
    }


@view_config(name='login', renderer='login.mako')
@forbidden_view_config(renderer='login.mako')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    message = ''
    login_params = ''
    password = ''
    if ('login' in request.params) and ('password' in request.params):
        login_params = request.params['login']
        password = request.params['password']
        if USERS.get(login_params) == password:
            headers = remember(request, login_params)
            return HTTPFound(location=came_from,
                             headers=headers)
        message = 'Failed login'

    return dict(
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login_params,
        password=password
    )


@view_config(route_name='edit', permission='edit')
def edit(request):
    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='delete', renderer='json', permission='edit', request_method='POST')
def delete(request):
    report_id = request.POST['id']
    session = DBSession()
    report = session.query(Report).filter(Report.id == report_id).one()
    session.delete(report)
    session.commit()
    return {'Result': 'OK'}


@view_config(route_name='logout', permission='edit', renderer='logout.mako', request_method="GET")
def logout(request):
    return {}


@view_config(route_name='logout', permission='edit', renderer='logout.mako', request_method="POST")
def logout_post(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)
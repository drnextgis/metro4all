from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home',          '/')
    config.add_route('reports',       '/reports')
    config.add_route('create_report', '/reports')
    config.add_route('reports_list',  '/reports/list')
    config.scan()
    return config.make_wsgi_app()

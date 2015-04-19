from pyramid.config import Configurator
from sqlalchemy import create_engine

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    sa_url = 'postgresql+psycopg2://%(user)s:%(password)s@%(host)s/%(name)s' % dict(
            user=settings['db.user'],
            password=settings['db.password'],
            host=settings['db.host'],
            name=settings['db.name'],
        )
    engine = create_engine(sa_url)
    
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()

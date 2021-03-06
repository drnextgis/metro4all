# -*- coding: utf-8 -*-
import os
import sys
import transaction

from sqlalchemy import create_engine

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Base,
    ReportCategory
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    sa_url = 'postgresql+psycopg2://%(user)s:%(password)s@%(host)s/%(name)s' % dict(
            user=settings['db.user'],
            password=settings['db.password'],
            host=settings['db.host'],
            name=settings['db.name'],
        )
    engine = create_engine(sa_url)

    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    DBSession.add(ReportCategory(translation=dict(name_ru=u"Информация")))
    DBSession.add(ReportCategory(translation=dict(name_ru=u"Ошибка")))
    DBSession.add(ReportCategory(translation=dict(name_ru=u"Проблема доступа")))
    DBSession.commit()

from pyramid.view import view_config


@view_config(route_name='home', renderer='home.mako')
def home(request):
    return {'one': '1', 'project': 'metro4all'}


@view_config(route_name='reports', renderer='reports.mako')
def reports(request):
    return {
        'one': '1', 'project': 'metro4all'
    }

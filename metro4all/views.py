from pyramid.view import view_config


@view_config(route_name='home', renderer='home.mako')
def home(request):
    return {'one': '1', 'project': 'metro4all'}


@view_config(route_name='reports', renderer='reports.mako')
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


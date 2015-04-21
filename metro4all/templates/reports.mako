<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <title>Сообщения</title>
    <link rel="shortcut icon" href="${request.static_url('metro4all:static/favicon.ico')}" type="image/x-icon">
    <!--[if IE]>
    <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
    <link href="${request.static_url('metro4all:static/contrib/jquery-ui-1.11.4/jquery-ui.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/contrib/jtable.2.4.0/themes/metro/metro4all/jtable.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/contrib/materialize/css/materialize.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/css/main.css')}"
          rel="stylesheet" type="text/css"/>
</head>
<body>


<div class="container">

    <div class="row title">
        <div class="col s12 blue-text text-lighten-5"><h2>MetroForAll</h2></div>
        <div class="col s12 subtitle blue-text text-lighten-4"><h4>Система сбора сообщений от пользователей</h4></div>
    </div>


    <div class="row">
        <div class="col s6"></div>
    </div>
    <div class="row filter">
        <ul class="collapsible" data-collapsible="accordion">
            <li>
                <div class="collapsible-header"><i class="mdi-action-search"></i>Фильтр</div>
                <div class="collapsible-body">
                    <form class="col s12">
                        <div class="row">
                            <div class="col select">
                                <label>Город</label>
                                <select class="browser-default">
                                    <option value="" selected>Не выбран</option>
                                    %for city in cities:
                                        <option value="${city.id}">${city.translation['name_ru']}</option>
                                    %endfor
                                </select>
                            </div>
                            <div class="col select">
                                <label>Узел</label>
                                <select class="browser-default" disabled>
                                    <option value="" selected>Не выбран</option>
                                </select>
                            </div>
                            <div class="col select">
                                <label>Категория</label>
                                <select class="browser-default">
                                    <option value="" selected>Не выбрана</option>
                                    %for cat in categories:
                                        <option value="${cat.id}">${cat.translation['name_ru']}</option>
                                    %endfor
                                </select>
                            </div>
                        </div>
                    </form>
                </div>
            </li>
        </ul>

    </div>
    <div class="row">
        <div class="col s12 reportsTable">
            <div id="reportsTable"></div>
        </div>
    </div>
</div>

<script src="${request.static_url('metro4all:static/contrib/jquery/jquery-1.11.2.min.js')}"
        type="text/javascript"></script>
<script src="${request.static_url('metro4all:static/contrib/jquery-ui-1.11.4/jquery-ui.min.js')}"
        type="text/javascript"></script>
<script src="${request.static_url('metro4all:static/contrib/jtable.2.4.0/jquery.jtable.min.js')}"
        type="text/javascript"></script>
<script src="${request.static_url('metro4all:static/contrib/jtable.2.4.0/localization/jquery.jtable.ru.js')}"
        type="text/javascript"></script>
<script src="${request.static_url('metro4all:static/contrib/materialize/js/materialize.js')}"
        type="text/javascript"></script>

<script type="text/javascript">
    $(document).ready(function () {

        $('.collapsible').collapsible({
            accordion: false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
        });

        $('#reportsTable').jtable({
            ##            title: 'Таблица сообщений',
                        paging: true,
            pageSize: 10,
            sorting: true,
            defaultSorting: 'report_on ASC',
            actions: {
                listAction: '/reports/list',
                updateAction: '/reports/update'
            },
            fields: {
                id: {
                    key: true,
                    list: false,
                    edit: false
                },
                city_name: {
                    title: 'Город',
                    width: '20%',
                    edit: false
                },
                node_name: {
                    title: 'Узел',
                    width: '20%',
                    edit: false,
                    display: function (data) {
                        var record = data.record;
                        return record.node_name || 'Не указан';
                    }
                },
                message: {
                    title: 'Описание',
                    width: '20%',
                    edit: false
                },
                category_name: {
                    title: 'Категория',
                    width: '20%'
                },
                report_on: {
                    title: 'Создан',
                    width: '20%',
                    create: false,
                    edit: false
                }
            }
        });
        $('#reportsTable').jtable('load');
    });
</script>
</body>
</html>
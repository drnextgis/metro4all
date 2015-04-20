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
    <link href="${request.static_url('metro4all:static/contrib/jtable.2.4.0/themes/lightcolor/gray/jtable.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/contrib/materialize/css/materialize.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/css/main.css')}"
          rel="stylesheet" type="text/css"/>
</head>
<body>


<div class="container">

    <div class="row blue lighten-1 blue-text text-lighten-5">
        <div class="col s12 blue lighten-2"><h2>MetroForAll / Reports</h2></div>
        <div class="col s12 blue-text text-lighten-4"><h4>Система сбора сообщений от пользователей</h4></div>
    </div>


    <div class="row">
        <div class="col s6"></div>
    </div>
    <div class="row">
        <ul class="collapsible" data-collapsible="accordion">
            <li>
                <div class="collapsible-header"><i class="mdi-action-search"></i>Фильтр</div>
                <div class="collapsible-body">
                    <form class="col s12">
                        <div class="row">
                            <div class="col s3">
                                <label>Город</label>
                                <select class="browser-default">
                                    <option value="" disabled selected>Выберите город</option>
                                </select>
                            </div>
                            <div class="col s3">
                                <label>Узел</label>
                                <select class="browser-default">
                                    <option value="" disabled selected>Выберите узел</option>
                                </select>
                            </div>
                            <div class="col s3">
                                <label>Категория</label>
                                <select class="browser-default">
                                    <option value="" disabled selected>Выберите категорию</option>
                                </select>
                            </div>
                        </div>
                    </form>
                </div>
            </li>
        </ul>

    </div>
    <div class="row">
        <div class="col s12">
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
            title: 'Таблица сообщений',
            paging: true,
            pageSize: 10,
            sorting: true,
            defaultSorting: 'City ASC',
            actions: {
                listAction: '/reports/list',
                updateAction: '/reports/update'
            },
            fields: {
                Id: {
                    key: true,
                    list: false
                },
                City: {
                    title: 'Город',
                    width: '20%'
                },
                Station: {
                    title: 'Узел',
                    width: '20%'
                },
                Text: {
                    title: 'Описание',
                    width: '20%'
                },
                Category: {
                    title: 'Категория',
                    width: '20%'
                },
                CreatedDate: {
                    title: 'Создан',
                    width: '20%',
                    type: 'date',
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
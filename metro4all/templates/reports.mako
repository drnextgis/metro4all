<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <title>Сообщения</title>
    <link rel="shortcut icon" href="${request.static_url('metro4all:static/favicon.ico')}" type="image/x-icon">
    <!--[if IE]>
    <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
    <link href="${request.static_url('metro4all:static/contrib/jquery-ui-1.11.4/jquery-ui.min.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/contrib/jtable.2.4.0/themes/metro/blue/jtable.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/contrib/materialize/css/materialize.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/css/main.css')}"
          rel="stylesheet" type="text/css"/>
</head>
<body>


<div class="container">
    <div class="row">
        <div class="col s12"><h3>Metro4all Reports</h3></div>
    </div>
    <div class="row">
        <form class="col s12">
            <div class="row">
                <div class="col s3">
                    <label>Browser Select</label>
                    <select class="browser-default">
                        <option value="" disabled selected>Выберите город</option>
                        <option value="1">Option 1</option>
                        <option value="2">Option 2</option>
                        <option value="3">Option 3</option>
                    </select>

                </div>
                <div class="col s3">
                    <label>Browser Select</label>
                    <select class="browser-default">
                        <option value="" disabled selected>Выберите станцию</option>
                        <option value="1">Option 1</option>
                        <option value="2">Option 2</option>
                        <option value="3">Option 3</option>
                    </select>
                </div>
            </div>
        </form>
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
        $('#reportsTable').jtable({
            title: 'Таблица сообщений',
            actions: {
                listAction: '/GettingStarted/PersonList',
                updateAction: '/GettingStarted/UpdatePerson',
                deleteAction: '/GettingStarted/DeletePerson'
            },
            fields: {
                Id: {
                    key: true,
                    list: false
                },
                City: {
                    title: 'Город',
                    width: '25%'
                },
                Station: {
                    title: 'Узел',
                    width: '25%'
                },
                Text: {
                    title: 'Описание',
                    width: '25%'
                },
                Category: {
                    title: 'Категория',
                    width: '25%'
                },
                RecordDate: {
                    title: 'Создан',
                    width: '25%',
                    type: 'date',
                    create: false,
                    edit: false
                }
            }
        });
    });
</script>
</body>
</html>
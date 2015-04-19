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
    <link href="${request.static_url('metro4all:static/contrib/jtable.2.4.0/themes/metro/blue/jtable.min.css')}"
          rel="stylesheet" type="text/css"/>
</head>
<body>
<div id="PersonTableContainer"></div>


<script src="${request.static_url('metro4all:static/contrib/jquery/jquery-1.11.2.min.js')}"
        type="text/javascript"></script>
<script src="${request.static_url('metro4all:static/contrib/jquery-ui-1.11.4/jquery-ui.min.js')}"
        type="text/javascript"></script>
<script src="${request.static_url('metro4all:static/contrib/jtable.2.4.0/jquery.jtable.min.js')}"
        type="text/javascript"></script>
<script src="${request.static_url('metro4all:static/contrib/jtable.2.4.0/localization/jquery.jtable.ru.js')}"
        type="text/javascript"></script>
<script type="text/javascript">
    $(document).ready(function () {
        $('#PersonTableContainer').jtable({
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
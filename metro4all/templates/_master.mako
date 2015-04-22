<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <title><%block name="title"/></title>
    <link rel="shortcut icon" href="${request.static_url('metro4all:static/favicon.ico')}" type="image/x-icon">
    <!--[if IE]>
    <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
    <link href="${request.static_url('metro4all:static/contrib/jquery-ui-1.11.4/jquery-ui.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/contrib/materialize/css/materialize.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/css/main.css')}"
          rel="stylesheet" type="text/css"/>
    <%block name="css"/>
</head>
<body>

<div class="container" <%block name="container_id"/>>

    <div class="row title">
        <div class="col s12 blue-text text-lighten-5">
            <h2>MetroForAll</h2>

            <p>Система сбора сообщений от пользователей</p>
        </div>
    </div>

    ${self.body()}

</div>

<script src="${request.static_url('metro4all:static/contrib/jquery/jquery-1.11.2.min.js')}"
        type="text/javascript"></script>
<script src="${request.static_url('metro4all:static/contrib/jquery-ui-1.11.4/jquery-ui.min.js')}"
        type="text/javascript"></script>
<script src="${request.static_url('metro4all:static/contrib/materialize/js/materialize.js')}"
        type="text/javascript"></script>
<script src="${request.static_url('metro4all:static/contrib/mustache/mustache.min.js')}"
        type="text/javascript"></script>
<script type="text/javascript">
    window.application_root = '${request.route_url('home')}';
</script>
    <%block name="scripts"/>
</body>
</html>
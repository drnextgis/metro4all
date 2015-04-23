<%
    from pyramid.security import authenticated_userid
    auth = 'true' if authenticated_userid(request) else 'false'
%>

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
        <div class="col s12">
            <h2><a href="${request.route_url('home')}">Сообщения</a> для <a href="http://metro4all.org/" target="_blank">Metro4All</a></h2>
            <p>Система сбора сообщений от пользователей с <a href="https://play.google.com/store/apps/details?id=com.nextgis.metroaccess" target="_blank">мобильных устройств</a></p>
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
    window.metroBugs = {};
    metroBugs.view = {};
    metroBugs.viewmodel = {};
    metroBugs.modules = {};
    metroBugs.templates = {
        state_checkbox: null
    };
    metroBugs.application_root = '${request.route_url('home')}';
    metroBugs.auth = ${auth};
</script>
    <%block name="scripts"/>
</body>
</html>
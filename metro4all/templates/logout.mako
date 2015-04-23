<%inherit file="_master.mako"></%inherit>

<%block name="title">Редактор сообщения</%block>

<%block name="css">
    <link href="${request.static_url('metro4all:static/contrib/jtable.2.4.0/themes/metro/metro4all/jtable.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/css/reports.css')}"
          rel="stylesheet" type="text/css"/>
</%block>

<div class="row">
    <div class="row">
        <form class="col s12" method="post">
            <div class="row">
                <div class="input-field col s6">
                    <button class="btn waves-effect waves-light" type="submit" name="action">Logout
                        <i class="mdi-content-send right"></i>
                    </button>
                </div>
            </div>
        </form>
    </div>
</div>
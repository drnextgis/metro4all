<%inherit file="_master.mako"></%inherit>

<%block name="title">Редактор сообщения</%block>

<%block name="css">
    <link href="${request.static_url('metro4all:static/contrib/jtable.2.4.0/themes/metro/metro4all/jtable.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/css/reports.css')}"
          rel="stylesheet" type="text/css"/>
</%block>

<%block name="container_id">id="edit"</%block>

<div class="row">
    <div class="col s12">
        <h3>Сообщение №${report.id}</h3>
    </div>
</div>
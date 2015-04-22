<%inherit file="_master.mako"></%inherit>

<%block name="title">Сообщения</%block>

<%block name="css">
    <link href="${request.static_url('metro4all:static/contrib/jtable.2.4.0/themes/metro/metro4all/jtable.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/css/reports.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/contrib/lightcase-2.0.3/css/lightcase.css')}"
          rel="stylesheet" type="text/css"/>
</%block>


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
##                        <div class="col select">
##                            <label>Узел</label>
##                            <select class="browser-default" disabled>
##                                <option value="" selected>Не выбран</option>
##                            </select>
##                        </div>
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
<div class="row table">
    <div class="col s12 reportsTable">
        <div id="reportsTable"></div>
    </div>
</div>

<%block name="scripts">
    <script src="${request.static_url('metro4all:static/contrib/jtable.2.4.0/jquery.jtable.min.js')}"
            type="text/javascript"></script>
    <script src="${request.static_url('metro4all:static/contrib/jtable.2.4.0/localization/jquery.jtable.ru.js')}"
            type="text/javascript"></script>
    <script src="${request.static_url('metro4all:static/contrib/lightcase-2.0.3/lightcase.min.js')}"
            type="text/javascript"></script>

    <%
        import time
        timestamp = '?' + str(int(time.time()))
    %>
    <script src="${request.static_url('metro4all:static/js/init.js') + timestamp}"
            type="text/javascript"></script>
    <script src="${request.static_url('metro4all:static/js/reports-table.js') + timestamp}"
            type="text/javascript"></script>
    <script src="${request.static_url('metro4all:static/js/reports-table-filter.js') + timestamp}"
            type="text/javascript"></script>
</%block>
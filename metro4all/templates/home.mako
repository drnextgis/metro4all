<%inherit file="_master.mako"></%inherit>

<%block name="title">Сообщения</%block>

<%block name="css">
    <link href="${request.static_url('metro4all:static/contrib/jtable.2.4.0/themes/metro/metro4all/jtable.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/css/reports.css')}"
          rel="stylesheet" type="text/css"/>
</%block>


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

<%block name="scripts">
    <script src="${request.static_url('metro4all:static/contrib/jtable.2.4.0/jquery.jtable.min.js')}"
            type="text/javascript"></script>
    <script src="${request.static_url('metro4all:static/contrib/jtable.2.4.0/localization/jquery.jtable.ru.js')}"
            type="text/javascript"></script>

    <script type="text/javascript">
        $(document).ready(function () {

            $('.collapsible').collapsible({
                accordion: false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
            });

            $('#reportsTable').jtable({
                paging: true,
                pageSize: 10,
                sorting: true,
                defaultSorting: 'report_on ASC',
                actions: {
                    listAction: '/reports/list'
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
                    report_on: {
                        title: 'Создан',
                        width: '10%',
                        create: false,
                        edit: false
                    },
                    category_name: {
                        title: 'Категория',
                        width: '10%',
                        display: function (data) {
                            var record = data.record;
                            return '<span data-category="' + record.category + '">' +
                                    record.category_name + '</span>';
                        }
                    },
                    fixed: {
                        title: 'Статус',
                        width: '8%',
                        create: false,
                        edit: false
                    },
                    edit: {
                        width: '2%',
                        display: function (data) {
                            var url_template = '${request.route_url('reports_edit', id='report_id')}';
                            url_template = url_template.replace('report_id', data.record.id);
                            return '<a href="' + url_template + '"><i class="mdi-action-search"></i></a>';
                        }
                    }
                }
            });
            $('#reportsTable').jtable('load');
        });
    </script>
</%block>
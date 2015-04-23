metroBugs.modules['reportsTable'] = {
    init: function () {
        this.setDom();
        this.initReportTable();
        this.loadTable();
    },

    setDom: function () {
        metroBugs.view.$table = $('#reportsTable');
    },

    initReportTable: function () {
        var context = this,
            jtableSettings;

        jtableSettings = {
            paging: true,
            pageSize: 10,
            sorting: true,
            defaultSorting: 'report_on DESC',
            actions: {
                listAction: '/reports/list'
            },
            fields: {
                id: {
                    key: true,
                    title: '#',
                    width: '3%',
                    edit: false
                },
                city_name: {
                    title: 'Город',
                    width: '10%',
                    edit: false
                },
                node_name: {
                    title: 'Узел',
                    sorting: false,
                    width: '12%',
                    edit: false,
                    display: function (data) {
                        var record = data.record;
                        return record.node_name || '';
                    }
                },
                message: {
                    title: 'Описание',
                    width: '40%',
                    sorting: false,
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
                    width: '12%',
                    display: function (data) {
                        var record = data.record;
                        return '<span data-category="' + record.category + '">' +
                            record.category_name + '</span>';
                    },
                    edit: false
                },
                fixed: {
                    title: 'Статус',
                    width: '9%',
                    create: false,
                    display: function (data) {
                        var report = data.record,
                            fixed = report.fixed;
                        return Mustache.render(metroBugs.templates.state_checkbox, {
                            fixed: fixed,
                            id: report.id,
                            auth: metroBugs.auth
                        });
                    }
                },
                scheme: {
                    width: '2%',
                    sorting: false,
                    display: function (data) {
                        var preview = data.record.preview,
                            html = '';
                        if (preview) {
                            html = '<a data-rel="lightcase" href="http://reports.metro4all.ru/images/' +
                            preview +
                            '.jpg"><i class="mdi-social-share"></i></a>';
                        }
                        return html;
                    },
                    edit: false
                },
                photos: {
                    width: '2%',
                    sorting: false,
                    display: function (data) {
                        var photos = data.record.photos,
                            html = '',
                            photosCount = photos.length;
                        if (photosCount > 0) {
                            for (var i = 0; i < photosCount; i++) {
                                html += '<a data-rel="lightcase:' + data.record.id +
                                '" href="http://reports.metro4all.ru/images/' +
                                photos[i].photo +
                                '.jpg"><i ' + (i == 0 ? 'class="mdi-maps-local-see' : '') +
                                '"></i></a>';
                            }
                        }
                        return html;
                    },
                    edit: false
                }
            }
        };

        if (metroBugs.auth) {
            jtableSettings.actions.deleteAction = metroBugs.application_root + 'reports/delete';
            jtableSettings.recordsLoaded = function () {
                $('a[data-rel^=lightcase]').lightcase();
                context.bindCheckboxesStateEvents();
            };
        } else {
            jtableSettings.fields.edit = {
                width: '2%',
                sorting: false,
                display: function (data) {
                    return '<a href="' + metroBugs.application_root + 'edit' + '"><i class="mdi-editor-border-color"></i></a>';
                },
                edit: false
            };
        }

        metroBugs.view.$table.jtable(jtableSettings);
    },

    loadTable: function () {
        metroBugs.view.$table.jtable('load');
    },

    bindCheckboxesStateEvents: function ($element) {
        var context = this;

        if (!$element) {
            $element = metroBugs.view.$table.find('input.state')
        }

        $element.change(function () {
            var $this = $(this),
                id = $this.attr('id').split('-')[1],
                checked = $this.is(":checked"),
                $divState = $this.parents('div.state');

            $divState.addClass('loading');
            $.ajax({
                url: metroBugs.application_root + 'reports/' + id + '/state/change',
                method: 'POST',
                data: {state: checked}
            }).then(function (stateModel) {
                context.setStateDivContent($divState, stateModel);
            });
        });
    },

    setStateDivContent: function ($divState, stateModel) {
        var $td = $divState.parent();
        $td.empty().html(Mustache.render(metroBugs.templates.state_checkbox, stateModel));
        this.bindCheckboxesStateEvents($td.find('input.state'));
    }
};
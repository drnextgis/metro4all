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
        metroBugs.view.$table.jtable({
            paging: true,
            pageSize: 10,
            sorting: true,
            defaultSorting: 'report_on DESC',
            actions: {
                listAction: '/reports/list'
            },
            recordsLoaded: function () {
                $('a[data-rel^=lightcase]').lightcase();
            },
            fields: {
                id: {
                    title: '#',
                    width: '3%'
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
                    }
                },
                fixed: {
                    title: 'Статус',
                    width: '9%',
                    create: false,
                    edit: false
                },
                scheme: {
                    width: '2%',
                    sorting: false,
                    display: function (data) {
                        var preview = data.record.preview,
                            html = '';
                        if (preview) {
                            html = '<a data-rel="lightcase" href="http://demo.nextgis.ru:6543/images/' +
                            preview +
                            '.jpg"><i class="mdi-social-share"></i></a>';
                        }
                        return html;
                    }
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
                                '" href="http://demo.nextgis.ru:6543/images/' +
                                photos[i].photo +
                                '.jpg"><i ' + (i == 0 ? 'class="mdi-maps-local-see' : '') +
                                '"></i></a>';
                            }
                        }
                        return html;
                    }
                }
            }
        });
    },

    loadTable: function () {
        metroBugs.view.$table.jtable('load');
    }
};
metroBugs.modules['reportsTableFilter'] = {
    init: function () {
        this.setDom();
        this.bindEvents();
    },

    setDom: function () {
        metroBugs.view.$selectCity = $('#selectCity');
        metroBugs.view.$selectCategory = $('#selectCategory');
    },

    bindEvents: function () {
        var context = this;
        metroBugs.view.$selectCity.change(function () {
            context.updateTable();
        });
        metroBugs.view.$selectCategory.change(function () {
            context.updateTable();
        });
    },

    updateTable: function () {
        var view = metroBugs.view;

        metroBugs.view.$table.jtable('load', {
            category_id: view.$selectCategory.val(),
            city_id: view.$selectCity.val()
        });
    }
};
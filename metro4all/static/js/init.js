window.metroBugs = {};

metroBugs.view = {};
metroBugs.viewmodel = {};
metroBugs.modules = {};
metroBugs.templates = {
    state_checkbox: null
};

$(document).ready(function () {
    var templatesDeferreds = [],
        templateDeferred;

    for (var template in metroBugs.templates) {
        templateDeferred = $.get(application_root + 'static/js/templates/' + template + '.mustache', function (template) {
            metroBugs.templates[template] = template;
        });
        templatesDeferreds.push(templateDeferred);
    }

    $.when.apply(window, templatesDeferreds).then(function () {
        for (var module in metroBugs.modules) {
            metroBugs.modules[module].init();
        }
    });
});
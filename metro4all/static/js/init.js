metroBugs = metroBugs || {};

$(document).ready(function () {
    var templatesDeferreds = [],
        templateDeferred;

    for (var templateName in metroBugs.templates) {
        templateDeferred = $.get(metroBugs.application_root + 'static/js/templates/' + templateName + '.mustache', function (template) {
            metroBugs.templates[templateName] = template;
        });
        templatesDeferreds.push(templateDeferred);
    }

    $.when.apply(window, templatesDeferreds).then(function () {
        for (var module in metroBugs.modules) {
            metroBugs.modules[module].init();
        }
    });
});
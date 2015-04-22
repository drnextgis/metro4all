window.metroBugs = {};

metroBugs.view = {};
metroBugs.viewmodel = {};
metroBugs.modules = {};

$(document).ready(function () {
    for(var module in metroBugs.modules) {
        metroBugs.modules[module].init();
    }
});
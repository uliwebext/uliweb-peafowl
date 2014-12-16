requirejs.config({
    "baseUrl": "/static/js/vendor",
    "paths": {
        "app"      : '../modules',
        "jquery"   : '/static/jquery/jquery-1.11.1.min',
        "text"     : 'require/text',
        "css"      : 'require/css', 
        "markdown" : 'Markdown.Converter',

        //--------------------------------------
        "scrolling"        : '_mmgrid/scrolling',
        "mmgrid"           : '_mmgrid/mmGrid',
        "mmpaginator"      : '_mmgrid/mmPaginator',
        "mmtreegrid"       : '_mmgrid/mmTreeGrid',
        "select2"          : '_select2/select2',
        "jqdialog2"        : 'jquery.dialog2/jquery.dialog2',
        "jqdialog2-helper" : "jquery.dialog2/jquery.dialog2.helpers",
        "adminLTE"         : "app/adminLTE"
    },
    "shim": {
        "mmgrid": {
            deps: ['css!_mmgrid/mmGrid'],
            exports: 'jQuery.fn.mmGrid'},
        "mmpaginator": {
            deps: ['scrolling', 'css!_mmgrid/mmPaginator'],
            exports: 'jQuery.fn.mmPaginator'},
        "mmtreegrid": {
            deps: ["mmgrid", "css!_mmgrid/mmTreeGrid"],
            exports: 'jQuery.fn.mmGrid'},
        "select2": {
            deps: ["css!_select2/select2"],
            exports: 'jQuery.fn.select2'
        },
        "jqdialog2": {
            deps: [
                "jquery.dialog2/jquery.controls",
                "css!jquery.dialog2/jquery.dialog2"
            ],
            exports: 'jQuery.fn.dialog2'
        },
        "jqdialog2-helper": {
            deps: ["jqdialog2"],
            exports: 'jQuery.fn.dialog2.helpers'
        }
    },
    urlArgs: "bust=" +  (new Date()).getTime()
});

// Load the main app module to start the app
requirejs(["app/main", "markdown"]);

requirejs.config({
    "baseUrl": "/static/js/vendor",
    "paths": {
        "app"      : '../modules',
        "jquery"   : '/static/jquery/jquery-1.11.1.min',
        "text"     : 'require/text',
        "css"      : 'require/css', 
        "markdown" : 'Markdown.Converter',

        //--------------------------------------
        "mmGrid"         : 'mmgrid/mmGrid',
        "mmPaginator"    : 'mmgrid/mmPaginator',
        "mmTreeGrid"     : 'mmgrid/mmTreeGrid',
        "select2"        : 'select2/select2',
        "dialog2"        : 'jquery.dialog2/jquery.dialog2',
        "dialog2-helper" : "jquery.dialog2/jquery.dialog2.helpers"
    },
    "shim": {
        "mmGrid": {
            deps: ['mmgrid/scrolling','css!mmgrid/mmGrid'],
            exports: 'jQuery.fn.mmGrid'},
        "mmPaginator": {
            deps: ['css!mmgrid/mmPaginator'],
            exports: 'jQuery.fn.mmPaginator'},
        "mmTreeGrid": {
            deps: ["mmGrid", "css!mmgrid/mmTreeGrid"],
            exports: 'jQuery.fn.mmGrid'},
        "select2": {
            deps: ["css!select2"],
            exports: 'jQuery.fn.select2'
        },
        "dialog2": {
            deps: [
                "jquery.dialog2/jquery.controls",
                "css!jquery.dialog2/jquery.dialog2"
            ],
            exports: 'jQuery.fn.dialog2'
        },
        "dialog2-helper": {
            deps: ["dialog2"],
            exports: 'jQuery.fn.dialog2.helpers'
        }
    },
    urlArgs: "bust=" +  (new Date()).getTime()
});

// Load the main app module to start the app
requirejs(["app/main", "markdown"]);

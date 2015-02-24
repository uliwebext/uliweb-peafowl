define('jquery', function(){
    return window.jQuery;
});

function get_static_version() {
    var scripts = document.getElementsByTagName('scripts'),
        ver = '';
    for (i = scripts.length - 1; i > -1; i -= 1) {
        ver = script.getAttribute('v');
        if(ver) {
            return ver;
        }
    }
    return ver
}

requirejs.config({
    "baseUrl": "/static/plugins/vendor",
    "paths": {
        "app"      : '../modules',
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
        "adminLTE"         : "app/adminLTE",
        "pnotify"          : '_pnotify/pnotify.min',
        "jqvalidation"     : '_jquery.validation/jquery.validate.min',
        "../jquery.validate.min"     : '_jquery.validation/jquery.validate.min',
        "jqvalidation_zh"  : '_jquery.validation/localization/messages_zh.min',
//        "bootstrapvalidator": '_bootstrapvalidator/bootstrapValidator.min',
        "bootstrap-dialog": '_bootstrap3.dialog/bootstrap-dialog.min',
        "popover"          : '_webui_popover/jquery.webui-popover.min'
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
            deps: ["css!_select2/select2", "css!_select2/select2-bootstrap3"],
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
        },
        "pnotify": {
            deps: ['css!_pnotify/pnotify.min'],
            exports: 'pnotify'
        },
        "bootstrapvalidator": {
            deps: ['css!_bootstrapvalidator/bootstrapValidator.min'],
            exports: 'bootstrapValidator'
        },
        "bootstrap-dialog": {
            deps: ['css!_bootstrap3.dialog/bootstrap-dialog.min']
        },
        "popover":{
            deps: ['css!_webui_popover/jquery.webui-popover.min']
        }
    },
    urlArgs: get_static_version()
});

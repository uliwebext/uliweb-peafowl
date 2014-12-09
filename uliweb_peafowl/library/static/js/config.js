requirejs.config({
    "baseUrl": "/static/js/vendor",
    "paths": {
        "app"      : '../modules',
        "jquery"   : '/static/jquery/jquery-1.11.1.min.js',
        "text"     : 'require/text',
        "css"      : 'require/css', 
        "markdown" : 'Markdown.Converter',

        "mmGrid"     : 'mmgrid/mmGrid',
        "mmTreeGrid" : 'mmgrid/mmTreeGrid'
    },
    "shim": {
        "mmGrid": {
            deps: [
                'mmgrid/mmPaginator',
                'mmgrid/scrolling',

                'css!mmgrid/mmGrid',
                'css!mmgrid/mmPaginator'
            ],
            exports: 'jQuery.fn.mmGrid'
        },
        "mmTreeGrid": {
            deps: [
                "mmgrid/mmGrid", 
                "css!mmgrid/mmTreeGrid"
            ],
            exports: 'jQuery.fn.mmGrid'
        }
    },
    urlArgs: "bust=" +  (new Date()).getTime()
});

// Load the main app module to start the app
requirejs(["app/main", "markdown"]);

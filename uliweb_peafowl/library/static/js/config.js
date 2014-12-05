requirejs.config({
    "baseUrl": "/static/js/lib",
    "paths": {
        "jquery": '/static/jquery/jquery-1.11.1.min.js',
    },
    "shim": {
    }
});

// Load the main app module to start the app
requirejs(["app/main"]);

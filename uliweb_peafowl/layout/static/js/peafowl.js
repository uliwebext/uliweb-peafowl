var show_message = function(message, category){
    require(['pnotify'], function(pnotify){
        new PNotify({
            history: {history: false}
            , text: message
            , type: category || 'success'
            , delay: 5000
            /*
            , animate_speed: 500
            , animation: {
                'effect_in': 'scale',
                'options_in': {easing:'easeOutElastic',percent:100},
                'effect_out': 'scale',
                'options_out': {easing:'easeInCubic',percent:0}
            }*/
        });
    });
}

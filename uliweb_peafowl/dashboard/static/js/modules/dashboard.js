
define(function(){

    var utils = {};

    var refresh_digital_panes = function(panes, container, template) {

        var len = panes.length;
        if(len==6) {
            colspan = 2
        } else if (len == 5) {
            colspan = 3
        } else if (len == 4) {
            colspan = 3
        } else if (len == 3) {
            colspan = 4
        } else if (len == 2) {
            colspan = 6
        } else if (len == 1) {
            colspan = 12
        } else {
            colspan = 3
        }

        var html = []
        for(var i=0; i<len; i++) {
            var pane = panes[i]
            var text = template;
            text = text.replace("{id}", pane.id)
            text = text.replace("{colspan}", colspan)
            text = text.replace("{color}", pane.color || "red")
            text = text.replace("{title}", pane.title || "Unititle")
            html.push(text)
        }

        $(container).html(html.join(""))

    }

    utils.refresh_digital_panes = refresh_digital_panes;


    return utils;
});
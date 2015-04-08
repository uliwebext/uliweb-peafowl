
define(["jquery"], function($){

    var utils = {};

    // Simple JavaScript Templating
    // John Resig - http://ejohn.org/ - MIT Licensed
    (function(utils){
      var cache = {};
     
      utils.tmpl = function tmpl(str, data){
        // Figure out if we're getting a template, or if we need to
        // load the template - and be sure to cache the result.
        var fn = !/\W/.test(str) ?
          cache[str] = cache[str] ||
            tmpl(document.getElementById(str).innerHTML) :
         
          // Generate a reusable function that will serve as a template
          // generator (and which will be cached).
          new Function("obj",
            "var p=[],print=function(){p.push.apply(p,arguments);};" +
           
            // Introduce the data as local variables using with(){}
            "with(obj){p.push('" +
           
            // Convert the template into pure JavaScript
            str
              .replace(/[\r\t\n]/g, " ")
              .split("<%").join("\t")
              .replace(/((^|%>)[^\t]*)'/g, "$1\r")
              .replace(/\t=(.*?)%>/g, "',$1,'")
              .split("\t").join("');\n")
              .split("%>").join("p.push('")
              .split("\r").join("\\'")
          + "');}return p.join('');\n");
       
        // Provide some basic currying to the user
        return data ? fn( data ) : fn;
      };
    })(utils);

    var Dashboard = function() {
    }

    Dashboard.prototype = {
        init: function() {

        },

        render_digital : function(element, template_name, digital_defs) {
            var html = utils.tmpl(template_name, {'digital': digital_defs})
            $(element).html(html);
        },

        render_content: function(element, template_name, content_defs) {
            var html = utils.tmpl(template_name, {'content': content_defs})
            $(element).html(html);
        }
    }

    

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
    utils.Dashboard = Dashboard;

    return utils;
});
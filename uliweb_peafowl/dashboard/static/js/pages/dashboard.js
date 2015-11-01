
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
        this._box_id = 1;
    }

    Dashboard.prototype = {
        init: function() {

        },

        get_boxid: function() {
            return "bid-" + this._box_id++;
        },

        render: function(element, template_name, data) {
            data['dashboard'] = this;
            var html = utils.tmpl(template_name, data)
            $(element).html(html);
        },

        is_pane_added: function(paneName, paneLayout) {
            for(var i=0; i<paneLayout.length; i++) {
                for(var j=0; j<paneLayout[i].panes.length; j++) {
                    if(paneLayout[i].panes[j].name == paneName) {
                        return true
                    }
                }
            }

            return false
        },

        ajax_content_loading: function(url, element) {
            $.get(url, function(result){
                $(element).html(result);
            });
        },

        calc_digital_colspan: function(pane_size) {
            if(pane_size==6) {
                colspan = 2
            } else if (pane_size == 5) {
                colspan = 3
            } else if (pane_size == 4) {
                colspan = 3
            } else if (pane_size == 3) {
                colspan = 4
            } else if (pane_size == 2) {
                colspan = 6
            } else if (pane_size == 1) {
                colspan = 12
            } else {
                colspan = 3
            }   
            
            return colspan         
        }
    }

    utils.Dashboard = Dashboard;

    return utils;
});
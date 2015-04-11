var show_message = function(message, category){

    require(["jqtoastr"], function(toastr){
        category = category || "success"

        var config = {
            "closeButton": true,
            "positionClass": "toast-top-center"   
        }
        var title = ""

        if(category == "success") {
            toastr.success(message, title, config)
        } else if (category == "error") {
            toastr.error(message, title, config)
        } else if (category == "info") {
            toastr.info(message, title, config)
        } else if (category == "warning") {
            toastr.warning(message, title, config)
        } else {
            toastr.info(message, title, config)
        }
    });

    return;

}


/* popup dialog

   @param target: target element
   @param options: could be url or plain object

   async content sould fire 'success.form' event, it'll hide the popup by default
*/
function popup_url(target, options, title){
    var opts;
    if (typeof options === 'string'){
        opts = {url:options, title:title || ''};
    }else opts = options;

    var d = {
        content:function(data){
            var begin, end;
            begin = data.indexOf('<!-- form -->')
            end = data.indexOf('<!-- end form -->')
            if (begin > -1 && end > -1){
                return data.substring(begin, end);
            }
            return data;
        },
        async: {
            success: function(that){
                that.getContentElement().on('success.form', function(e, data){
                    that.hide();
                });
            }
        },
        title: 'Popup',
        width:400,
        cache:false,
        height:'auto',
        padding:true,
        closeable:true,
        type:'async',
        url:'example',
        delay:50
    };

    require(['popover'], function(){
        var o = $.extend({}, d, opts);
        $(target).webuiPopover(o);
    });
}
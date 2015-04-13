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
function popup_url(target, options, title, callback){
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
                    if (callback) callback(data);
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

/*
 * process ajax request and jquery.validation
 */

function common_ajax_submit(target, validator){
    require(['jquery.form'], function(){
        var el = $(target);
        el.ajaxSubmit({
            beforeSubmit:function(){
                el.find(':submit').prop('disabled', true);
            },
            success:function(data){
                if (data.success){
                    el.trigger('success.form', data);
                }else{
                    validator.showErrors(data.errors);
                }
                el.find(':submit').prop('disabled', false);
            },
            error:function(){
                el.find(':submit').prop('disabled', false);
            }
        });
    });
}

/*
 * options:
 *    rules
 *    messages
 *    ajax_submit
 */
var do_submit = function(target, options) {
    var default_options = {
        rules:{},
        messages:{},
        ajax_submit:common_ajax_submit
    }

    var opts = $.extend({}, default_options, options);

    require(['jqvalidation'], function(){
        var form = $(target);
        var validator = form.validate({
            errorElement : 'span',
            errorClass : 'help-block',
            focusInvalid : true,
            rules : opts.rules,
            messages : opts.messages,
            highlight : function(element) {
                $(element).closest('.form-group').addClass('has-error');
            },

            success : function(label) {
                label.closest('.form-group').removeClass('has-error');
                label.remove();
            },

            errorPlacement : function(error, element) {
                element.parent('div').append(error);
            },

            submitHandler : function(form) {
                opts.ajax_submit(form, validator);
            }
        });

    });
}
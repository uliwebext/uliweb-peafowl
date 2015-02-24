#coding=utf-8
from uliweb import expose, functions

@expose('/library_demo')
class LibraryDemoView(object):
    def bootstrap3dialog(self):
        return {}

    def iconsheet(self):
        return {}

    def webui_popover(self):
        return {}

    def webui_popover_dialog(self):
        import uliweb.form as form
        class MyForm(form.Form):
            name = form.StringField(required=True)

            def post_html(self):
                return """<script>
                require(['jquery.form'], function(){
                    $('#dialog').ajaxForm();
                });
                </script>
                """

        f = MyForm(id='dialog')
        f.form_action = url_for(self.__class__.webui_popover_dialog)
        if request.method == 'GET':
            return f.html()
        else:
            if f.validate(request.POST):
                return json({'success':True})
            else:
                r = {'success':False, 'errors':f.errors}
                return json(r)

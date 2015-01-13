#coding=utf-8
from uliweb.form import *
from uliweb import expose, functions
from uliweb.i18n import ugettext_lazy as _
import logging

log = logging.getLogger(__name__)

def __begin__():
    functions.require_login_admin()

class AddForm(Form):
    def form_validate(self, data):
        from uliweb.utils.common import import_attr, log
        from uliweb.orm import Model

        errors = {}

        if data['basemodel']:
            try:
                m = functions.get_model(data['basemodel'])
                if not (isinstance(m, type) and issubclass(m, Model)):
                    errors['basemodel'] = _("Object is not a subclass of Model")
            except Exception as e:
                log.exception(e)
                errors['basemodel'] = _("Model can't be imported")

        return errors    

@expose('/admin/sheet_config')
class AdminSheetConfigView(object):

    def __init__(self):
        self.model = functions.get_model('sheet_config')
        self.model_his = functions.get_model('sheet_config_his')

    @expose('')
    def index(self):

        fields = [
            {'name':'display_name', 'width':200},
            {'name':'sheet_name', 'width':200},
            {'name':'is_published', 'verbose_name':_('生效'), 'width':100},
            'description',
            {'name':'published_time', 'width':150},
            {'name':'action', 'verbose_name':_('操作'), 'width':120}
        ]        

        def action(value, obj):
            from uliweb.core.html import Tag
            actions = [
                Tag('a', '<i class="fa fa-eye"></i>', title=_('查看'),
                    href=url_for(self.__class__.view, sheet_id=obj.id),
                    _class="btn btn-xs btn-flat btn-primary"),
                Tag('a', '<i class="fa fa-remove"></i>', title=_('删除'),
                    href=url_for(self.__class__.delete, sheet_id=obj.id),
                    _class="btn btn-xs btn-flat btn-danger action-delete"),

            ]

            return ' '.join(map(str, actions))


        fields_convert_map = {
            'action': action,
        }
        view = functions.ListView(self.model, fields=fields, 
            fields_convert_map=fields_convert_map)
        objects = view.objects()
        return {
            'view': view, 
            'objects': objects,
            'total': view.total
        }

    def add(self):

        fields = ['sheet_name', 'display_name', 'description', 'basemodel']

        def post_created_form(fcls, model):
            from uliweb_admin.ulayout.form_helper import Bootstrap3Layout
            from uliweb.form.widgets import Button

            fcls.layout_class = Bootstrap3Layout
            fcls.form_buttons = [
                str(Button(value=_('保存'), _class="btn btn-primary btn-sm",
                    name="submit", type="submit")),
                ]

        def pre_save(data):
            from uliweb.utils.common import get_uuid, import_attr
            data['uuid'] = get_uuid()

            if not data['display_name']:
                data['display_name'] = data['sheet_name']


        def post_save(obj, data):
            obj.sync()

        view = functions.AddView(self.model_his, 
            ok_url=url_for(self.__class__.index),
            post_created_form=post_created_form,
            form_cls=AddForm,
            pre_save=pre_save,
            post_save=post_save,
            fields=fields, version=True)

        return view.run()

    def view(self, sheet_id):
        pass

    def delete(self, sheet_id):
        row = self.model.get(self.model.c.id==sheet_id)
        sheet_name = row.sheet_name
        row.delete()

        for obj in self.model_his.filter(self.model_his.c.sheet_name==sheet_name):
            obj.delete()
        return json({'success':True})


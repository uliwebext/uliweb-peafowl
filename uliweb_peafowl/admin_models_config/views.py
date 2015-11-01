#coding=utf-8
from uliweb import expose, functions
from uliweb.i18n import ugettext_lazy as _
import logging

log = logging.getLogger(__name__)

def __begin__():
    functions.require_login()

@expose('/admin/models_config')
class AdminModelsConfigView(object):
    """
    Model administration config app
    """

    def __init__(self):
        self.model = functions.get_model('model_config')
        self.model_his = functions.get_model('model_config_his')

    @expose('')
    def index(self):
        fields = [
            {'name':'display_name', 'width':200},
            {'name':'model_name', 'width':200},
            {'name':'is_published', 'verbose_name':_('Is Published'), 'width':100},
            'description',
            {'name':'published_time', 'width':150},
            {'name':'action', 'verbose_name':_('Action'), 'width':120}
        ]

        def _action(value, obj):
            from uliweb.core.html import Tag

            actions = [
                Tag('a', '<i class="fa fa-eye"></i>', title=_('View'),
                    href=url_for(self.__class__.view, model_name=obj.model_name),
                    _class="btn btn-xs btn-primary"),
                Tag('a', '<i class="fa fa-remove"></i>', title=_('Delete'),
                    href=url_for(self.__class__.delete, model_name=obj.model_name),
                    _class="btn btn-xs btn-danger action-delete"),

            ]
            if obj.uuid:
                actions.insert(1, Tag('a', '<i class="fa fa-toggle-off"></i>', title=_('Unpublish'),
                    href=url_for(self.__class__.unpublish, model_name=obj.model_name),
                    _class="btn btn-xs btn-warning action-unpublish"))
            return ' '.join(map(str, actions))

        def _is_published(value, obj):
            if obj.uuid:
                return '<i class="fa fa-check-square-o"></i> (%s)' % obj.uuid
            else:
                return '<i class="fa fa-square-o"></i>'

        fields_convert_map = {'action':_action, 'is_published':_is_published}

        view =functions.ListView(self.model, fields=fields,
                                 fields_convert_map=fields_convert_map)
        objects = view.objects()
        return {'view':view, 'objects':objects, 'total':view.total}

    def add(self):
        from forms import AddForm

        fields = ['model_name', 'display_name', 'table_name', 'description',
                  'basemodel', 'has_extension', 'extension_model']

        def post_created_form(fcls, model):
            from uliweb.form.widgets import Button

            fcls.layout_class = 'bs3t'
            fcls.form_buttons = [
                str(Button(value=_('Save'), _class="btn btn-primary btn-sm",
                    name="submit", type="submit")),
                ]

        def pre_save(data):
            from uliweb.utils.common import get_uuid, import_attr
            from uliweb.contrib.model_config import get_model_fields, get_model_indexes

            data['uuid'] = get_uuid()[:6]
            if not data['table_name']:
                data['table_name'] = data['model_name'].lower()

            if not data['display_name']:
                data['display_name'] = data['model_name']

            #add import basemodel support
            if data['basemodel']:
                BM = import_attr(data['basemodel'])
                data['fields'] = get_model_fields(BM)
                data['indexes'] = get_model_indexes(BM)

            if data['extension_model']:
                EM = import_attr(data['extension_model'])
                data['extension_fields'] = get_model_fields(EM)
                data['extension_indexes'] = get_model_indexes(EM)

        def post_save(obj, data):
            r = self.model(model_name=obj.model_name,
                           display_name=obj.display_name,
                           description=obj.description,
                           modified_user=request.user.id)
            r.save(version=True)


        view = functions.AddView(self.model_his, ok_url=url_for(self.__class__.index),
                                 post_created_form=post_created_form,
                                 form_cls=AddForm,
                                 pre_save=pre_save,
                                 post_save=post_save,
                                 fields=fields, version=True)
        return view.run()

    def _get_model(self, model_name, uuid):
        return self.model_his.get((self.model_his.c.model_name==model_name) &
                                    (self.model_his.c.uuid==uuid))

    def view(self, model_name):
        model = self.model.get(self.model.c.model_name==model_name)

        uuid = request.GET.get('uuid')
        uuids = [row.uuid for row in
                    self.model_his.filter(self.model_his.c.model_name==model_name)\
                        .fields(self.model_his.c.uuid)\
                        .order_by(self.model_his.c.create_time.desc())]

        obj = None
        if not uuid and len(uuids)>0:
            uuid = uuids[0]

        if uuid in uuids:
            obj = self._get_model(model_name, uuid)

        template_data = {'uuids':uuids, 'model_name':model_name,
                         'uuid':uuid, 'object':obj, 'published_uuid':model.uuid if model else ''}
        if obj:
            template_data['columns'] = eval(obj.fields or '[]')
            template_data['indexes'] = eval(obj.indexes or '[]')
            template_data['extension_columns'] = eval(obj.extension_fields or '[]')
            template_data['extension_indexes'] = eval(obj.extension_indexes or '[]')
            fields = ['model_name', 'display_name', 'table_name', 'basemodel', 'has_extension', 'extension_model']
            view = functions.DetailView(self.model_his, obj=obj, fields=fields,
                                        template_data=template_data)
            return view.run()
        else:
            template_data['view'] = ''
            template_data['columns'] = []
            template_data['indexes'] = []
            template_data['extension_columns'] = []
            template_data['extension_indexes'] = []
            return template_data

    def save(self, model_name):
        import json as JSON
        from uliweb.utils.common import get_uuid

        column_name = request.GET.get('column_name')
        column = JSON.loads(request.POST[column_name])
        uuid = request.GET.get('uuid')
        action = request.GET.get('action')

        obj = self._get_model(model_name, uuid)
        old_column = getattr(obj, column_name)

        list_columns = column_name in ('fields', 'indexes', 'extension_fields',
                                       'extension_indexes')
        if list_columns:
            old_column = eval(old_column or '[]')

        index = -1
        if action in ('edit', 'delete'):
            for x in range(len(old_column)):
                if old_column[x]['name'] == column['name']:
                    index = x
                    break

        if index >= 0:
            reserved = old_column[index].pop('_reserved', False)
        else:
            reserved = None

        if action in ('add', 'delete') or (index>=0 and old_column[index] != column):
            #if not published, then directly use current record
            if obj.status == '1':
                data = obj.to_dict()
                data.pop('id')
                data.pop('create_time')
                data['status'] = '0'
                obj = self.model_his(**data)
                obj.uuid = get_uuid()[:6]

            if list_columns:
                if action == 'add':
                    old_column.append(column)
                elif action == 'edit':
                    column['_reserved'] = reserved
                    old_column[index] = column
                else:
                    del old_column[index]
            else:
                old_column = column

            setattr(obj, column_name, old_column)
            obj.save(version=True)
            uuid = obj.uuid
        return json({'success':True, 'message':'Success!', 'data':{'uuid':uuid}})

    def publish(self, model_name):
        from uliweb.utils import date
        from uliweb.orm import Begin, Commit, Rollback

        Begin()
        uuid = request.GET.get('uuid')
        obj = self._get_model(model_name, uuid)
        if not obj:
            return json({'success':False, 'message':"Model %s(%s) can't be found" % (model_name, uuid)})
        obj.status = '1'
        obj.published_time = date.now()
        if len(obj.extension_fields) > 0:
            obj.has_extension = True
        obj.save(version=True)

        row = self.model.get(self.model.c.model_name==model_name)
        row.uuid = uuid
        row.published_time = date.now()
        row.modified_user = request.user.id
        row.modified_time = obj.published_time
        row.display_name = obj.display_name
        row.description = obj.description
        row.save(version=True)

        try:
            M = functions.get_model(model_name)
            M.migrate()
            if obj.has_extension:
                M.ext._model.migrate()
            Commit()

        except Exception as e:
            Rollback()
            log.exception(e)
            return json({'success':False, 'message':'Migrate Model %s(%s) Failed!' % (model_name, uuid)})
        return json({'success':True, 'message':'Model %s(%s) has been published successfully!' % (model_name, uuid)})

    def unpublish(self, model_name):
        count = self.model_his.filter(self.model_his.c.model_name==model_name).count()
        if count <= 1:
            return json({'success':False, 'message':'There should be at lastest one version existed'})
        row = self.model.get(self.model.c.model_name==model_name)
        row.uuid = ''
        row.published_time = None
        row.save(version=True)
        return json({'success':True})

    def delete(self, model_name):
        row = self.model.get(self.model.c.model_name==model_name)
        row.delete()

        for obj in self.model_his.filter(self.model_his.c.model_name==model_name):
            obj.delete()
        return json({'success':True})

    def delete_version(self, model_name):
        uuid = request.GET.get('uuid')
        row = self.model.get(self.model.c.model_name==model_name)

        version = self._get_model(model_name, uuid)
        if version.uuid != row.uuid:
            version.delete()
        else:
            return json({'success':False, 'message':"You can't delete published version"})

        return json({'success':True})
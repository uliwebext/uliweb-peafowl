#coding=utf-8
from uliweb import expose, functions

@expose('/admin/menus')
class AdminMenusView(object):
    def __begin__(self):
        functions.require_login_admin()

    def __init__(self):
        self.menus_category = functions.get_model('admin_menus_category')
        self.menus = functions.get_model('admin_menus')

    @expose('')
    def index(self):
        categories = []
        for c in self.menus_category.all():
            categories.append(c.to_dict())
        return {'categories':categories}

    def _get_layout(self):
        return {
            'rows':
                [
                    [{'name':'title', 'attrs':{'placeholder':'Title'}},
                    {'name':'key', 'attrs':{'placeholder':'Menu ID'}}],
                ],
        }

    def _get_rules(self):
        return {
            'title':{
                'required':True,
            },
            'key':{
                'required':True,
            },
        }

    @expose('add_category', name='add_category')
    def add_category(self):
        response.template = 'utils/inc_addview.html'
        layout = self._get_layout()
        rules = self._get_rules()

        def success_data(obj, data):
            return obj.to_dict()

        view = functions.AddView(self.menus_category, layout_class='bs3v',
                                 layout=layout, rules=rules,
                                 success_data=success_data)
        return view.run(json_result=True)

    @expose('edit_category/<id>', name='edit_category')
    def edit_category(self, id):
        obj = self.menus_category.get(int(id))
        response.template = 'utils/inc_addview.html'
        layout = self._get_layout()
        rules = self._get_rules()

        def success_data(obj, data):
            return obj.to_dict()

        view = functions.EditView(self.menus_category, obj=obj,
                                 layout_class='bs3v',
                                 layout=layout, rules=rules,
                                 success_data=success_data)
        return view.run(json_result=True)

    @expose('remove_category/<id>', name='remove_category')
    def remove_category(self, id):
        obj = self.menus_category.get(int(id))
        view = functions.DeleteView(self.menus_category, obj=obj)
        return view.run(json_result=True)
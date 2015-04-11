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

    @expose('add_category', name='add_category')
    def add_category(self):
        response.template = 'utils/inc_addview.html'
        layout = {
            'rows':
                [
                    [{'name':'title', 'attrs':{'placeholder':'Title'}},
                    {'name':'key', 'attrs':{'placeholder':'Menu ID'}}],
                ],
        }
        rules = {
            'title':{
                'required':True,
            },
            'key':{
                'required':True,
            },
        }

        def success_data(obj, data):
            return obj.to_dict()

        view = functions.AddView(self.menus_category, layout_class='bs3v',
                                 layout=layout, rules=rules,
                                 success_data=success_data)
        return view.run(json_result=True)

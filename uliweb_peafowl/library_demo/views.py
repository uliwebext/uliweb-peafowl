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

    def _make_form(self):
        f = {
            'fields':[
                {'name':'str', 'type':'str', 'label':'String', 'required':True},
                {'name':'password', 'type':'password', 'label':'Password'},
                {'name':'hidden', 'type':'hidden', 'label':'Hidden'},
                {'name':'int', 'type':'int', 'label':'Integer'},
                {'name':'float', 'type':'float', 'label':'Float'},
                {'name':'bool', 'type':'bool', 'label':'Bool'},
                {'name':'bool1', 'type':'bool', 'label':'Bool'},
                {'name':'date', 'type':'date', 'label':'Date'},
                {'name':'datetime', 'type':'datetime', 'label':'Datetime'},
                {'name':'time', 'type':'time', 'label':'Time'},
                {'name':'list', 'type':'list', 'label':'List'},
                {'name':'select1', 'type':'select', 'label':'Single Select', 'choices':[('F', 'Female'), ('M', 'Male')]},
                {'name':'select2', 'type':'select', 'label':'Multiple Select', 'choices':[('F', 'Female'), ('M', 'Male')], 'multiple':True},
                {'name':'file', 'type':'file', 'label':'File'},
                {'name':'image', 'type':'image', 'label':'Image'},
                {'name':'radios1', 'type':'radios', 'label':'Sex',
                    'choices':[('F', 'Female'), ('M', 'Male')]},
                {'name':'radios2', 'type':'radios', 'label':'Sex',
                    'choices':[('F', 'Female'), ('M', 'Male')], 'inline':True},
                {'name':'checkboxes1', 'type':'checkboxes', 'label':'Sex',
                    'choices':[('F', 'Female'), ('M', 'Male')]},
                {'name':'checkboxes2', 'type':'checkboxes', 'label':'Sex',
                    'choices':[('F', 'Female'), ('M', 'Male')], 'inline':True},
                {'name':'lines', 'type':'lines', 'label':'Lines'},
                {'name':'desc', 'type':'text', 'label':'Description'},
            ],
            'layout_class':'bs3',
            'layout':{},
        }
        return f

    def _make_data(self):
        from uliweb.utils import date

        return {
            'str':'string',
            'password':'password',
            # 'hidden':'hidden',
            'int':10,
            'float':1.0,
            'bool':True,
            'date':date.to_date('2010-10-12'),
            'desc':'<p>abc</p><p>cde</p>',

        }

    def _run_form(self, form, menu_id, desc):
        from uliweb import request

        result = {
            'form':form,
            'menu_id':menu_id,
            'desc':desc,
            'success':None
        }
        if request.method == 'GET':
            return result
        else:
            if form.validate(request.values, request.files):
                result['success'] = 'success'
                print '====== form =', form.data, form.errors
                return result
            else:
                result['success'] = 'error'
                return result

    def bs3vform(self):
        from uliweb.form import make_form


        f = self._make_form()
        form_cls = make_form(**f)
        form = form_cls()

        response.template = 'LibraryDemoView/bs3form.html'
        return self._run_form(form, 'vform', 'Vertical form')

    def bs3hform(self):
        from uliweb.form import make_form


        f = self._make_form()
        f['layout_class'] = 'bs3h'
        form_cls = make_form(**f)
        form = form_cls()

        response.template = 'LibraryDemoView/bs3form.html'
        return self._run_form(form, 'hform', 'Horizontal form')


    def _get_layout(self):
        return [
            '-- Basic --',

            ['str', 'password'],
            ['int', 'float'],

            '-- Extend --',

            ['bool', {'name':'bool1', 'inline':True}],
            ['date', 'datetime', 'time'],

            [{'name':'list'}, {'name':'select1', 'colspan':2}],
            {'name':'select2'},

            ['file', 'image'],
            ['radios1', 'checkboxes1'],
            ['radios2', 'checkboxes2'],
            'lines',
            'desc'
        ]

    def _get_layout2(self):
        return [
            '-- Basic --',

            ['str', 'password'],
            ['int', 'float'],

            '-- Extend --',

            ['bool', 'date'],
            ['datetime', 'time'],

            ['list', 'select1'],
            {'name':'select2'},

            ['file', 'image'],
            ['radios1', 'checkboxes1'],
            ['radios2', 'checkboxes2'],
            'lines',
            'desc'
        ]

    def bs3layout(self):
        from uliweb.form import make_form


        f = self._make_form()
        f['layout_class'] = 'bs3'
        f['layout']['rows'] = self._get_layout()
        form_cls = make_form(**f)
        form = form_cls()

        response.template = 'LibraryDemoView/bs3form.html'
        return self._run_form(form, 'form_layout', 'Form Layout')

    def bs3tlayout(self):
        from uliweb.form import make_form


        f = self._make_form()
        f['layout_class'] = 'bs3table'
        f['layout']['rows'] = self._get_layout2()
        f['layout']['readonly'] = False
        form_cls = make_form(**f)

        data = self._make_data()
        form = form_cls(data=data)

        response.template = 'LibraryDemoView/bs3form.html'
        return self._run_form(form, 'form_tlayout', 'Form Table Layout')

    def bs3tlayout_readonly(self):
        from uliweb.form import make_form


        f = self._make_form()
        f['layout_class'] = 'bs3table'
        f['layout']['rows'] = self._get_layout2()
        f['layout']['readonly'] = True
        form_cls = make_form(**f)

        data = self._make_data()
        form = form_cls(data=data)

        response.template = 'LibraryDemoView/bs3form.html'
        return self._run_form(form, 'form_tlayout_readonly', 'Form Table Layout Readonly')

    def bs3layout2(self):
        from uliweb.form import make_form


        f = self._make_form()
        f['layout_class'] = 'bs3'
        f['layout']['rows'] = [
            ['str', 'password'],
            ['str', {'name':'password',
                     'cols':[{'name':'password', 'attrs':{'style':'display:table-cell;padding-right:60px;'}},
                                                '<a href="#" style="display:table-cell;position:absolute;right:20px;top:30px;">Forget</a>']},
            ],
            [{'name':'amount', 'label':'<label class="" for="exampleInputAmount">.</label>',
              'cols':"""
    <div class="input-group">
      <div class="input-group-addon">$</div>
      <input type="text" class="form-control" id="exampleInputAmount" placeholder="Amount">
      <div class="input-group-addon">.00</div>
    </div>"""}, {'name':'password', 'attrs':{'disabled':True}}
            ],
        ]
        form_cls = make_form(**f)
        form = form_cls()

        response.template = 'LibraryDemoView/bs3form.html'
        return self._run_form(form, 'form_layout', 'Form Layout')

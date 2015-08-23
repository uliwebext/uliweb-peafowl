#coding=utf-8
from uliweb import expose, functions

@expose('/library_demo')
class LibraryDemoView(object):
    def bootstrap3dialog(self):
        return {}

    def iconsheet(self):
        return {}

    def toastr(self):
        return {}

    def webui_popover(self):
        return {}

    def mmgrid(self):
        return {}

    def webui_popover_dialog(self):
        import uliweb.form as form
        class MyForm(form.Form):
            layout_class = 'bs3h'

            name = form.StringField('String', required=True)

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
                {'name':'str', 'type':'str', 'label':'String', 'required':True, 'help_string':'help string', 'placeholder':'string'},
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
                    'choices':[('F', 'Female'), ('M', 'Male')]},
                {'name':'checkboxes1', 'type':'checkboxes', 'label':'Sex',
                    'choices':[('F', 'Female'), ('M', 'Male')]},
                {'name':'checkboxes2', 'type':'checkboxes', 'label':'Sex',
                    'choices':[('F', 'Female'), ('M', 'Male')]},
                {'name':'lines', 'type':'lines', 'label':'Lines'},
                {'name':'desc', 'type':'text', 'label':'Description'},
            ],
            'layout_class':'bs3v',
            'layout':{
                'fields': {
                    'radios2':{'inline':True},
                    'checkboxes2':{'inline':True},
                    'bool1':{'inline':True, 'label':''},
                    'int':{'format':lambda x, all:20},
                },

            },
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
            'list':[u'中', u'文'],
            'select1':'F',
            'select2':['F', 'M'],
            'radios1':'F',
            'radios2':'M',
            'checkboxes1':['F'],
            'checkboxes2':['F', 'M'],
            'date':date.to_date('2010-10-12'),
            'datetime':date.to_datetime('2010-10-12 13:23:45'),
            'time':date.to_time('13:23:45'),

            'desc':'<p>abc</p><p>cde</p>',

        }

    def _run_form(self, form, menu_id, desc, ajax=False):
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
                if ajax:
                    return json({'success':True})
                else:
                    return result
            else:
                print '====== errors =', form.errors
                if ajax:
                    return json({'success':False, 'errors':form.errors})
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

            ['bool', {'name':'bool1', 'inline':True, 'label':''}],
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

            ['bool', {'name':'bool1', 'inline':True, 'label':''}],
            ['date', 'datetime', 'time'],

            [{'name':'list'}, {'name':'select1', 'colspan':2}],
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
        f['layout_class'] = 'bs3v'
        f['layout']['rows'] = self._get_layout()
        form_cls = make_form(**f)
        form = form_cls()

        response.template = 'LibraryDemoView/bs3form.html'
        return self._run_form(form, 'form_layout', 'Form Layout')

    def bs3tlayout(self):
        from uliweb.form import make_form


        f = self._make_form()
        f['layout_class'] = 'bs3t'
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
        f['layout_class'] = 'bs3t'
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
        f['layout_class'] = 'bs3v'
        f['layout']['rows'] = [
            ['str', {'name':'password',
                     'cols':[{'name':'password', 'attrs':{'style':'display:initial;'},
                                'wrap':['<div style="display:table-cell;margin-right:10px;width:1000px;">', '</div>']},
                                '<a href="#" style="display:table-cell;padding-left:10px;">Forget</a>'],
                    },
            ],
            ['str', {'name':'password',
                     'label':'<label>Password:</label>',
                     'cols':'''<div style="display:table-row">
                     <div style='display:table-cell;margin-right:10px;width:1000px;'>
                        <input class='form-control' type="password" value="" id="field_password" name="password" style="width:100%;height:34px;" widget="password">
                     </div>
                     <a href='#' style="display:table-cell;padding-left:10px;">Forget</a>
                     </div>'''
                    },
            ],
            [{'name':'amount', 'label':'<label class="" for="exampleInputAmount">.</label>',
              'cols':"""
    <div class="input-group">
      <div class="input-group-addon">$</div>
      <input type="text" class="form-control" id="exampleInputAmount" placeholder="Amount">
      <div class="input-group-addon">.00</div>
    </div>"""}, {'name':'password', 'attrs':{'disabled':True}}
            ],
            [{'name':'str', 'build':'inputgroup', 'attrs':{'before':'<input type="checkbox">'}},
             {'name':'str', 'build':'inputgroup', 'attrs':{'after':'@gmail.com'}}
             ],
            [{'name':'str', 'build':'inputbtn', 'attrs':{'before':'<button class="btn btn-default" type="button">Go!</button>'}},
             {'name':'str', 'build':'inputbtn', 'attrs':{'after':'<button class="btn btn-default" type="button">Go!</button>'}}
             ],
            [{'name':'str', 'build':'inputbtn', 'attrs':{'before':'''
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">Action <span class="caret"></span></button>
        <ul class="dropdown-menu" role="menu">
          <li><a href="#">Action</a></li>
          <li><a href="#">Another action</a></li>
          <li><a href="#">Something else here</a></li>
          <li class="divider"></li>
          <li><a href="#">Separated link</a></li>
        </ul>'''}},
             {'name':'str', 'build':'inputbtn', 'attrs':{'after':'''
                     <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">Action <span class="caret"></span></button>
        <ul class="dropdown-menu dropdown-menu-right" role="menu">
          <li><a href="#">Action</a></li>
          <li><a href="#">Another action</a></li>
          <li><a href="#">Something else here</a></li>
          <li class="divider"></li>
          <li><a href="#">Separated link</a></li>
        </ul>'''}}
             ],
        ]
        form_cls = make_form(**f)
        form = form_cls()

        response.template = 'LibraryDemoView/bs3form.html'
        return self._run_form(form, 'form_layout2', 'Form Layout')

    def get_login_form(self):
        f = {
            'fields':[
                {'name':'username', 'type':'str', 'label':u'用户名', 'placeholder':u'用户名'},
                {'name':'password', 'type':'password', 'label':u'密码', 'placeholder':u'密码'},
                {'name':'remember_me', 'type':'bool', 'label':u'记住我'},
            ],
            'layout_class':'bs3h',
            'layout':{
                'label_width':3,
                'rows':[
                    'username',
                    'password',
                    {'name':'remember_me', 'inline':True, 'label':''},
                ],
                'buttons':[u'<button type="submit" class="btn btn-primary">提交</button>',
                           '<a href="#">忘记密码</a>'],
            },
            'rules':{
                'username':{
                    'required':True,
                    'minlength:end':6,
                },
                'password':{
                    'required':True,
                }
            },

        }

        return f

    def bs3login(self):
        from uliweb.form import make_form

        f = self.get_login_form()
        form_cls = make_form(**f)
        form = form_cls(id='login_form')

        return self._run_form(form, 'form_login', 'Form Login')

    def bs3login_ajax(self):
        from uliweb.form import make_form

        f = self.get_login_form()
        form_cls = make_form(**f)
        form = form_cls(id='login_form')

        return self._run_form(form, 'form_login_ajax', 'Form Login Ajax', ajax=True)

    def bs3tlayout_widgets(self):
        from uliweb.form import make_form


        f = self._make_form()
        f['layout_class'] = 'bs3t'
        f['layout']['rows'] = self._get_layout2()
        f['layout']['readonly'] = False
        f['layout']['fields']['date'] = {'attrs':{'options':{
                'dateFormat':
                    'yy-mm-dd'}}}
        # f['layout']['fields']['select1'] = {'widget':'select2'}
        # f['layout']['fields']['select2'] = {'widget':'select2'}
        # f['layout']['fields']['file'] = {'widget':'filestyle', 'attrs':{
        #     'options':{'buttonText':'', 'buttonName':'btn-primary'}}}
        # f['layout']['fields']['image'] = {'widget':'filestyle', 'attrs':{
        #     'options':{'buttonText':'', 'buttonName':'btn-success       ',
        #                'iconName':'glyphicon-picture'}}}
        form_cls = make_form(**f)

        data = self._make_data()
        form = form_cls(data=data)

        response.template = 'LibraryDemoView/bs3form_widgets.html'
        return self._run_form(form, 'form_tlayout_widgets', 'Form Widgets')


    def _make_js_form_data(self):
        return {
            'attrs': {'id':'test_form', 'method':'GET'},
            'fields':[
                {'name':'username', 'type':'str', 'label':'用户名',
                    'placeholder':'用户名', 'help_string':'请输入用户名，长度不少于6个字符'},
                {'name':'password', 'type':'password', 'label':'密码', 'placeholder':'密码'},
                {'name':'remember_me', 'type':'bool', 'label':'记住我'},
                {'name':'hidden', 'type':'hidden'},
                {'name':'file', 'type':'file', 'label':'文件'},
                {'name':'text', 'type':'text', 'label':'内容'},
                {'name':'select', 'type':'select', 'label':'多选',
                    'choices':[('0', '中文'), ('1', '英文')], 'multiple':True},
                {'name':'static', 'type':'str', 'label':'静态字段', 'static':True},
                {'name':'date', 'type':'date', 'label':'日期'},
                {'name':'datetime', 'type':'datetime', 'label':'日期时间'},
                {'name':'radios1', 'type':'radios', 'label':'单选',
                    'choices':[('0', '中文'), ('1', '英文')]},
                {'name':'radios2', 'type':'radios', 'label':'行内单选',
                    'choices':[('0', '中文'), ('1', '英文')], 'inline':True},

                {'name':'checkboxes1', 'type':'checkboxes', 'label':'多选',
                    'choices':[('0', '中文'), ('1', '英文')]},
                {'name':'checkboxes2', 'type':'checkboxes', 'label':'行内多选',
                    'choices':[('0', '中文'), ('1', '英文')], 'inline':True},
            ],
            'layout_type':'bs3t',
            'layout':{
                'label_width':3,
                'button_offset': '155px',
                'fields':[
                    {'name':'remember_me', 'inline':True, 'hide_label':True}
                ],
                'rows':[
                    '-- Basic --',
                    ['username', 'password'],
                    ['remember_me', 'file'],
                    '-- Extend --',
                    'text',
                    ['select', 'static'],
                    ['date', 'datetime'],
                    ['radios1', 'radios2'],
                    ['checkboxes1', 'checkboxes2']
                ],
                'buttons':[
                    {
                        'id':'btnSubmit',
                        'type':'submit',
                        'class':'btn btn-primary btn-sm',
                        'text':'提交'
                    },
                    ' <a href="#">忘记密码</a>'
                ]
            },
            'rules':{
                'username':{
                    'required':True,
                    'minlength':6,
                },
                'password':{
                    'required':True,
                }
            },
            'data': {
                #username: 'hello',
                'password': 'password',
                'remember_me': True,
                'hidden': 'hidden',
                'file': 'file.csv',
                'text': '<h1>This is Header</h1><p>Content</p>',
                'select': ['0', '1'],
                'static': '这是静态字段',
                'radios1': '0',
                'radios2': '1',
                'checkboxes1': ['0', '1'],
                'checkboxes2': ['0', '1'],
                'date': '2015-04-15',
                'datetime': '2015-04-15 12:12:12'
            }
        }

    def bs3jsform(self):
        result = {
            'menu_id':'form_js',
            'desc':'js form builder',
            'success':None,
            'form': self._make_js_form_data()
        }
        return result

    def bs3jsform_readonly(self):
        f = self._make_js_form_data()
        f['readonly'] = True

        result = {
            'menu_id':'form_js_readonly',
            'desc':'js form builder',
            'success':None,
            'form': f
        }
        return result
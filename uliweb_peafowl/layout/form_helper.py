import copy
from uliweb.core.html import Buf, Tag, Div, to_attrs
from uliweb.form.layout import Layout
from uliweb.utils.common import safe_str

class Bootstrap3_Build(object):
    input_type = 'text'
    input_class = 'form-control'

    def __init__(self, form, field, attrs=None, label_width=0, inline=False,
                 dir='v', **kwargs):
        assert 0 <= label_width <= 12

        attrs = attrs or {}
        self.form = form
        if isinstance(field, (str, unicode)):
            fieldname = field
            self.field = getattr(form.__class__, fieldname)
        else:
            fieldname = field.name
            self.field = field

        self.attrs = _attrs = field.html_attrs.copy()
        _attrs.update(attrs)
        if 'id' not in _attrs:
            _attrs['id'] = field.id
        _attrs['name'] = fieldname
        _attrs['class'] = (_attrs.setdefault('class', '') + ' %s' % self.input_class).strip()
        _attrs['widget'] = _attrs.get('widget') or field.type_name

        self.label_width = label_width
        self.kwargs = kwargs
        self.inline = inline
        self.dir = dir
        self._label = kwargs.pop('label', field.label)
        self.table_cell = kwargs.pop('table_cell', None)
        self.wrap = kwargs.get('wrap')

        if form.ok:
            self.value = self.form.data.get(fieldname, '')
            self.html_value = field.to_html(self.value)
        else:
            self.value = self.form.data.get(fieldname, '')
            self.html_value = self.value

        if self.table_cell:
            self.label = field.get_label(self._label, _class="table-field-label")
        else:
            #horizontal
            if self._label:
                if dir == 'v':
                    self.label = field.get_label(self._label)
                else:
                    self.label = field.get_label(self._label, _class="col-sm-%d control-label" % label_width)
            else:
                self.label = self._label
        self.content = self.to_html()
        if self.wrap:
            self.content = self.wrap[0] + self.content + self.wrap[1]

    def html(self):
        return self.label + self.content

    def to_html(self):
        if self.field.static:
            return self.to_static()
        else:
            return self.to_widget()

    def to_widget(self):
        _attrs = to_attrs(self.attrs)
        return '<input type="%s" value="%s"%s></input>' % (self.input_type, safe_str(self.html_value), _attrs)

    def to_hidden(self):
        return '<input type="hidden" value="%s"></input>' % safe_str(self.html_value)

    def to_static(self):
        cls = ''
        if self.table_cell:
            cls = ' table-field-content'
        return '<div class="form-control-static%s">%s</div>' % (cls, self.get_static_value())

    def get_static_value(self):
        value = self.value
        f = self.kwargs.get('format', value)
        if callable(f):
            _value = f(value, self.form.data)
        else:
            _value = self.convert_html(value)
        return _value

    def get_help_string(self):
        help_string = self.kwargs.get('help_string', '')
        if not help_string and self.field and self.field.help_string:
            help_string = self.field.help_string
        if help_string:
            return '<p class="help-block">%s</p>' % help_string
        else:
            return ''

    def convert_html(self, value):
        if isinstance(value, (tuple, list)):
            return ' '.join(['<span class="label label-default">%s</span>' % safe_str(x)
                             for x in value])

        return self.field.to_html(value)

class Bootstrap3_Column(Bootstrap3_Build):
    def __init__(self, layout, form, col, label_width=0, dir='v', table_cell=False):
        """
        col should be html, fieldname, dict = {'name':'fieldname', 'label':, 'cols':}
        """
        self.layout = layout
        self.form = form
        self.label_width = label_width
        self.dir = dir
        self.field = None
        self.error = False
        self.label = ''
        self.kwargs = {}
        self.table_cell = table_cell

        if isinstance(col, (str, unicode)):
            if not col in self.form.fields:
                self.content = col
                self.name = ''
                self.label = ''
            else:
                kwargs = copy.deepcopy(self.layout.get('fields', {}).get(col, {}))
                self.kwargs = kwargs
                self.field = field = self.form.fields[col]
                build = self.get_build(form, field, label_width=label_width, dir=self.dir,
                                       table_cell=table_cell, **kwargs)
                self.content = build.content
                self.name = field.name
                self.label = build.label
        elif isinstance(col, dict):
            self.name = col['name']
            kwargs = copy.deepcopy(self.layout.get('fields', {}).get(self.name, col))
            cols = kwargs.pop('cols', [])
            kwargs.update(col)
            self.kwargs = kwargs
            wrap = kwargs.get('wrap')

            if not isinstance(cols, (tuple, list)):
                cols = [cols]
            if not cols:
                self.field = field = self.form.fields[self.name]
                build = self.get_build(form, field, label_width=label_width, dir=self.dir,
                                       table_cell=table_cell, **kwargs)
                self.content = build.content
                self.label = kwargs.get('label', build.label)
            else:
                result = []
                for c in cols:
                    b = self.__class__(self.layout, form, c, label_width=label_width, dir=self.dir,
                                       table_cell=table_cell)
                    result.append(b.content)
                    if b.name == self.name:
                        self.label = b.label
                        self.field = b.field
                self.content = ''.join(result)
                if wrap:
                    self.content = wrap[0] + self.content + wrap[1]

        if self.field:
            self.error_msg = self.form.errors.get(self.field.name, '')
            if self.error_msg and layout['error']:
                self.error = True

        if not self.label:
            self.label = self.kwargs.get('label', '')

    def get_build(self, form, field, label_width, **kwargs):
        build_type = kwargs.get('build', fields_mapping[field.type_name])
        build_cls = builders[build_type]
        build = build_cls(form, field, label_width=label_width, **kwargs)
        return build

    def html(self):
        if self.table_cell:
            return ('<div class="table-field-row">' + self.label +
                    '<div class="table-field-col">' + self.content + '</div></div>')

        col_cls = 'form-group'
        if self.error:
            col_cls = col_cls + ' has-error'
        if self.name:
            _id = 'div_field_%s' % self.name
        else:
            _id = None

        buf = Buf()
        with buf.div(_class=col_cls, id=_id):
            buf << self.label
            if self.dir == 'h':
                if self.label:
                    buf << '<div class="col-sm-%d">' % (12-self.label_width)
                else:
                    buf << '<div class="col-sm-offset-%d col-sm-%d">' % (self.label_width,
                                                                         12-self.label_width)
            # buf << '<div class="table-field-row">'
            buf << self.content
            # buf << '</div>'
            buf << self.get_help_string()
            if self.error:
                buf << self.get_error()
            if self.dir == 'h':
                buf << '</div>'

        return str(buf)

    def get_error(self):
        if self.error_msg:
            return '<p class="error-message help-block">%s</p>' % self.error_msg
        else:
            return ''

Bootstrap3_String = Bootstrap3_Build
class Bootstrap3_Text(Bootstrap3_Build):

    def to_widget(self):
        self.attrs['rows'] = getattr(self.field, 'rows', 4)
        _attrs = to_attrs(self.attrs)
        return '<textarea%s>%s</textarea>' % (_attrs, self.html_value)

Bootstrap3_Lines = Bootstrap3_Text

class Bootstrap3_Password(Bootstrap3_Build):
    input_type = 'password'

class Bootstrap3_Hidden(Bootstrap3_Build):
    input_type = 'hidden'

class Bootstrap3_File(Bootstrap3_Build):
    input_type = 'file'

class Bootstrap3_Checkbox(Bootstrap3_Build):
    input_type = 'checkbox'

    def to_widget(self):
        value = self.html_value
        field = self.field
        attrs = self.attrs

        if value:
            attrs['checked'] = None
        if self.inline:
            attrs.pop('class', None)
            _attrs = to_attrs(attrs)
            return '<label class="checkbox-inline"><input type="checkbox"%s></input> %s</label>' % (_attrs, self.field.label)
        else:
            attrs['class'] = 'checkbox'
            _attrs = to_attrs(attrs)
            return '<input type="%s" %s></input>' % (self.input_type, _attrs)

    def convert_html(self, value):
        if value:
            cls = 'glyphicon glyphicon-ok'
        else:
            cls = 'glyphicon glyphicon-remove'
        return '<i class="%s"></i>' % cls


class Bootstrap3_Select(Bootstrap3_Build):

    def to_widget(self):
        from uliweb.form.widgets import Select

        field = self.field
        attrs = self.attrs

        choices = field.get_choices()[:]
        if (field.empty is not None) and (not field.multiple):
            group = False
            if choices:
                if len(choices[0]) > 2:
                    group = True
                    c = [(x[1], x[2]) for x in choices]
                else:
                    c = choices
                if (not field.default in dict(c)):
                    if group:
                        choices.insert(0, (choices[0][0], '', field.empty))
                    else:
                        choices.insert(0, ('', field.empty))

        return str(Select(choices, self.form.data.get(field.name), multiple=field.multiple, size=field.size, **attrs))

    def convert_html(self, value):
        r = []
        for v, x in self.field.get_choices():
            if self.field.multiple:
                if v in value:
                    r.append(x)
            else:
                if v == value:
                    return x
        return ' '.join(['<span class="label label-default">%s</span>' % x for x in r])

class Bootstrap3_Radios(Bootstrap3_Select):
    input_type = 'radio'

    def to_widget(self):
        """
        """
        from uliweb.form.widgets import Select
        from uliweb.utils.common import safe_str

        field = self.field
        attrs = self.attrs

        buf = Buf()
        _value = [safe_str(x) for x in (self.form.data.get(field.name) or [])]
        for i, (v, title) in enumerate(field.get_choices()):
            _attrs = copy.deepcopy(attrs)
            if safe_str(v) in _value:
                _attrs['checked'] = None
            _attrs.pop('class', None)
            _attrs['id'] = _attrs['id'] + '_' + str(i+1)
            v_attrs = to_attrs(_attrs)
            if self.inline:
                buf << '<label class="%s-inline"><input type="%s" value="%s"%s> %s</label>' % (self.input_type,
                                            self.input_type, v, v_attrs, title)
            else:
                buf << '<div class="%s"><label><input type="%s" value="%s"%s>%s</label></div>' % (self.input_type,
                                            self.input_type, v, v_attrs, title)
        return str(buf)

class Bootstrap3_Checkboxes(Bootstrap3_Radios):
    input_type = 'checkbox'

class Bootstrap3_InputGroup(Bootstrap3_String):
    '''
    attrs:
        'class': will be used in div
        'before': will be added in front of widget
        'after': will be added after widget
    '''

    input_class = ''

    def to_widget(self):
        d = {}
        _attrs = copy.deepcopy(self.attrs)
        d['class'] = _attrs.pop('class', '')
        d['attrs'] = to_attrs(_attrs)
        d['before'] = b = _attrs.pop('before', '')
        if b:
            d['before'] = '<div class="input-group-addon">%s</div>' % b
        d['after'] = a = _attrs.pop('after', '')
        if a:
            d['after'] = '<div class="input-group-addon">%s</div>' % a
        return """<div class="input-group %(class)s">
  %(before)s
  <input type="text" class="form-control" %(attrs)s>
  %(after)s
</div>""" % d

class Bootstrap3_InputBtn(Bootstrap3_String):
    '''
    attrs:
        'class': will be used in div
        'before': will be added in front of widget
        'after': will be added after widget
    '''

    input_class = ''

    def to_widget(self):
        d = {}
        _attrs = copy.deepcopy(self.attrs)
        d['class'] = _attrs.pop('class', '')
        d['attrs'] = to_attrs(_attrs)
        d['before'] = b = _attrs.pop('before', '')
        if b:
            d['before'] = '<span class="input-group-btn">%s</span>' % b
        d['after'] = a = _attrs.pop('after', '')
        if a:
            d['after'] = '<span class="input-group-btn">%s</span>' % a
        return """<div class="input-group %(class)s">
  %(before)s
  <input type="text" class="form-control" %(attrs)s>
  %(after)s
</div>""" % d

fields_mapping = {
    'str':'str',
    'select':'select',
    'text':'text',
    'unicode':'str',
    'lines':'lines',
    'password':'password',
    'hidden':'hidden',
    'int':'str',
    'list':'str',
    'radios':'radios',
    'image':'file',
    'float':'str',
    'file':'file',
    'bool':'checkbox',
    'checkboxes':'checkboxes',
    'date':'str',
    'time':'str',
    'datetime':'str',
}

builders = {
    'str':Bootstrap3_String,
    'select':Bootstrap3_Select,
    'text':Bootstrap3_Text,
    'lines':Bootstrap3_Lines,
    'password':Bootstrap3_Password,
    'hidden':Bootstrap3_Hidden,
    'radios':Bootstrap3_Radios,
    'file':Bootstrap3_File,
    'checkbox':Bootstrap3_Checkbox,
    'checkboxes':Bootstrap3_Checkboxes,
    'inputgroup':Bootstrap3_InputGroup,
    'inputbtn':Bootstrap3_InputBtn,
}
class Bootstrap3VLayout(Layout):
    use_table = False
    dir = 'v'

    def init(self):
        if not self.layout:
            self.layout = {'rows':[name for name, obj in self.form.fields_list if not self.is_hidden(obj)]}
        elif isinstance(self.layout, list):
            self.layout = {'rows':self.layout}
        elif isinstance(self.layout, dict):
            if not self.layout.get('rows'):
                self.layout['rows'] = [name for name, obj in self.form.fields_list if not self.is_hidden(obj)]
        else:
            raise Exception("layout is not the right data type")

        self.label_width = 0

        #process readonly
        if self.layout.get('readonly'):
            for name, f in self.form.fields_list:
                f.static = True

        #process error display
        self.layout['error'] = self.layout.get('error', True)

    def begin(self):
        if not self.form.html_attrs['class'] and self.layout.get('form_class'):
            self.form.html_attrs['class'] = self.layout.get('form_class')
        self.form.html_attrs['role'] = 'form'
        return self.form.form_begin

    def line(self, line):
        result = []
        columns_num = len(line)
        total_width = 0
        for f in line:
            if isinstance(f, (str, unicode)):
                col = {'name':f}
            elif isinstance(f, dict):
                col = f
            elif isinstance(f, (tuple, list)):
                col = {'name':'', 'cols':f}
            else:
                raise Exception("layout line should be string, list or dict, but %r found" % f)
            width, r = self.process_column(col, columns_num)
            total_width += width
            result.append((width, r))

        b = Buf()
        if columns_num == 1:
            if self.use_table:
                with b.tr:
                    with b.td(colspan=12):
                        b << result[0][1]
            else:
                b << result[0][1]
        else:
            if self.use_table:
                with b.tr:
                    for width, r in result:
                        span = width * 12 / total_width
                        with b.td(colspan=span, width='%f%%' % (span *100.0/12)):
                            b << r
            else:
                with b.div(_class="row"):
                    for width, r in result:
                        col_cls = 'col-sm-%d' % (width * 12 / total_width)
                        with b.div(_class=col_cls):
                            b << r
        return str(b)

    def process_column(self, col, columns_num):
        col_width = col.pop('colspan', 1)
        build = Bootstrap3_Column(self.layout, self.form, col, label_width=self.label_width,
                                  dir=self.dir, table_cell=self.use_table)
        return col_width*12/columns_num, build.html()

    def buttons(self):
        buttons = self.layout.get('buttons', self.form.get_buttons())
        return ' '.join([str(x) for x in buttons])

    def buttons_line(self):
        buttons = self.layout.get('buttons', self.form.get_buttons())
        button_offset = self.layout.get('button_offset', self.label_width)
        buf = Div(_class='form-group')
        if button_offset:
            with buf:
                with buf.div(_class="col-sm-offset-%d col-sm-%d" % (button_offset, 12-button_offset)):
                    buf << buttons
        else:
            with buf:
                buf << buttons
        return str(buf)

    def body(self):
        buf = Buf()
        self.process_layout(buf)
        return str(buf)

    def process_layout(self, buf):
        """
        Layout format should be:
        [
            #if one column should be:
            [['one_column']]
            'one_column'
            {'name':'column_name'},
            [[{'name':'column_name'}]],
            [['one_column', 'others']]

            #if multi column should be:
            ['column_one', 'column_two']
            [['column_one', 'others'], 'column_two],
            [{'name':'column_one_name'}, [{'name:'column_two_name'}, 'others']],

            '-- fieldset legend --'
        ]
        """
        first = True
        fieldset = None
        title = None
        table = None
        table_class = self.layout.get('table_class', 'table table-bordered table-hover table-layout')
        for line in self.layout['rows']:
            if isinstance(line, (str, unicode)):
                #process fieldset title
                if line.startswith('--') and line.endswith('--'):
                    fieldset = True
                    title = line.strip('- ')
                    if first:
                        buf << '<fieldset><legend>%s</legend>' % title
                        first = False
                    else:
                        if self.use_table:
                            buf << '</table>'
                        buf << '</fieldset><fieldset><legend>%s</legend>' % title

                    if self.use_table:
                        buf << '<table class="%s">' % table_class
                        table = True

                #process line
                else:
                    if self.use_table and not table:
                        buf << '<table class="%s">' % table_class
                        table = True

                    _line = [line]
                    buf << self.line(_line)
            else:
                if isinstance(line, dict):
                    _line = [line]
                elif isinstance(line, (tuple, list)):
                    _line = line
                else:
                    raise Exception("Layout row should be str, dict, tuple, or list, but %r found" % line)
                buf << self.line(_line)

        if table:
            buf << '</table>'
        if fieldset:
            buf << '</fieldset>'


class Bootstrap3HLayout(Bootstrap3VLayout):
    dir = 'h'

    def init(self):
        super(Bootstrap3HLayout, self).init()
        self.label_width = self.layout.get('label_width', 2)

    def begin(self):
        if not self.form.html_attrs['class'] and self.layout.get('form_class'):
            self.form.html_attrs['class'] = self.layout.get('form_class')
        if 'form-horizontal' not in self.form.html_attrs['class']:
            self.form.html_attrs['class'] = (self.form.html_attrs['class'] + ' form-horizontal').lstrip()
        self.form.html_attrs['role'] = 'form'
        return self.form.form_begin

class Bootstrap3TLayout(Bootstrap3VLayout):
    use_table = True

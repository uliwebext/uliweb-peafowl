import copy
from uliweb.core.html import Buf, Tag, Div, to_attrs
from uliweb.form.layout import Layout

class Bootstrap3_Build(object):
    input_type = 'text'
    input_class = 'form-control'

    def html(self, form, field, attrs=None, label_width=0, **kwargs):
        """
        form is Form instance
        If label_width > 0, then the layout will be horizontal
        """
        assert 0 <= label_width <= 12

        attrs = copy.deepcopy(attrs or {})
        if isinstance(field, (str, unicode)):
            fieldname = field
            obj = getattr(form, fieldname)
            field = getattr(form.__class__, fieldname)
        else:
            fieldname = field.name
            obj = getattr(form, fieldname)

        if 'id' not in attrs:
            attrs['id'] = field.id
        attrs['name'] = fieldname
        attrs['class'] = (attrs.setdefault('class', '') + ' %s' % self.input_class).strip()
        attrs['widget'] = attrs.get('widget') or field.type_name

        if form.ok:
            value = field.to_html(obj.data)
        else:
            value = obj.data

        if not label_width:
            return self.default_html(form, field, obj, value, attrs, **kwargs)
        else:
            return self.default_horizontal_html(form, field, obj, value, attrs, label_width, **kwargs)

    def default_html(self, form, field, obj, value, attrs, **kwargs):
        return obj.label + self.to_html(form, field, obj, value, attrs, 0, **kwargs) + self.get_help_string(field)

    def default_horizontal_html(self, form, field, obj, value, attrs, label_width, **kwargs):
        return (field.get_label(_class="col-sm-%d control-label" % label_width) +
                '<div class="col-sm-%d">' % (12-label_width) +
                self.to_html(form, field, obj, value, attrs, label_width, **kwargs) + '</div>')

    def to_html(self, form, field, obj, value, attrs, label_width, **kwargs):
        if field.static:
            return self.to_static(form, field, obj, value, attrs, label_width, **kwargs)
        else:
            return self.to_widget(form, field, obj, value, attrs, label_width, **kwargs)

    def to_widget(self, form, field, obj, value, attrs, label_width, **kwargs):
        _attrs = to_attrs(attrs)
        return '<input type="%s" value="%s"%s></input>' % (self.input_type, value, _attrs)

    def to_hidden(self, form, field, obj, value, attrs, **kwargs):
        return '<input type="hidden" value="%s"></input>' % value

    def to_static(self, form, field, obj, value, attrs, label_width, **kwargs):
        return '<p class="form-control-static">%s</p>' % self.get_static_value(value, **kwargs)

    def get_static_value(self, value, **kwargs):
        static_value = kwargs.get('static_value', value)
        return static_value

    def get_help_string(self, field):
        if field.help_string:
            return '<p class="help-block">%s</p>' % field.help_string
        else:
            return ''

Bootstrap3_String = Bootstrap3_Build
class Bootstrap3_Text(Bootstrap3_Build):

    def to_widget(self, form, field, obj, value, attrs, label_width, **kwargs):
        attrs['rows'] = getattr(field, 'rows', 4)
        _attrs = to_attrs(attrs)
        return '<textarea%s>%s</textarea>' % (_attrs, value)

Bootstrap3_Lines = Bootstrap3_Text

class Bootstrap3_Password(Bootstrap3_Build):
    input_type = 'password'

class Bootstrap3_Hidden(Bootstrap3_Build):
    input_type = 'hidden'

class Bootstrap3_File(Bootstrap3_Build):
    input_type = 'file'

class Bootstrap3_Checkbox(Bootstrap3_Build):

    def to_widget(self, form, field, obj, value, attrs, label_width, **kwargs):
        if value:
            attrs['checked'] = None
        attrs.pop('class', None)
        _attrs = to_attrs(attrs)
        if label_width:
            return '<div class="checkbox"><input type="checkbox"%s></input></div>' % _attrs
        else:
            return '<input type="checkbox"%s>%s</input>' % (_attrs, kwargs.get('label') or field.label)

    def default_html(self, form, field, obj, value, attrs, **kwargs):
        widget = self.to_html(form, field, obj, value, attrs, 0)
        help_string = self.get_help_string(field)
        if field.static:
            return '<div class="checkbox">%s%s</div>' % (widget, help_string)
        else:
            return '<div class="checkbox"><label>%s</label>%s</div>' % (widget, help_string)

    def to_static(self, form, field, obj, value, attrs, label_width, **kwargs):
        staic_value = self.get_static_value(value, **kwargs)
        if label_width:
            return '<p class="form-control-static">%s</p>' % staic_value
        else:
            return '<p class="form-control-static">%s %s</p>' % (staic_value, field.label)

    def get_static_value(self, value, **kwargs):
        static_value = kwargs.get('static_value', None)
        if static_value:
            return static_value
        else:
            if value:
                cls = 'glyphicon glyphicon-check'
            else:
                cls = 'glyphicon glyphicon-unchecked'
        return '<i class="%s"></i>' % cls

class Bootstrap3_Select(Bootstrap3_Build):

    def to_widget(self, form, field, obj, value, attrs, label_width, **kwargs):
        from uliweb.form.widgets import Select

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

        return str(Select(choices, obj.data, multiple=field.multiple, size=field.size, **attrs))

class Bootstrap3_Radios(Bootstrap3_Build):
    input_type = 'radio'

    def to_widget(self, form, field, obj, value, attrs, label_width, **kwargs):
        """
        """
        from uliweb.form.widgets import Select
        from uliweb.utils.common import safe_str

        buf = Buf()
        _value = [safe_str(x) for x in obj.data or []]
        for i, (v, title) in enumerate(field.get_choices()):
            _attrs = copy.deepcopy(attrs)
            if safe_str(v) in _value:
                _attrs['checked'] = None
            _attrs.pop('class', None)
            _attrs['id'] = _attrs['id'] + '_' + str(i+1)
            v_attrs = to_attrs(_attrs)
            if field.inline:
                buf << '<label class="%s-inline"><input type="%s" value="%s"%s> %s</label>' % (self.input_type,
                                            self.input_type, v, v_attrs, title)
            else:
                buf << '<div class="%s"><label><input type="%s" value="%s"%s>%s</label></div>' % (self.input_type,
                                            self.input_type, v, v_attrs, title)
        return str(buf)

class Bootstrap3_Checkboxes(Bootstrap3_Radios):
    input_type = 'checkbox'

fields_mapping = {
    'str':Bootstrap3_String,
    'select':Bootstrap3_Select,
    'text':Bootstrap3_Text,
    'unicode':Bootstrap3_String,
    'lines':Bootstrap3_Lines,
    'password':Bootstrap3_Password,
    'hidden':Bootstrap3_Hidden,
    'int':Bootstrap3_String,
    'list':Bootstrap3_String,
    'radios':Bootstrap3_Radios,
    'image':Bootstrap3_File,
    'float':Bootstrap3_String,
    'file':Bootstrap3_File,
    'bool':Bootstrap3_Checkbox,
    'checkboxes':Bootstrap3_Checkboxes,
    'date':Bootstrap3_String,
    'time':Bootstrap3_String,
    'datetime':Bootstrap3_String,
}
class Bootstrap3Layout(Layout):

    def init(self):
        if not self.layout:
            self.layout = {'rows':[name for name, obj in self.form.fields_list]}
        elif isinstance(self.layout, list):
            self.layout = {'rows':self.layout}
        elif isinstance(self.layout, dict):
            if not self.layout.get('rows'):
                self.layout['rows'] = [name for name, obj in self.form.fields_list]
        else:
            raise Exception("layout is not the right data type")

        self.label_width = 0

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
            if isinstance(f, (str, unicode, dict)):
                cols = [f]
            elif isinstance(f, (tuple, list)):
                cols = f
            else:
                raise Exception("layout line should be string, list or dict, but %r found" % f)
            width, r = self.process_column(cols, columns_num)
            total_width += width
            result.append((width, r))

        b = Buf()
        if columns_num == 1:
            b << result[0][1]
        else:
            with b.div(_class="row"):
                for width, r in result:
                    col_cls = 'col-sm-%d' % (width * 12 / total_width)
                    with b.div(_class=col_cls):
                        b << r
        return str(b)

    def get_build(self, field):
        return fields_mapping[field.type_name]()

    def process_column(self, cols, columns_num):
        r = []
        label_width = self.label_width
        error = False
        buf = Buf()
        obj = None
        for f in cols:
            col_width = 1
            if isinstance(f, (str, unicode)):
                if f not in self.form.fields:
                    r.append(f)
                    continue
                else:
                    name = f
                    kwargs = {}
            elif isinstance(f, dict):
                kwargs = f.copy()
                name = kwargs.pop('name')
                col_width = kwargs.pop('colspan', 1)
                #todo add text support
            else:
                raise Exception("Not support layout data type for %r" % f)

            field = self.form.fields[name]
            #first field will be obj, and the column id will be the first field object
            if not obj:
                obj = field
            if self.is_hidden(field):
                continue

            build = self.get_build(field)
            r.append(build.html(self.form, field, label_width=label_width, **kwargs))
            if name in self.form.errors:
                error = True
        col_cls = 'form-group'
        if error:
            col_cls = col_cls + ' has-error'
        if obj:
            _id = 'div_' + obj.id
        else:
            _id = None
        with buf.div(_class=col_cls, id=_id):
            buf << ''.join(r)
        return col_width*12/columns_num, str(buf)

    def _buttons_line(self, buttons):
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
                        buf << '</fieldset><fieldset><legend>%s</legend>' % title
                #process line
                else:
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
        if fieldset:
            buf << '</fieldset>'


class Bootstrap3HLayout(Bootstrap3Layout):

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


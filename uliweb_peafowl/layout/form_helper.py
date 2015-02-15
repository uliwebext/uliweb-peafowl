from uliweb.core.html import Buf, Tag, Div, to_attrs
from uliweb.form.layout import Layout

class Bootstrap3Layout(Layout):
    form_class = 'form-horizontal'
    label_width = 2

    def begin(self):
        if not self.form.html_attrs['class'] and self.form_class:
            self.form.html_attrs['class'] = self.form_class
        self.form.html_attrs['role'] = 'form'
        return self.form.form_begin

    def line(self, obj, label, input, help_string='', error=None):

        _class = "form-group"
        if error:
            _class = _class + ' has-error'

        div_group = Div(_class=_class, id='div_'+obj.id, newline=True)
        with div_group:
            div_group << input.get_label(_class='col-sm-%d control-label' % self.label_width)
            div = Div(_class='col-sm-%d controls' % (12-self.label_width), newline=True)
            with div:
                if obj.static:
                    f_cls = ' form-control-static'
                    input = '<p class="form-control-static">%s</p>' % input.data
                if obj.build.__name__ in ('Checkbox', 'Radio'):
                    d = Div(_class=obj.build.__name__.lower())
                    with d:
                        d << input
                    div << d
                else:
                    f_cls = ' form-control'
                    _cls = obj.html_attrs['class']
                    if _cls:
                        obj.html_attrs['class'] = obj.html_attrs['class'] + f_cls
                    else:
                        obj.html_attrs['class'] = f_cls
                    div << input
                if not obj.static:
                    div << Tag('p', _class="help help-block", _value=help_string)
                    if error:
                        div << Div(_class="message help-block", _value=error, newline=True)

            div_group << str(div)
        return str(div_group)

    def _buttons_line(self, buttons):
        buf = Div(_class="form-group")
        with buf:
            div = Div(_class="col-sm-offset-%d col-sm-%d" % (self.label_width, 12-self.label_width))
            with div:
                div << buttons
            buf << div
        return buf

    def body(self):
        buf = Buf()
        if not self.layout:
            self.layout = [name for name, obj in self.form.fields_list]
        self.process_layout(buf)
        return str(buf)

    def process_layout(self, buf):
        if self.form.form_title:
            buf << '<fieldset><legend>%s</legend>' % self.form.form_title
        for line in self.layout:
            f = getattr(self.form, line)
            obj = self.form.fields[line]
            if self.is_hidden(obj):
                buf << f
            else:
                if obj.build.__name__ in ('Checkbox', 'Radio'):
                    pass
                buf << self.line(obj, f.label, f, f.help_string, f.error)
        if self.form.form_title:
            buf << '</fieldset>'

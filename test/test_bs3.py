from uliweb_peafowl.layout.form_helper import *
from uliweb.form import *

def test_bs3build():
    """
    >>> fields = [
    ...     {'name':'str', 'type':'str', 'label':'String', 'help_string':'This is help string'},
    ... ]
    >>> F = make_form(fields=fields, layout_class=Bootstrap3Layout)
    >>> f = F()
    >>> Bootstrap3_Build().html(f, 'str')
    '<label for="field_str">String:</label><input type="text" value="" class="form-control" id="field_str" name="str"></input><p class="help-block">This is help string</p>'
    >>> Bootstrap3_Build().html(f, 'str', {'class':'test'})
    '<label for="field_str">String:</label><input type="text" value="" class="test form-control" id="field_str" name="str"></input><p class="help-block">This is help string</p>'
    >>> Bootstrap3_Build().html(f, 'str', label_width=2)
    '<label class="col-sm-2 control-label" for="field_str">String:</label><div class="col-sm-10"><input type="text" value="" class="form-control" id="field_str" name="str"></input></div>'
    """

def test_textarea():
    """
    >>> fields = [
    ...     {'name':'textarea', 'type':'text', 'label':'Textarea'},
    ... ]
    >>> F = make_form(fields=fields, layout_class=Bootstrap3Layout)
    >>> f = F()
    >>> Bootstrap3_Text().html(f, 'textarea')
    '<label for="field_textarea">Textarea:</label><textarea class="form-control" id="field_textarea" name="textarea" rows="4"></textarea>'
    >>> F.textarea.static = True
    >>> Bootstrap3_Text().html(f, 'textarea')
    '<label for="field_textarea">Textarea:</label><p class="form-control-static"></p>'
    """

def test_bool():
    """
    >>> fields = [
    ...     {'name':'bool', 'type':'bool', 'label':'Checkbox'},
    ... ]
    >>> F = make_form(fields=fields, layout_class=Bootstrap3Layout)
    >>> f = F()
    >>> Bootstrap3_Checkbox().html(f, 'bool')
    '<div class="checkbox"><label><input type="checkbox" id="field_bool" name="bool">Checkbox</input></label></div>'
    >>> F.bool.static = True
    >>> Bootstrap3_Checkbox().html(f, 'bool')
    '<div class="checkbox"><label><p class="form-control-static"></p></label></div>'
    """

def test_makeform1():
    """
    >>> fields = [
    ...     {'name':'str', 'type':'str', 'label':'String', 'help_string':'This is help string'},
    ...     {'name':'textarea', 'type':'text', 'label':'Textarea'},
    ... ]
    >>> F = make_form(fields=fields, layout_class=Bootstrap3Layout)
    >>> f = F()
    >>> print f
    <form action="" class="" method="POST" role="form">
    <div class="form-group">
        <label for="field_str">String:</label><input type="text" value="" class="form-control" id="field_str" name="str"></input><p class="help-block">This is help string</p>
    </div>
    <BLANKLINE>
    <BLANKLINE>
    <div class="form-group">
        <label for="field_textarea">Textarea:</label><textarea class="form-control" id="field_textarea" name="textarea" rows="4"></textarea>
    </div>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <button class="btn btn-primary" name="submit" type="submit">Submit</button>
    <BLANKLINE>
    </form>
    <BLANKLINE>
    """

if __name__ == '__main__':
    fields = [
        {'name':'str', 'type':'str', 'label':'String', 'static':True},
        {'name':'textarea', 'type':'text', 'label':'Textarea', 'static':True},
    ]
    layout = {
        'rows':[
            ['str', 'textarea'],
        ]
    }
    F = make_form(fields=fields, layout_class=Bootstrap3Layout, layout=layout)
    f = F(data={'textarea':"this is a test"})
    print f

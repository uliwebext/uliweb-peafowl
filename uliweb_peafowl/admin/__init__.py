#coding=utf-8
from uliweb import expose, functions

def prepare_default_env(sender, env):
    from uliweb import settings

    env['ADMIN_URL'] = settings.ADMIN.ADMIN_URL

def require_login_admin(f=None, next=None):
    from uliweb.utils.common import wraps
    
    def _login(next=None):
        from uliweb import request, Redirect, url_for
        
        if not request.user:
            path = functions.request_url()
            Redirect(next or url_for('admin_login', next=path))
    
    if not f:
        _login(next=next)
        return
    
    @wraps(f)
    def _f(*args, **kwargs):
        _login(next=next)
        return f(*args, **kwargs)
    return _f  
  
def default_admin_menu(name, active='', validators=None, id=None, _class=None):
    """
    :param menu: menu item name
    :param active: something like "x/y/z"
    :param check: validate callback, basic validate is defined in settings
    """
    from plugs.menus import iter_menu
    s = []
    for _t, y in iter_menu(name, active, validators):
        index = y['index']
        indent = ' '*index*2
        if _t == 'item':
            _lica = []
            if y['active']:
                _lica.append('active')
            if y['expand']:
                _lica.append('open')
            if y['subs']:
                _lica.append("treeview")
            _licstr = 'class="%s"' % (' '.join(_lica)) if _lica else ''
            s.extend([indent, '<li ', _licstr, '><a href="', y['link'], '">'])
            if 'icon' in y and y['icon']:
                if y['icon'].startswith("ion-"):
                    s.extend(['<i class="ion %s"></i>' % y['icon']])
                elif y['icon'].startswith("fa-"):
                    s.extend(['<i class="fa %s"></i>' % y['icon']])
                else:
                    s.extend(['<i class="fa fa-%s"></i>' % y['icon']])
            else:
                if index > 1:
                    s.append('<i class="fa fa-angle-double-right"></i>')


            s.extend([indent, '<span>', str(y['title']), '</span>'])
            if y['subs']:
                s.append('<i class="fa fa-angle-left pull-right"></i>')
            s.append('</a>')
        elif _t == 'open':
            pass
        elif _t == 'close':
            s.append('</li>\n')
        elif _t == 'begin':
            if index == 0:
                _id = (' id="%s"' % id) if id else ''
                _cls = (' %s' % _class) if _class else ''
                s.append('<ul class="sidebar-menu plugs-menu%s"%s>\n' % (_cls, _id))
            else:
                s.extend(['\n', indent, '<ul class="treeview-menu">\n'])
        else:
            s.extend([indent, '</ul>\n', indent])
    
    return ''.join(s)
    
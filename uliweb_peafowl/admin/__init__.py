#coding=utf-8
from uliweb import expose, functions

def prepare_default_env(sender, env):
    from uliweb import settings

    env['ADMIN_URL'] = settings.ADMIN.ADMIN_URL

def iter_menu(name, active='', validators=None):

    from plugs.menus import get_menu, _validate

    x = active.split('/')
    items = get_menu(name)
    context = {}
    
    def p(menus, active, index=0):
        
        begin = False
        
        #process sub menus
        for j in menus.get('subs', []):
            flag = _validate(j, context, validators)
                
            if not flag:
                continue
            
            if not begin:
                yield 'begin', {'index':index}
                begin = True
                
            yield 'open', {'index':index}
            
            if index < len(x):
                _name = x[index]
                _path = '/'.join(x[0:index+1])
            else:
                _name = ''
                _path = ''

            _active = active == j['id'].split(name+'/')[-1]
            _inpath = _path == j['id'].split(name+'/')[-1]

            # print j['id'].split(name+'/')[-1], _name, _path
            # print _active, _inpath

            link = j.get('link', '#')
            title = j.get('title', j['name'])
            expand = j.get('expand', False)
            
            d = j.copy()
            d.update({'active_path': _inpath, 'active':_active, 'title':title, 'link':link, 'expand':expand, 'index':index+1})
            yield 'item', d
            
            for y in p(j, active, index+1):
                yield y
            
            yield 'close', {'index':index+1}
        
        if begin:
            yield 'end', {'index':index}
         
    for m in p(items, active):
        yield m

  
def _default_admin_menu(name, active='', validators=None, id=None, _class=None, menu_default_class=''):
    """
    :param menu: menu item name
    :param active: something like "x/y/z"
    :param check: validate callback, basic validate is defined in settings
    """

    s = []
    for _t, y in iter_menu(name, active, validators):
        index = y['index']
        indent = ' '*index*2
        if _t == 'item':
            _lica = []
            if y['active_path']:
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
                s.append('<ul class="%s plugs-menu%s"%s>\n' % (menu_default_class, _cls, _id))
            else:
                s.extend(['\n', indent, '<ul class="treeview-menu">\n'])
        else:
            s.extend([indent, '</ul>\n', indent])
    
    return ''.join(s)
    
def default_admin_menu(name, active='', validators=None, id=None, _class=None):
    return _default_admin_menu(name, active=active, 
        validators=validators, id=id, _class=_class, menu_default_class='sidebar-menu')

def default_admin_navigation(name, active='', validators=None, id=None, _class=None):
    return _default_admin_menu(name, active=active, 
        validators=validators, id=id, _class=_class, menu_default_class='navigation-menu')

#coding=utf-8
from uliweb import expose, functions
from uliweb.i18n import ugettext_lazy as _
from uliweb import settings
import urllib

def login():
    from uliweb.contrib.auth import login
    
    form = functions.get_form('auth.LoginForm')()
    
    response.template = "AdminView/login.html"
    default_page = settings.get_var("ADMIN/ADMIN_DEFAULT")

    if request.user:
        next = request.GET.get('next')
        if next:
            return redirect(next)
    
    if request.method == 'GET':
        form.next.data = request.GET.get('next', request.referrer or default_page)
        return {'form':form, 'msg':''}

    if request.method == 'POST':
        flag = form.validate(request.params)
        if flag:
            f, d = functions.authenticate(username=form.username.data, password=form.password.data)
            if f:
                request.session.remember = form.rememberme.data
                login(form.username.data)
                next = urllib.unquote(request.POST.get('next', default_page))
                return redirect(next)
            else:
                form.errors.update(d)
        msg = form.errors.get('_', '') or _('Login failed!')
        return {'form':form, 'msg':str(msg)}    
        
def logout():
    from uliweb.contrib.auth import logout as out
    default_login_page = settings.get_var("ADMIN/ADMIN_LOGIN")
    out()
    next = urllib.unquote(request.POST.get('next', default_login_page))
    return redirect(next)    


@expose('/admin')
class AdminView(object):
    def __begin__(self):
        functions.require_login_admin()

    @expose('')
    def index(self):
        return {}
    

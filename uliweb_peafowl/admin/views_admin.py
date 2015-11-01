#coding=utf-8
from uliweb import expose, functions
from uliweb.i18n import ugettext_lazy as _
from uliweb import settings
import urllib

@expose('/admin')
class AdminView(object):
    def __begin__(self):
        functions.require_login()

    @expose('')
    def index(self):
        return {}
    

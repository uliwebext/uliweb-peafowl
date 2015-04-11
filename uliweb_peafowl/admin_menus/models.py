#coding=utf-8

from uliweb.orm import *
from uliweb.i18n import ugettext_lazy as _

class Admin_Menus_Category(Model):
    key = Field(str, max_length=255, verbose_name=_('Key'))
    title = Field(str, max_length=255, verbose_name=_('Title'))

class Admin_Menus(Model):
    parent = Reference('admin_menus')
    category = Reference('admin_menus_category')
    key = Field(str, max_length=255, verbose_name=_('Key'))
    title = Field(str, max_length=255, verbose_name=_('Name'))
    link = Field(str, max_length=255, verbose_name=_('Link'))
    icon = Field(str, max_length=255, verbose_name=_('Icon'), hint="Fontawesome font class name withouth 'fa-'")
    order = Field(int, verbose_name=_('Order'))
    ext_class = Field(str, max_length=255, verbose_name=_('CSS classes'))
    enabled = Field(bool, default=False, verbose_name=_('Enabled'))
# coding=utf-8
from uliweb.orm import *
from uliweb.utils.common import get_var
from uliweb.utils.generic import GenericReference


def get_modified_user():
    from uliweb import request

    return request.user.id


class DashBoard(Model):
    __verbose_name__ = u'仪表盘布局'

    # dashboard_type = GenericReference(object_fieldname='dashboard_type', table_fieldname='dashboard_type_id')
    # entity = GenericReference(object_fieldname='entity', table_fieldname='entity_id')
    name = Field(CHAR, max_length=50, verbose_name='仪表盘名称')
    layout = Field(CHAR, max_length=1, choices=get_var('DASHBOARD/DASHBOARD_LAYOUT'), verbose_name='布局')
    panel_type = Field(CHAR, max_length=1, choices=get_var('DASHBOARD/PANEL_TYPE'),
                       verbose_name='面板类型')
    default = Field(bool, verbose_name='默认标识', default=False)

    def __unicode__(self):
        return self.name


class Panel(Model):
    __verbose_name__ = u'内容面板'

    name = Field(CHAR, max_length=50, verbose_name='名称')
    title = Field(CHAR, max_length=100, verbose_name='显示名称')
    description = Field(CHAR, max_length=100, verbose_name='描述')
    num = Field(int, verbose_name='数量')
    unit = Field(CHAR, max_length=10, verbose_name='单位')
    content_type = Field(CHAR, max_length=1, choices=get_var('DASHBOARD/CONTENT_TYPE'),
                         verbose_name='内容类型')
    URI = Field(str, max_length=255, verbose_name='访问URI')
    parameters = Field(str, max_length=255, verbose_name='参数')
    count_function = Field(str, max_length=255, verbose_name='数字函数')
    color = Field(CHAR, max_length=20, verbose_name='颜色')
    height = Field(int, verbose_name='高度')
    icon = Field(CHAR, max_length=20, verbose_name='图标')
    closeable = Field(bool, verbose_name='关闭标识')

    def __unicode__(self):
        return self.title


class PanelLayout(Model):
    __verbose_name__ = u'面板布局'

    dashboard = Reference('dashboard', verbose_name='仪表盘')
    panel = Reference('panel', verbose_name='面板')
    row = Field(int, verbose_name='行位置')
    col = Field(int, verbose_name='列位置')
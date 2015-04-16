# coding=utf-8
from uliweb.orm import *
from uliweb.utils.common import get_var
from uliweb.utils.generic import GenericReference


def get_modified_user():
    from uliweb import request

    if request:
        return request.user.id


class DashBoardPanel(Model):
    __verbose_name__ = u'仪表盘内容面板'

    name = Field(str, max_length=50, verbose_name='名称', unique=True)
    title = Field(str, max_length=100, verbose_name='显示名称')
    description = Field(str, max_length=100, verbose_name='描述')
    num = Field(int, verbose_name='数量')
    unit = Field(str, max_length=10, verbose_name='单位')
    panel_type = Field(str, max_length=1, choices=get_var('DASHBOARD/PANEL_TYPE'), verbose_name='面板类型')
    content_type = Field(str, max_length=1, choices=get_var('DASHBOARD/CONTENT_TYPE'),
                         verbose_name='内容类型')
    URI = Field(str, max_length=255, verbose_name='访问URI')
    parameters = Field(str, max_length=255, verbose_name='参数')
    count_function = Field(str, max_length=255, verbose_name='数字函数')
    color = Field(str, max_length=20, verbose_name='颜色')
    height = Field(int, verbose_name='高度')
    icon = Field(CHAR, max_length=20, verbose_name='图标')
    closeable = Field(bool, verbose_name='关闭标识')

    panel_type = Field(str, max_length=1, choices=get_var('DASHBOARD/PANEL_TYPE'),
                       verbose_name='面板类型')

    created_time = Field(
        datetime.datetime, verbose_name='创建时间', auto_now_add=True)
    created_user = Reference(
        'user', verbose_name='创建人', default=get_modified_user, auto_add=True)

    modified_time = Field(
        datetime.datetime, verbose_name='修改时间', auto_now_add=True, auto_now=True)
    modified_user = Reference(
        'user', verbose_name='修改人', default=get_modified_user, auto=True, auto_add=True)

    def __unicode__(self):
        return self.title


class DashBoardPanelLayout(Model):
    __verbose_name__ = u'仪表盘面板布局'

    dashboard_type = GenericReference(table_fieldname='type_id', object_fieldname='owner_id')
    dashboard_name = Field(str, max_length=50, verbose_name='仪表盘')
    layout = Field(str, max_length=10, verbose_name='布局')

    panel = Reference('dashboardpanel', verbose_name='面板')
    title = Field(str, max_length=100, verbose_name='显示名称')
    color = Field(str, max_length=20, verbose_name='颜色')
    height = Field(int, verbose_name='高度')
    icon = Field(str, max_length=20, verbose_name='图标')
    row = Field(int, verbose_name='行位置')
    col = Field(int, verbose_name='列位置')

    created_time = Field(
        datetime.datetime, verbose_name='创建时间', auto_now_add=True)
    created_user = Reference(
        'user', verbose_name='创建人', default=get_modified_user, auto_add=True)

    modified_time = Field(
        datetime.datetime, verbose_name='修改时间', auto_now_add=True, auto_now=True)
    modified_user = Reference(
        'user', verbose_name='修改人', default=get_modified_user, auto=True, auto_add=True)
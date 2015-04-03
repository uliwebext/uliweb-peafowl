#coding=utf8
from uliweb import expose, functions
from uliweb_peafowl.dashboard.common import Dashboard
import logging

log = logging.getLogger(__name__)


class MockDashboard(Dashboard):

    def get_digital_panes(self):
        return [
            {
                'count': "1234", 
                'unit' : "",
                'description': '未处理开发任务', 
                'link' : '/records/query',
                'color': 'aqua',
                'icon' : 'fa-list',
                'id'   : '0001',
            },
            {
                'count': "98", 
                'unit' : "%",
                'description': 'BUG处理率', 
                'link' : '/records/query',
                'color': 'red',
                'icon' : 'fa-bug',
                'id'   : '0002',
            },
            {
                'count': "1000", 
                'unit' : "人",
                'description': '全部用户', 
                'link' : '/records/query',
                'color': 'yellow',
                'icon' : 'fa-male',
                'id'   : '0003',
            },
            {
                'count': "397", 
                'unit' : "个",
                'description': '三期项目', 
                'link' : '/records/query',
                'color': 'green',
                'icon' : 'fa-building',
                'id'   : '0004',
            },                                    
        ]

    def get_content_panes(self):
        return [
            {
                'name': 'pane1',
                'title': 'IFRAME显示',
                'column': 1,
                'row': 1,
                'height': 200,
                'type': 'IFRAME',
                'url' : '/library_demo/dashboard/mock/iframe'
            },
            {
                'name': 'pane2',
                'title': '我的任务列表',
                'column': 1,
                'row': 2,
                'height': 200,
            },
            {
                'name': 'pane3',
                'title': '论坛热帖',
                'column': 2,
                'row': 1,
                'height': 300,
            },                        
            {
                'name': 'pane4',
                'title': '开发任务列表',
                'column': 1,
                'row': 3,
                'height': 200,
            },             
        ]

    def get_content_layout(self):
        return (8, 4)


@expose('/library_demo/dashboard')
class DashboardView(object):

    def __init__(self):
        self.instance = MockDashboard()

    @expose('')
    def index(self):

        view = self.instance.get_view()
        return view

    def edit(self):
        view = self.instance.get_editview()
        return view

@expose('/library_demo/dashboard/mock')        
class MockView(object):

    def iframe(self):
        return {}

    def html_snippet(self):
        return {}

    def json_object(self):
        pass

    def json_datagrid(self):
        pass

    def json_chart(self):
        pass
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
                'link': '/records/query',
                'color': 'aqua',
                'icon' : 'fa-list'
            },
            {
                'count': "98", 
                'unit' : "%",
                'description': 'BUG处理率', 
                'link': '/records/query',
                'color': 'red',
                'icon' : 'fa-bug'
            },
            {
                'count': "1000", 
                'unit' : "人",
                'description': '全部用户', 
                'link': '/records/query',
                'color': 'yellow',
                'icon' : 'fa-male'
            },
            {
                'count': "397", 
                'unit' : "个",
                'description': '三期项目', 
                'link': '/records/query',
                'color': 'green',
                'icon' : 'fa-building'
            },                                    
        ]

    def get_content_panes(self):
        return []


@expose('/library_demo/dashboard')
class DashboardView(object):

    def __init__(self):
        self.instance = MockDashboard()

    @expose('')
    def index(self):

        view = self.instance.get_view()
        return view
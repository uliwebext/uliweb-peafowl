# coding=utf8
import logging

from uliweb import expose
from uliweb_peafowl.dashboard.common import Dashboard

log = logging.getLogger(__name__)


class MockDashboard(Dashboard):
    pass


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
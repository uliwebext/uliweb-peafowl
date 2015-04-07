# coding=utf-8
from uliweb import functions

DIGITAL = '0'
CONTENT = '1'


class Dashboard(object):
    def __init__(self):
        self.panel = functions.get_model('panel')
        self.dashboard = functions.get_model('dashboard')
        self.panellayout = functions.get_model('panellayout')
    
    def _get_panels(self, type):
        dashboard = self.dashboard.get(self.dashboard.c.default == True, self.dashboard.c.panel_type == type)
        layout = dashboard.get_display_value('layout')


        condition = (self.panellayout.c.dashboard == dashboard.id)

        grids = []
        for index, colspan in enumerate(layout):

            cond = (self.panellayout.c.col == index + 1) & condition
            panels = [panel.panel for panel in
                      self.panellayout.filter(cond).order_by(self.panellayout.c.row)]
            grids.append({'colspan': colspan, 'panels': panels})
        return grids

    def get_digital_panes(self):
        return self._get_panels(DIGITAL)

    def get_content_panes(self):
        return self._get_panels(CONTENT)

    def save(self):
        pass

    def get_view(self):
        return {
            'digital': self.get_digital_panes(),
            'content': self.get_content_panes(),
        }

    def get_editview(self):
        return {
            'digital': self.get_digital_panes(),
            'content': self.get_content_panes(),
        }

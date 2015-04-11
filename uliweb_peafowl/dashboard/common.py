# coding=utf-8
from uliweb import functions, settings

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

    def _get_all_panels(self, type):
        query = self.panel.filter(self.panel.c.panel_type == type).order_by(self.panel.c.name)
        return [pane for pane in query]

    def get_all_digital_panes(self):
        return self._get_all_panels(DIGITAL)

    def get_all_content_panes(self):
        return self._get_all_panels(CONTENT)        

    def get_layout_def(self):
        layout_def = settings.DASHBOARD.DASHBOARD_LAYOUT
        options = []
        for id, cols in layout_def:
            options.append((id, "-".join([str(i) for i in cols])))
        return options

    def get_current_content_layout(self):
        dashboard = self.dashboard.get(self.dashboard.c.default == True, 
            self.dashboard.c.panel_type == CONTENT)
        layout = dashboard.get_display_value('layout')

        return "-".join([str(i) for i in layout])

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

            'all_digital': self.get_all_digital_panes(),
            'all_content': self.get_all_content_panes(),
            'content_layout_def': self.get_layout_def(),
            'current_content_layout': self.get_current_content_layout()
        }

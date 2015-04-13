# coding=utf-8
from uliweb import functions, settings

DIGITAL = '0'
CONTENT = '1'


class Dashboard(object):
    def __init__(self, entity=None, default=True):
        self.panel = functions.get_model('panel')
        self.dashboard = functions.get_model('dashboard')
        self.panellayout = functions.get_model('panellayout')
        self.entity = entity
        self.default = default

    def _get_condition(self, dashboardname):
        condition = (self.panellayout.c.default == self.default)

        obj = self.dashboard.get(self.dashboard.c.name == dashboardname)
        condition = (self.panellayout.c.dashboard == obj.id) & condition

        if self.entity:
            condition = (self.panellayout.c.dashboard_type == self.entity) & condition
        return condition

    def _get_layout(self, dashboardname):
        panellayout = self.panellayout.get(self._get_condition(dashboardname))
        return panellayout.layout or panellayout.dashboard.layout


    def _get_panels(self, dashboardname):

        layout = self._get_layout(dashboardname).split('-')

        grids = []
        for index, colspan in enumerate(layout):
            cond = (self.panellayout.c.col == index + 1) & self._get_condition(dashboardname)
            panels = []
            for obj in self.panellayout.filter(cond).order_by(self.panellayout.c.row):
                panel = obj.panel
                if obj.title:
                    panel.title = obj.title
                if obj.height:
                    panel.height = obj.height
                if obj.icon:
                    panel.icon = obj.icon
                if obj.color:
                    panel.color = obj.color
                panels.append(panel)

            grids.append({'colspan': colspan, 'panels': panels})
        return grids

    def _get_all_panels(self, panel_type):
        query = self.panel.filter(self.panel.c.panel_type == panel_type).order_by(self.panel.c.name)
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

    def get_digital_panes(self):
        return self._get_panels('digital')

    def get_content_panes(self):
        return self._get_panels('content')

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
            'current_content_layout': self._get_layout('content')
        }


    def _save_panel(self, panels, layout):
        for pane in panels:
            dashboard, name, row, col = pane
            dashboard = self.dashboard.get(self.dashboard.c.name == dashboard)
            panel = self.panel.get(self.panel.c.name == name)
            panellayout = self.panellayout.get(self.panellayout.c.dashboard == dashboard,
                                               self.panellayout.c.panel == panel, self.panellayout.c.default == False)

            if panellayout:
                panellayout.row = row
                panellayout.col = col
                panellayout.layout = layout
                panellayout.default = False
                panellayout.save()
            else:
                panellayout = panellayout(dashboard=dashboard, panel=panel, row=row, col=col, layou=layout,
                                          default=False)
                panellayout.save()

    def save(self, data):
        digital_panels = data['digital']
        content_panels = data['content']
        layout = data['current_content_layout']
        self._save_panel(digital_panels, layout)
        self._save_panel(content_panels, layout)


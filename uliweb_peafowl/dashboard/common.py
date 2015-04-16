# coding=utf-8
from uliweb import functions, settings
from uliweb import orm

DIGITAL = '0'
CONTENT = '1'


class Dashboard(object):
    def __init__(self, digital_name, content_name, entity=None):
        self.panel = functions.get_model('dashboardpanel')
        self.layout = functions.get_model('dashboardpanellayout')
        self.digital_name = digital_name
        self.content_name = content_name
        if isinstance(entity, (tuple, list)) or isinstance(entity, orm.Model):
            self.entity = entity
        else:
            self.entity = None

    def _get_panels(self, dashboardname):
        res = self.layout.filter(self.layout.c.dashboard_name == dashboardname)
        if self.entity:
            return res.filter(self.entity)
        return res


    def _get_layout(self, dashboardname):
        panellayout = self._get_panels(dashboardname).one()
        return panellayout.layout

    def _get_old_panels(self, dashboardname):
        panels = self._get_panels(dashboardname)
        return [panel.panel._name_ for panel in panels]

    def _get_sorted_panels(self, dashboardname):

        layout = self._get_layout(dashboardname).split('-')

        grids = []

        for index, colspan in enumerate(layout):
            cond = (self.layout.c.col == index + 1)
            panels = []
            for obj in self._get_panels(dashboardname).filter(cond).order_by(self.layout.c.row):
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
        return self._get_sorted_panels(self.digital_name)

    def get_content_panes(self):
        return self._get_sorted_panels(self.content_name)

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

    def _diff_panel(self, old_panels, new_panels):
        list(set(old_panels) - set(new_panels))

    def _save_panel(self, dashboardname, panels, layout):

        def _get_panel(name):
            panel = self.panel.get(self.panel.c.name == name)
            panellayout = self._get_panels(dashboardname).filter(self.layout.c.panel == panel.id).one()
            return panellayout, panel

        new_panels = []
        for pane in panels:
            dashboard, name, row, col = pane
            new_panels.append(name)

            panellayout, panel = _get_panel(name)
            if panellayout:
                panellayout.dashboard_owner = self.entity
                panellayout.row = row
                panellayout.col = col
                panellayout.layout = layout
                panellayout.save()
            else:
                panellayout = self.layout(dashboardname=dashboardname, dashboard_type=self.entity,
                                          panel=panel.id, row=row, col=col, layout=layout)
                panellayout.save()

        for name in list(set(self._get_old_panels(dashboardname)) - set(new_panels)):
            panellayout, panel = _get_panel(name)

            if panellayout:
                panellayout.delete()

    def save(self, data):
        """
        :param data: data to save
        :param default: entity related default is False, admin config default is True
        :return:
        """
        digital_panels = data.get(self.digital_name, '')
        content_panels = data.get(self.content_name, '')
        layout = data.get('layout', '')
        self._save_panel(self.digital_name, digital_panels, '3-' * len(digital_panels))
        self._save_panel(self.content_name, content_panels, layout)


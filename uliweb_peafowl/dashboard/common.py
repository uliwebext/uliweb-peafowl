# coding=utf-8
from uliweb import expose, functions

class Dashboard(object):


    def _get_digital_panes(self):

        # color: 
        #   aqua, green, yellow, red, blue, light-blue
        #   navy, teal, olive, lime, orange, fuchsia
        #   purple, maroon

        default_colors = [
            'light-blue', 'green', 'yellow', 'red', 
            'purple', 'blue', 'olive',  'orange', 'maroon', 
            'aqua', 'fuchsia', 'teal', 'lime', 
        ]

        default_icons = [
            'fa-bar-chart', 'fa-pie-chart', 'fa-line-chart', 'fa-flag',
            'fa-slack', 'fa-cubes', 'fa-cube', 'fa-pagelines', 'fa-anchor'
        ]

        panes = self.get_digital_panes()

        for index, pane in enumerate(panes):
            if not pane.has_key('color'):
                pane['color'] = default_colors[index % len(default_colors)]
            if not pane.has_key('icon'):
                pane['icon'] = default_icons[index % len(default_icons)]

        digital_pane_size = len(panes)
        if digital_pane_size   == 6:
            colspan = 2
        elif digital_pane_size == 5:
            colspan = 3
        elif digital_pane_size == 4:
            colspan = 3
        elif digital_pane_size == 3:
            colspan = 4
        elif digital_pane_size == 2:
            colspan = 6
        elif digital_pane_size == 1:
            colspan = 12    
        else:
            colspan = 3    

        return {
            'size': digital_pane_size,
            'colspan': colspan,
            'panes': panes
        }


    def _get_content_panes(self):

        panes = self.get_content_panes()

        return {
            'size': len(panes),
            'panes': panes
        }

    def get_view(self):
        return {
            'digital': self._get_digital_panes(),
            'content': self._get_content_panes(),
        }

    def get_editview(self):
        return {}
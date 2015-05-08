from uliweb import functions, settings
from uliweb.orm import set_dispatch_send

set_dispatch_send(False)

panel = functions.get_model('dashboardpanel')
layout = functions.get_model('dashboardpanellayout')


def process_panel():
    p = settings.get('PANEL', {})
    for data in p.items():
        panel(**data).save()

def process_layout():
    l = settings.get('PANELLAYOUT', {})
    for data in l.items():
        layout(**data).save()

if __name__ == '__main__':
    process_panel()
    process_layout()
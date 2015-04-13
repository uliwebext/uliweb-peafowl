from uliweb import functions, settings
from uliweb.orm import set_dispatch_send

set_dispatch_send(False)

dashboard = functions.get_model('dashboard')
panel = functions.get_model('panel')
panellayout = functions.get_model('panellayout')


def process_dashboard():
    d = settings.get('DASHBOARD', {})
    for name, layout in d.items():
        data = {'name': name, 'layout': layout}
        dashboard(**data).save()


def process_panel():
    p = settings.get('PANEL', {})
    for data in p.items():
        panel(**data).save()


if __name__ == '__main__':
    process_dashboard()
    process_panel()
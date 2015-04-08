#! /usr/bin/env python
# coding=utf-8

from uliweb import settings, functions
from uliweb.manage import make_simple_application
from uliweb.orm import Begin, Commit, Rollback
from uliweb.orm import set_dispatch_send


set_dispatch_send(False)


def import_mock_data():
    dashboard = functions.get_model('dashboard')
    panel = functions.get_model('panel')
    panellayout = functions.get_model('panellayout')

    for data in settings.DASHBOARD_MOCKDATA.dashboards:
        obj = dashboard(**data)
        obj.save()
    for data in settings.PANEL_MOCKDATA.panels:
        obj = panel(**data)
        obj.save()

    for data in settings.PANEL_DASHBOARD_MOCKDATA.layout:
        board, pane, row, col = data
        layout = {}
        layout['dashboard'] = dashboard.get(dashboard.c.name == board)
        layout['panel'] = panel.get(panel.c.name == pane)
        layout['row'] = row
        layout['col'] = col
        obj = panellayout(**layout)
        obj.save()


def process():
    import_mock_data()


def call(args, options, global_options):
    app = make_simple_application(apps_dir=global_options.apps_dir)

    Begin()
    try:
        process()
        Commit()
    except:
        Rollback()
        import traceback

        traceback.print_exc()

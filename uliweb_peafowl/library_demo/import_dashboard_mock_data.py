#! /usr/bin/env python
# coding=utf-8

from uliweb import settings, functions
from uliweb.manage import make_simple_application
from uliweb.orm import Begin, Commit, Rollback
from uliweb.orm import set_dispatch_send


set_dispatch_send(False)


def import_mock_data():
    panel = functions.get_model('dashboardpanel')
    panellayout = functions.get_model('dashboardpanellayout')

    for data in settings.PANEL_MOCKDATA.panels:
        obj = panel(**data)
        obj.save()

    for data in settings.PANEL_DASHBOARD_MOCKDATA.layout:
        board, panel_layout, pane, row, col = data
        layout = {}

        layout['dashboard_name'] = board
        layout['panel'] = panel.get(panel.c.name == pane)
        layout['row'] = row
        layout['col'] = col
        layout['layout'] = panel_layout
        obj = panellayout(**layout)
        obj.save()


def clear_mock_data():
    panel = functions.get_model('dashboardpanel')
    panellayout = functions.get_model('dashboardpanellayout')

    panel.remove()
    panellayout.remove()


def process():
    clear_mock_data()
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

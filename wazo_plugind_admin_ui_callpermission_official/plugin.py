# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.helpers.destination import register_listing_url

from .service import CallpermissionService
from .view import CallpermissionView, CallpermissionListingView

callpermission = create_blueprint('callpermission', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        CallpermissionView.service = CallpermissionService()
        CallpermissionView.register(callpermission, route_base='/callpermissions')
        register_flaskview(callpermission, CallpermissionView)

        CallpermissionListingView.service = CallpermissionService()
        CallpermissionListingView.register(callpermission, route_base='/callpermissions_listing')

        register_listing_url('callpermission', 'callpermission.CallpermissionListingView:list_json')

        core.register_blueprint(callpermission)

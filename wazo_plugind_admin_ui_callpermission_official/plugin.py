# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.helpers.destination import register_listing_url

from .service import CallPermissionService
from .view import CallPermissionView, CallPermissionListingView

callpermission = create_blueprint('callpermission', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        CallPermissionView.service = CallPermissionService()
        CallPermissionView.register(callpermission, route_base='/callpermissions')
        register_flaskview(callpermission, CallPermissionView)

        CallPermissionListingView.service = CallPermissionService()
        CallPermissionListingView.register(callpermission, route_base='/callpermissions_listing')

        register_listing_url('callpermission', 'callpermission.CallPermissionListingView:list_json')

        core.register_blueprint(callpermission)

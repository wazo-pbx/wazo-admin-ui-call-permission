# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import jsonify, request
from flask_babel import lazy_gettext as l_
from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.classful import BaseView, LoginRequiredView
from wazo_admin_ui.helpers.classful import extract_select2_params, build_select2_response

from .form import CallPermissionForm


class CallPermissionView(BaseView):
    form = CallPermissionForm
    resource = 'callpermission'

    @classy_menu_item('.callpermissions', l_('Call Permissions'), order=8, icon='ban')
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        resource['user_ids'] = [user['id'] for user in resource['users']]
        resource['group_ids'] = [group['id'] for group in resource['groups']]
        resource['outcall_ids'] = [outcall['id'] for outcall in resource['outcalls']]
        resource['extensions'] = [{'exten': exten} for exten in resource['extensions']]
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.user_ids.choices = self._build_set_choices_users(form.users)
        form.group_ids.choices = self._build_set_choices_groups(form.groups)
        form.outcall_ids.choices = self._build_set_choices_outcalls(form.outcalls)
        return form

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            if user.form.lastname.data:
                text = '{} {}'.format(user.form.firstname.data, user.form.lastname.data)
            else:
                text = user.form.firstname.data
            results.append((user.form.id.data, text))
        return results

    def _build_set_choices_groups(self, groups):
        return [(group.form.id.data, group.form.name.data) for group in groups]

    def _build_set_choices_outcalls(self, outcalls):
        return [(outcall.form.id.data, outcall.form.name.data) for outcall in outcalls]

    def _map_form_to_resources(self, form, form_id=None):
        data = super()._map_form_to_resources(form, form_id)
        data['user_ids'] = [user_id for user_id in form.user_ids.data]
        data['group_ids'] = [group_id for group_id in form.group_ids.data]
        data['outcall_ids'] = [outcall_id for outcall_id in form.outcall_ids.data]
        data['extensions'] = [extension['exten'] for extension in data['extensions']]
        return data


class CallPermissionListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        callpermissions = self.service.list(**params)
        results = [{'id': callpermission['id'], 'text': callpermission['name']}
                   for callpermission in callpermissions['items']]
        return jsonify(build_select2_response(results, callpermissions['total'], params))

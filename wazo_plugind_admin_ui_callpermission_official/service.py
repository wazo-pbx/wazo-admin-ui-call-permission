# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.confd import confd
from wazo_admin_ui.helpers.service import BaseConfdService


class CallPermissionService(BaseConfdService):
    resource_confd = 'call_permissions'

    def get(self, resource_id):
        resource = super().get(resource_id)
        users = confd.call_permissions(resource_id).list_users()
        resource['users'] = self._build_user_list(users['items'])
        return resource

    def _build_user_list(self, users):
        result = []
        for user in users:
            user_data = self.get_user(user['user_id'])
            result.append({
                'id': user['user_id'],
                'firstname': user_data['firstname'],
                'lastname': user_data['lastname']
            })
        return result

    def update(self, resource):
        super().update(resource)
        existing_resource = self.get(resource['id'])
        self.update_users(resource['id'], resource['user_ids'], existing_resource['users'])
        self.update_groups(resource['id'], resource['group_ids'], existing_resource['groups'])
        self.update_outcals(resource['id'], resource['outcall_ids'], existing_resource['outcalls'])

    def update_users(self, callpermission_id, user_ids, existing_user_ids=None):
        if existing_user_ids:
            for existing_user_id in existing_user_ids:
                confd.users(existing_user_id).remove_call_permission(callpermission_id)
        for user_id in user_ids:
            confd.users(user_id).add_call_permission(callpermission_id)

    def update_groups(self, callpermission_id, groups_ids, existing_groups_ids=None):
        if existing_groups_ids:
            for existing_group_id in existing_groups_ids:
                confd.groups(existing_group_id).remove_call_permission(callpermission_id)
        for groups_id in groups_ids:
            confd.groups(groups_id).add_call_permission(callpermission_id)

    def update_outcals(self, callpermission_id, outcall_ids, existing_outcall_ids=None):
        if existing_outcall_ids:
            for existing_outcall_id in existing_outcall_ids:
                confd.outcalls(existing_outcall_id).remove_call_permission(callpermission_id)
        for outcall_id in outcall_ids:
            confd.outcalls(outcall_id).add_call_permission(callpermission_id)

    def get_user(self, user_id):
        return confd.users.get(user_id)

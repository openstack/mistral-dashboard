# Copyright 2015 Huawei Technologies Co., Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.urls import reverse

from openstack_dashboard.test import helpers as horizon_test

from mistraldashboard import api
from mistraldashboard.test import helpers as test

INDEX_URL = reverse('horizon:mistral:actions:index')


class ActionsTest(test.TestCase):

    @horizon_test.create_mocks({api: ('pagination_list',)})
    def test_index(self):
        self.mock_pagination_list.return_value =\
            [self.mistralclient_actions.list(), False, False]
        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'mistral/actions/index.html')
        self.mock_pagination_list.assert_called_once_with(
            entity="actions", request=horizon_test.IsHttpRequest(),
            marker=None, sort_keys='name', sort_dirs='desc',
            paginate=True, reversed_order=True)

    @horizon_test.create_mocks({api: ('action_create',)})
    def test_create_post(self):
        action = self.mistralclient_actions.first()
        self.mock_action_create.return_value = action
        url = reverse("horizon:mistral:actions:create")
        form_data = {
            'definition_source': 'raw',
            'definition_data': action.definition
        }
        res = self.client.post(url, form_data)

        self.assertNoFormErrors(res)
        self.mock_action_create.assert_called_once_with(
            horizon_test.IsHttpRequest(),
            action.definition)

    @horizon_test.create_mocks({api: ('action_update',)})
    def test_update_post(self):
        action = self.mistralclient_actions.first()
        self.mock_action_update.return_value = action
        url = reverse("horizon:mistral:actions:update")
        form_data = {
            'definition_source': 'raw',
            'definition_data': action.definition
        }
        res = self.client.post(url, form_data)

        self.assertNoFormErrors(res)
        self.mock_action_update.assert_called_once_with(
            horizon_test.IsHttpRequest(),
            action.definition)

    @horizon_test.create_mocks({api: ('action_get',)})
    def test_detail(self):
        action = self.mistralclient_actions.list()[0]
        self.mock_action_get.return_value = action
        url = reverse('horizon:mistral:actions:detail',
                      args=[action.id])
        res = self.client.get(url)

        self.assertTemplateUsed(res, 'mistral/actions/detail.html')
        self.mock_action_get.assert_called_once_with(
            horizon_test.IsHttpRequest(), action.id)

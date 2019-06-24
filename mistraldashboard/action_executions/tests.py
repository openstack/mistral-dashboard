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

from openstack_dashboard.test import helpers

from mistraldashboard import api
from mistraldashboard.test import helpers as test

INDEX_URL = reverse('horizon:mistral:action_executions:index')


class ActionExecutionsTest(test.TestCase):

    @helpers.create_mocks({api: ('action_executions_list',)})
    def test_index(self):
        self.mock_action_executions_list.return_value =\
            self.mistralclient_action_executions.list()
        res = self.client.get(INDEX_URL)

        self.assertTemplateUsed(res, 'mistral/action_executions/index.html')
        self.mock_action_executions_list.assert_called_once_with(
            helpers.IsHttpRequest())

    @helpers.create_mocks({api: ('action_execution_update',)})
    def test_update_post(self):
        action_execution = self.mistralclient_action_executions.first()
        self.mock_action_execution_update.return_value = action_execution
        form_data = {"action_execution_id": action_execution.id,
                     "state": action_execution.state,
                     "output_source": "raw",
                     "output_data": action_execution.output}
        res = self.client.post(
            reverse('horizon:mistral:action_executions:update',
                    args=(action_execution.id,)),
            form_data)
        self.assertNoFormErrors(res)
        self.mock_action_execution_update.assert_called_once_with(
            helpers.IsHttpRequest(), action_execution.id,
            action_execution.state, action_execution.output)

    @helpers.create_mocks({api: ('action_execution_get',)})
    def test_detail(self):
        action_execution = self.mistralclient_action_executions.list()[0]
        self.mock_action_execution_get.return_value = action_execution
        url = reverse('horizon:mistral:action_executions:detail',
                      args=[action_execution.id])
        res = self.client.get(url)

        self.assertTemplateUsed(res, 'mistral/action_executions/detail.html')
        self.mock_action_execution_get.assert_called_once_with(
            helpers.IsHttpRequest(), action_execution.id)

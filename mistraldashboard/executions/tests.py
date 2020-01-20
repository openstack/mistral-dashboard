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

INDEX_URL = reverse('horizon:mistral:executions:index')


class ExecutionsTest(test.TestCase):

    @helpers.create_mocks({api: ('pagination_list',)})
    def test_index(self):
        self.mock_pagination_list.return_value =\
            [self.mistralclient_executions.list(), False, False]
        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'mistral/executions/index.html')
        self.assertCountEqual(res.context['table'].data,
                              self.mistralclient_executions.list())
        self.mock_pagination_list.assert_called_once_with(
            entity="executions",
            request=helpers.IsHttpRequest(),
            marker=None,
            sort_dirs='desc',
            paginate=True)

    @helpers.create_mocks({api: ('execution_update',)})
    def test_update_post(self):
        execution = self.mistralclient_executions.first()
        self.mock_execution_update.return_value = execution
        form_data = {
            "execution_id": execution.id,
            "description": "description"}
        res = self.client.post(
            reverse('horizon:mistral:executions:update_description',
                    args=(execution.id,)),
            form_data)
        self.assertNoFormErrors(res)
        self.mock_execution_update.assert_called_once_with(
            helpers.IsHttpRequest(), execution.id,
            "description", "description")

    @helpers.create_mocks({api: ('execution_get', 'task_list')})
    def test_detail(self):
        execution = self.mistralclient_executions.list()[0]
        tasks = self.mistralclient_tasks.list()
        self.mock_execution_get.return_value = execution
        self.mock_task_list.return_value = tasks
        url = reverse('horizon:mistral:executions:detail',
                      args=[execution.id])
        res = self.client.get(url)

        self.assertTemplateUsed(res, 'mistral/executions/detail.html')
        self.mock_execution_get.assert_called_once_with(
            helpers.IsHttpRequest(), execution.id)
        self.mock_task_list.assert_called_once_with(
            helpers.IsHttpRequest(), execution.id)

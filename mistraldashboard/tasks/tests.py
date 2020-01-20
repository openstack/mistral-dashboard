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

INDEX_URL = reverse('horizon:mistral:tasks:index')


class TasksTest(test.TestCase):

    @helpers.create_mocks({api: ('task_list',)})
    def test_index(self):
        self.mock_task_list.return_value =\
            self.mistralclient_tasks.list()
        res = self.client.get(INDEX_URL)

        self.assertTemplateUsed(res, 'mistral/tasks/index.html')
        self.assertCountEqual(res.context['table'].data,
                              self.mistralclient_tasks.list())
        self.mock_task_list.assert_called_once_with(helpers.IsHttpRequest())

    @helpers.create_mocks({api: ('task_get',)})
    def test_detail(self):
        task = self.mistralclient_tasks.list()[0]
        self.mock_task_get.return_value = task
        url = reverse('horizon:mistral:tasks:detail',
                      args=[task.id])
        res = self.client.get(url)
        self.assertTemplateUsed(res, 'mistral/tasks/detail.html')
        self.mock_task_get.assert_called_once_with(
            helpers.IsHttpRequest(), task.id)

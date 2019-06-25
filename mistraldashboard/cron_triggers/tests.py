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

INDEX_URL = reverse('horizon:mistral:cron_triggers:index')


class CronTriggersTest(test.TestCase):

    @helpers.create_mocks({api: ('cron_trigger_list',)})
    def test_index(self):
        self.mock_cron_trigger_list.return_value =\
            self.mistralclient_cron_triggers.list()
        res = self.client.get(INDEX_URL)

        self.assertTemplateUsed(res, 'mistral/cron_triggers/index.html')
        self.mock_cron_trigger_list.assert_called_once_with(
            helpers.IsHttpRequest())

    @helpers.create_mocks({api: ('cron_trigger_create',
                                 'workflow_list')})
    def test_create_post(self):
        cron_trigger = self.mistralclient_cron_triggers.first()
        workflows = self.mistralclient_workflows.list()
        self.mock_cron_trigger_create.return_value = cron_trigger
        self.mock_workflow_list.return_value = workflows
        url = reverse("horizon:mistral:cron_triggers:create")
        form_data = {
            'name': cron_trigger.name,
            'workflow_id': '1',
            'input_source': 'raw',
            'input_data': '{"a":"b"}',
            'params_source': 'raw',
            'params_data': '{"a":"b"}',
            'schedule_pattern': cron_trigger.pattern,
            'first_time': cron_trigger.first_execution_time,
            'schedule_count': '1'
        }
        res = self.client.post(url, form_data)

        self.assertNoFormErrors(res)
        self.mock_cron_trigger_create.assert_called_once_with(
            helpers.IsHttpRequest(),
            cron_trigger.name, form_data["workflow_id"],
            {u'a': u'b'}, {u'a': u'b'},
            None, None,
            form_data["schedule_count"]
            )
        self.mock_workflow_list.assert_called_once_with(
            helpers.IsHttpRequest())

    @helpers.create_mocks({api: ('cron_trigger_get',)})
    def test_detail(self):
        cron_trigger = self.mistralclient_cron_triggers.list()[0]
        self.mock_cron_trigger_get.return_value = cron_trigger
        url = reverse('horizon:mistral:cron_triggers:detail',
                      args=[cron_trigger.id])
        res = self.client.get(url)

        self.assertTemplateUsed(res, 'mistral/cron_triggers/detail.html')
        self.mock_cron_trigger_get.assert_called_once_with(
            helpers.IsHttpRequest(), cron_trigger.id)

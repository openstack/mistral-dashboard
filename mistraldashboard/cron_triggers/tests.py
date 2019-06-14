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

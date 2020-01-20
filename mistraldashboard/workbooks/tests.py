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

INDEX_URL = reverse('horizon:mistral:workbooks:index')
CREATE_URL = reverse('horizon:mistral:workbooks:create')
UPDATE_URL = reverse('horizon:mistral:workbooks:update')


class WorkflowsTest(test.TestCase):

    @helpers.create_mocks({api: ('workbook_list',)})
    def test_index(self):
        self.mock_workbook_list.return_value =\
            self.mistralclient_workbooks.list()
        res = self.client.get(INDEX_URL)

        self.assertTemplateUsed(res, 'mistral/workbooks/index.html')
        self.assertCountEqual(res.context['table'].data,
                              self.mistralclient_workbooks.list())
        self.mock_workbook_list.\
            assert_called_once_with(helpers.IsHttpRequest())

    def test_create_get(self):
        res = self.client.get(CREATE_URL)
        self.assertTemplateUsed(res, 'mistral/workbooks/create.html')

    @helpers.create_mocks({api: ('workbook_validate',
                                 'workbook_create')})
    def test_create_post(self):
        self.mock_workbook_validate.return_value = {'valid': True}
        workbook = self.mistralclient_workbooks.first()

        url = reverse('horizon:mistral:workbooks:select_definition')
        res = self.client.get(url)
        self.assertTemplateUsed(
            res,
            'mistral/workbooks/select_definition.html'
        )
        form_data = {
            'definition_source': 'raw',
            'definition_data': workbook.definition
        }
        res = self.client.post(url, form_data)

        self.assertTemplateUsed(res, 'mistral/workbooks/create.html')
        self.mock_workbook_validate.assert_called_once_with(
            helpers.IsHttpRequest(), workbook.definition)

        form_data = {
            'definition': workbook.definition
        }
        self.mock_workbook_create.return_value = workbook
        res = self.client.post(CREATE_URL, form_data)
        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 302)
        self.assertRedirectsNoFollow(res, INDEX_URL)

        self.mock_workbook_create.assert_called_once_with(
            helpers.IsHttpRequest(),
            workbook.definition)

    def test_update_get(self):
        res = self.client.get(UPDATE_URL)
        self.assertTemplateUsed(res, 'mistral/workbooks/update.html')

    @helpers.create_mocks({api: ('workbook_validate',
                                 'workbook_update')})
    def test_update_post(self):
        workbook = self.mistralclient_workbooks.first()
        self.mock_workbook_validate.return_value = {'valid': True}
        url = reverse('horizon:mistral:workbooks:change_definition')
        res = self.client.get(url)
        self.assertTemplateUsed(
            res,
            'mistral/workbooks/select_definition.html'
        )
        form_data = {
            'definition_source': 'raw',
            'definition_data': workbook.definition
        }
        res = self.client.post(url, form_data)

        self.assertTemplateUsed(res, 'mistral/workbooks/update.html')
        self.mock_workbook_validate.assert_called_once_with(
            helpers.IsHttpRequest(),
            workbook.definition)

        form_data = {
            'definition': workbook.definition
        }
        self.mock_workbook_update.return_value = workbook
        res = self.client.post(UPDATE_URL, form_data)
        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 302)
        self.assertRedirectsNoFollow(res, INDEX_URL)

        self.mock_workbook_update.assert_called_once_with(
            helpers.IsHttpRequest(),
            workbook.definition)

    @helpers.create_mocks({api: ('workbook_list',
                                 'workbook_delete')})
    def test_delete_ok(self):
        workbooks = self.mistralclient_workbooks.list()
        self.mock_workbook_list.return_value = workbooks
        self.mock_workbook_delete.return_value = None

        data = {'action': 'workbooks__delete',
                'object_ids': [workbooks[0].name]}

        res = self.client.post(INDEX_URL, data)

        self.mock_workbook_delete.assert_called_once_with(
            helpers.IsHttpRequest(), workbooks[0].name)
        self.mock_workbook_list.assert_called_once_with(
            helpers.IsHttpRequest())
        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, INDEX_URL)

    @helpers.create_mocks({api: ('workbook_get',)})
    def test_detail(self):
        workbook = self.mistralclient_workbooks.list()[0]
        self.mock_workbook_get.return_value = workbook
        url = reverse('horizon:mistral:workbooks:detail',
                      args=[workbook.name])
        res = self.client.get(url)

        self.assertTemplateUsed(res, 'mistral/workbooks/detail.html')
        self.mock_workbook_get.assert_called_once_with(
            helpers.IsHttpRequest(), workbook.name)

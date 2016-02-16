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

from django.core.urlresolvers import reverse
import mock

from mistraldashboard.test import helpers as test

INDEX_URL = reverse('horizon:mistral:workbooks:index')
CREATE_URL = reverse('horizon:mistral:workbooks:create')
UPDATE_URL = reverse('horizon:mistral:workbooks:update')


class WorkflowsTest(test.TestCase):

    def test_index(self):
        with mock.patch('mistraldashboard.api.workbook_list',
                        return_value=self.mistralclient_workbooks.list()):
            res = self.client.get(INDEX_URL)

        self.assertTemplateUsed(res, 'mistral/workbooks/index.html')

    def test_create_get(self):
        res = self.client.get(CREATE_URL)
        self.assertTemplateUsed(res, 'mistral/workbooks/create.html')

    def test_create_post(self):
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
        with mock.patch('mistraldashboard.api.workbook_validate',
                        return_value={'valid': True}) as mocked_validate:
            res = self.client.post(url, form_data)

        self.assertTemplateUsed(res, 'mistral/workbooks/create.html')
        mocked_validate.assert_called_once_with(
            mock.ANY,
            workbook.definition
        )

        form_data = {
            'definition': workbook.definition
        }
        with mock.patch('mistraldashboard.api.workbook_create',
                        return_value=workbook) as mocked_create:
            res = self.client.post(CREATE_URL, form_data)
        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 302)
        self.assertRedirectsNoFollow(res, INDEX_URL)

        mocked_create.assert_called_once_with(
            mock.ANY,
            workbook.definition
        )

    def test_update_get(self):
        res = self.client.get(UPDATE_URL)
        self.assertTemplateUsed(res, 'mistral/workbooks/update.html')

    def test_update_post(self):
        workbook = self.mistralclient_workbooks.first()

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
        with mock.patch('mistraldashboard.api.workbook_validate',
                        return_value={'valid': True}) as mocked_validate:
            res = self.client.post(url, form_data)

        self.assertTemplateUsed(res, 'mistral/workbooks/update.html')
        mocked_validate.assert_called_once_with(
            mock.ANY,
            workbook.definition
        )

        form_data = {
            'definition': workbook.definition
        }
        with mock.patch('mistraldashboard.api.workbook_update',
                        return_value=workbook) as mocked_update:
            res = self.client.post(UPDATE_URL, form_data)
        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 302)
        self.assertRedirectsNoFollow(res, INDEX_URL)

        mocked_update.assert_called_once_with(
            mock.ANY,
            workbook.definition
        )

    def test_delete_ok(self):
        workbooks = self.mistralclient_workbooks.list()

        data = {'action': 'workbooks__delete',
                'object_ids': [workbooks[0].name]}

        with mock.patch(
                'mistraldashboard.api.workbook_list',
                return_value=workbooks
        ), mock.patch(
                'mistraldashboard.api.workbook_delete',
                return_value=None
        ) as mocked_delete:

            res = self.client.post(INDEX_URL, data)

        mocked_delete.assert_called_once_with(
            mock.ANY,
            workbooks[0].name
        )
        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, INDEX_URL)

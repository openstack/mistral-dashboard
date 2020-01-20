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

INDEX_URL = reverse('horizon:mistral:workflows:index')
CREATE_URL = reverse('horizon:mistral:workflows:create')
UPDATE_URL = reverse('horizon:mistral:workflows:update')


class WorkflowsTest(test.TestCase):

    @helpers.create_mocks({api: ('workflow_list',)})
    def test_index(self):
        self.mock_workflow_list.return_value =\
            self.mistralclient_workflows.list()
        res = self.client.get(INDEX_URL)

        self.assertTemplateUsed(res, 'mistral/workflows/index.html')
        self.assertCountEqual(res.context['table'].data,
                              self.mistralclient_workflows.list())
        self.mock_workflow_list.assert_called_once_with(
            helpers.IsHttpRequest())

    def test_create_get(self):
        res = self.client.get(CREATE_URL)
        self.assertTemplateUsed(res, 'mistral/workflows/create.html')

    @helpers.create_mocks({api: ('workflow_validate',
                                 'workflow_create')})
    def test_create_post(self):
        workflow = self.mistralclient_workflows.first()
        self.mock_workflow_validate.return_value = {'valid': True}
        self.mock_workflow_create.return_value = workflow

        url = reverse('horizon:mistral:workflows:select_definition')
        res = self.client.get(url)
        self.assertTemplateUsed(
            res,
            'mistral/workflows/select_definition.html'
        )
        form_data = {
            'definition_source': 'raw',
            'definition_data': workflow.definition
        }
        res = self.client.post(url, form_data)

        self.assertTemplateUsed(res, 'mistral/workflows/create.html')
        self.mock_workflow_validate.assert_called_once_with(
            helpers.IsHttpRequest(),
            workflow.definition
        )

        form_data = {
            'definition': workflow.definition
        }
        res = self.client.post(CREATE_URL, form_data)
        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 302)
        self.assertRedirectsNoFollow(res, INDEX_URL)

        self.mock_workflow_create.assert_called_once_with(
            helpers.IsHttpRequest(),
            workflow.definition
        )

    def test_update_get(self):
        res = self.client.get(UPDATE_URL)
        self.assertTemplateUsed(res, 'mistral/workflows/update.html')

    @helpers.create_mocks({api: ('workflow_validate',
                                 'workflow_update')})
    def test_update_post(self):
        workflow = self.mistralclient_workflows.first()
        self.mock_workflow_validate.return_value = {'valid': True}
        self.mock_workflow_update.return_value = workflow

        url = reverse('horizon:mistral:workflows:change_definition')
        res = self.client.get(url)
        self.assertTemplateUsed(
            res,
            'mistral/workflows/select_definition.html'
        )
        form_data = {
            'definition_source': 'raw',
            'definition_data': workflow.definition
        }
        res = self.client.post(url, form_data)

        self.assertTemplateUsed(res, 'mistral/workflows/update.html')
        self.mock_workflow_validate.assert_called_once_with(
            helpers.IsHttpRequest(),
            workflow.definition
        )

        form_data = {
            'definition': workflow.definition
        }
        res = self.client.post(UPDATE_URL, form_data)
        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 302)
        self.assertRedirectsNoFollow(res, INDEX_URL)

        self.mock_workflow_update.assert_called_once_with(
            helpers.IsHttpRequest(),
            workflow.definition
        )

    @helpers.create_mocks({api: ('workflow_list',
                                 'workflow_delete')})
    def test_delete_ok(self):
        workflows = self.mistralclient_workflows.list()
        self.mock_workflow_list.return_value = workflows
        self.mock_workflow_delete.return_value = None

        data = {'action': 'workflows__delete',
                'object_ids': [workflows[0].name]}

        res = self.client.post(INDEX_URL, data)

        self.mock_workflow_delete.assert_called_once_with(
            helpers.IsHttpRequest(),
            workflows[0].name
        )
        self.mock_workflow_list.assert_called_once_with(
            helpers.IsHttpRequest())
        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, INDEX_URL)

    @helpers.create_mocks({api: ('workflow_get',)})
    def test_detail(self):
        workflow = self.mistralclient_workflows.list()[0]
        self.mock_workflow_get.return_value = workflow
        url = reverse('horizon:mistral:workflows:detail',
                      args=[workflow.name])
        res = self.client.get(url)

        self.assertTemplateUsed(res, 'mistral/workflows/detail.html')
        self.mock_workflow_get.assert_called_once_with(
            helpers.IsHttpRequest(), workflow.name)

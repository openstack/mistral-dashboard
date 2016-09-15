# -*- coding: utf-8 -*-
#
# Copyright 2014 - StackStorm, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from horizon import exceptions
from horizon import forms
from horizon import tables

from mistraldashboard import api
from mistraldashboard.workflows import forms as mistral_forms
from mistraldashboard.workflows import tables as workflows_tables


class IndexView(tables.DataTableView):
    table_class = workflows_tables.WorkflowsTable
    template_name = 'mistral/workflows/index.html'

    def get_data(self):
        return api.workflow_list(self.request)


class DetailView(generic.TemplateView):
    template_name = 'mistral/workflows/detail.html'
    page_title = _("Workflow Definition")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        workflow = self.get_data(self.request, **kwargs)
        context['definition'] = (
            workflow.definition or
            'This workflow was created as part of workbook %s'
            % workflow.name.split('.')[0])
        return context

    def get_data(self, request, **kwargs):
        try:
            workflow_name = kwargs['workflow_name']
            workflow = api.workflow_get(request, workflow_name)
        except Exception:
            msg = _('Unable to get workflow "%s".') % workflow_name
            redirect = reverse('horizon:mistral:workflows:index')
            exceptions.handle(self.request, msg, redirect=redirect)

        return workflow


class ExecuteView(forms.ModalFormView):
    form_class = mistral_forms.ExecuteForm
    template_name = 'mistral/workflows/execute.html'
    success_url = reverse_lazy("horizon:mistral:executions:index")

    def get_context_data(self, **kwargs):
        context = super(ExecuteView, self).get_context_data(**kwargs)

        context["workflow_name"] = self.kwargs['workflow_name']

        return context

    def get_initial(self, **kwargs):
        return {'workflow_name': self.kwargs['workflow_name']}


class SelectDefinitionView(forms.ModalFormView):
    template_name = 'mistral/workflows/select_definition.html'
    modal_header = _("Create Workflow")
    form_id = "select_definition"
    form_class = mistral_forms.DefinitionForm
    submit_label = _("Next")
    submit_url = reverse_lazy("horizon:mistral:workflows:select_definition")
    success_url = reverse_lazy('horizon:mistral:workflows:create')
    page_title = _("Select Definition")

    def get_form_kwargs(self):
        kwargs = super(SelectDefinitionView, self).get_form_kwargs()
        kwargs['next_view'] = CreateView

        return kwargs


class ChangeDefinitionView(SelectDefinitionView):
    modal_header = _("Update Workflow")
    submit_url = reverse_lazy("horizon:mistral:workflows:change_definition")
    success_url = reverse_lazy('horizon:mistral:workflows:update')
    page_title = _("Update Definition")

    def get_form_kwargs(self):
        kwargs = super(ChangeDefinitionView, self).get_form_kwargs()
        kwargs['next_view'] = UpdateView

        return kwargs


class CreateView(forms.ModalFormView):
    template_name = 'mistral/workflows/create.html'
    modal_header = _("Create Workflow")
    form_id = "create_workflow"
    form_class = mistral_forms.CreateForm
    submit_label = _("Create")
    submit_url = reverse_lazy("horizon:mistral:workflows:create")
    success_url = reverse_lazy('horizon:mistral:workflows:index')
    page_title = _("Create Workflow")

    def get_initial(self):
        initial = {}

        if 'definition' in self.kwargs:
            initial['definition'] = self.kwargs['definition']

        return initial


class UpdateView(CreateView):
    template_name = 'mistral/workflows/update.html'
    modal_header = _("Update Workflow")
    form_id = "update_workflow"
    form_class = mistral_forms.UpdateForm
    submit_label = _("Update")
    submit_url = reverse_lazy("horizon:mistral:workflows:update")
    page_title = _("Update Workflow")

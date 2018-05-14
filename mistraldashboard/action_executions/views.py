# Copyright 2016 - Nokia.
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

from django.urls import reverse
from django.urls import reverse_lazy

from django.utils.translation import ugettext_lazy as _
from django.views import generic

from horizon import exceptions
from horizon import forms
from horizon import tables

from mistraldashboard.action_executions import forms as action_execution_forms
from mistraldashboard.action_executions import tables as mistral_tables
from mistraldashboard import api
from mistraldashboard.default import utils
from mistraldashboard import forms as mistral_forms


def get_single_action_execution_data(request, **kwargs):
    try:
        action_execution_id = kwargs['action_execution_id']
        action_execution = api.action_execution_get(
            request,
            action_execution_id
        )
    except Exception:
        msg = _('Unable to get action execution "%s".') % action_execution_id
        redirect = reverse('horizon:mistral:action_execution:index')
        exceptions.handle(request, msg, redirect=redirect)

    return action_execution


class OverviewView(generic.TemplateView):
    template_name = 'mistral/action_executions/detail.html'
    page_title = _("Action Execution Details")
    workflow_url = 'horizon:mistral:workflows:detail'
    task_execution_url = 'horizon:mistral:tasks:detail'

    def get_context_data(self, **kwargs):
        context = super(OverviewView, self).get_context_data(**kwargs)
        action_execution = get_single_action_execution_data(
            self.request,
            **kwargs
        )
        if action_execution.workflow_name:
            action_execution.workflow_url = reverse(
                self.workflow_url,
                args=[action_execution.workflow_name])
        if action_execution.task_execution_id:
            action_execution.task_execution_url = reverse(
                self.task_execution_url,
                args=[action_execution.task_execution_id]
            )
        if action_execution.input:
            action_execution.input = utils.prettyprint(action_execution.input)
        if action_execution.output:
            action_execution.output = utils.prettyprint(
                action_execution.output
            )
        if action_execution.state:
            action_execution.state = utils.label(action_execution.state)
        action_execution.accepted = utils.booleanfield(
            action_execution.accepted
        )

        breadcrumb = [(action_execution.id, reverse(
            'horizon:mistral:action_executions:detail',
            args=[action_execution.id]
        ))]

        context["custom_breadcrumb"] = breadcrumb
        context['action_execution'] = action_execution

        return context


class CodeView(forms.ModalFormView):
    template_name = 'mistral/default/code.html'
    modal_header = _("Code view")
    form_id = "code_view"
    form_class = mistral_forms.EmptyForm
    cancel_label = "OK"
    cancel_url = reverse_lazy("horizon:mistral:action_executions:index")
    page_title = _("Code view")

    def get_context_data(self, **kwargs):
        context = super(CodeView, self).get_context_data(**kwargs)
        column = self.kwargs['column']
        action_execution = get_single_action_execution_data(
            self.request,
            **self.kwargs
        )
        io = {}

        if column == 'input':
            io['name'] = _('Input')
            io['value'] = utils.prettyprint(action_execution.input)
        elif column == 'output':
            io['name'] = _('Output')
            io['value'] = (
                utils.prettyprint(action_execution.output)
                if action_execution.output
                else _("No available output yet")
            )

        context['io'] = io

        return context


class IndexView(tables.DataTableView):
    table_class = mistral_tables.ActionExecutionsTable
    template_name = 'mistral/action_executions/index.html'

    def get_data(self):

        return api.action_executions_list(self.request)


class UpdateView(forms.ModalFormView):
    template_name = 'mistral/action_executions/update.html'
    modal_header = _("Update Action Execution")
    form_id = "update_action_execution"
    form_class = action_execution_forms.UpdateForm
    submit_label = _("Update")
    success_url = reverse_lazy("horizon:mistral:action_executions:index")
    submit_url = "horizon:mistral:action_executions:update"
    cancel_url = "horizon:mistral:action_executions:index"
    page_title = _("Update Action Execution")

    def get_initial(self):
        return {"action_execution_id": self.kwargs["action_execution_id"]}

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(
            self.submit_url,
            args=[self.kwargs["action_execution_id"]]
        )

        return context


class FilteredByTaskView(tables.DataTableView):
    table_class = mistral_tables.ActionExecutionsTable
    template_name = 'mistral/action_executions/filtered.html'
    data = {}

    def get_data(self, **kwargs):
        try:
            task_id = self.kwargs['task_id']
            data = api.action_executions_list(self.request, task_id)
        except Exception:
            msg = (
                _('Unable to get action execution by task id "%s".') % task_id
            )
            redirect = reverse('horizon:mistral:action_executions:index')
            exceptions.handle(self.request, msg, redirect=redirect)

        return data

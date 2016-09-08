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
from mistraldashboard.default.utils import prettyprint
from mistraldashboard import forms as mistral_forms
from mistraldashboard.tasks import tables as mistral_tables


def get_single_task_data(request, **kwargs):
    try:
        task_id = kwargs['task_id']
        task = api.task_get(request, task_id)
    except Exception:
        msg = _('Unable to get task "%s".') % task_id
        redirect = reverse('horizon:mistral:tasks:index')
        exceptions.handle(request, msg, redirect=redirect)

    return task


class ExecutionView(tables.DataTableView):
    table_class = mistral_tables.TaskTable
    template_name = 'mistral/tasks/filtered.html'

    def get_data(self, **kwargs):
        try:
            execution_id = self.kwargs['task_id']
            tasks = api.task_list(self.request, execution_id)
        except Exception:
            msg = _('Unable to get task by execution id "%s".') % execution_id
            redirect = reverse('horizon:mistral:executions:index')
            exceptions.handle(self.request, msg, redirect=redirect)

        return tasks


class OverviewView(generic.TemplateView):
    template_name = 'mistral/tasks/detail.html'
    page_title = _("Task Details")
    workflow_url = 'horizon:mistral:workflows:detail'
    execution_url = 'horizon:mistral:executions:detail'

    def get_context_data(self, **kwargs):
        context = super(OverviewView, self).get_context_data(**kwargs)
        task = get_single_task_data(self.request, **kwargs)
        task.workflow_url = reverse(self.workflow_url,
                                    args=[task.workflow_name])
        task.execution_url = reverse(self.execution_url,
                                     args=[task.workflow_execution_id])
        task.result = prettyprint(task.result)
        task.published = prettyprint(task.published)
        context['task'] = task

        return context


class CodeView(forms.ModalFormView):
    template_name = 'mistral/default/code.html'
    modal_header = _("Code view")
    form_id = "code_view"
    form_class = mistral_forms.EmptyForm
    cancel_label = "OK"
    cancel_url = reverse_lazy("horizon:mistral:tasks:index")
    page_title = _("Code view")

    def get_context_data(self, **kwargs):
        context = super(CodeView, self).get_context_data(**kwargs)
        column = self.kwargs['column']
        task = get_single_task_data(self.request, **self.kwargs)
        io = {}

        if column == 'result':
            io['name'] = _('Result')
            io['value'] = task.result = prettyprint(task.result)
        elif column == 'published':
            io['name'] = _('Published')
            io['value'] = task.published = prettyprint(task.published)

        context['io'] = io

        return context


class IndexView(tables.DataTableView):
    table_class = mistral_tables.TaskTable
    template_name = 'mistral/tasks/index.html'

    def get_data(self):

        return api.task_list(self.request)

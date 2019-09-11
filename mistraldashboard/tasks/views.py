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

from django.urls import reverse
from django.urls import reverse_lazy

from django.utils.translation import gettext_lazy as _
from django.views import generic

from horizon import exceptions
from horizon import forms
from horizon import tables

from mistraldashboard import api
from mistraldashboard.default import utils

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
            execution_id = self.kwargs['execution_id']
            tasks = api.task_list(self.request, execution_id)
        except Exception:
            msg = _('Unable to get task by execution id "%s".') % execution_id
            redirect = reverse('horizon:mistral:executions:index')
            exceptions.handle(self.request, msg, redirect=redirect)

        return tasks


class OverviewView(generic.TemplateView):
    template_name = 'mistral/tasks/detail.html'
    page_title = _("Task Details")
    workflow_detail_url = 'horizon:mistral:workflows:detail'
    workflow_execution_tasks_url = 'horizon:mistral:executions:tasks'
    execution_url = 'horizon:mistral:executions:detail'
    action_execution_url = 'horizon:mistral:action_executions:task'

    def get_context_data(self, **kwargs):
        context = super(OverviewView, self).get_context_data(**kwargs)
        task = get_single_task_data(self.request, **kwargs)
        task.workflow_detail_url = reverse(self.workflow_detail_url,
                                           args=[task.workflow_name])
        task.execution_url = reverse(self.execution_url,
                                     args=[task.workflow_execution_id])
        task.result = utils.prettyprint(task.result)
        task.published = utils.prettyprint(task.published)
        task.state = utils.label(task.state)
        if task.type == "ACTION":
            task.type_url = reverse(
                self.action_execution_url,
                args=[task.id]
            )
        elif task.type == "WORKFLOW":
            task.type_url = reverse(
                self.workflow_execution_tasks_url,
                args=[task.id]
            )

        breadcrumb = [(task.id, reverse(
            'horizon:mistral:tasks:detail',
            args=[task.id]
        ))]

        context["custom_breadcrumb"] = breadcrumb
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
            io['value'] = task.result = utils.prettyprint(task.result)
        elif column == 'published':
            io['name'] = _('Published')
            io['value'] = task.published = utils.prettyprint(task.published)

        context['io'] = io

        return context


class IndexView(tables.DataTableView):
    table_class = mistral_tables.TaskTable
    template_name = 'mistral/tasks/index.html'

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        tasks = []
        prev_marker = self.request.GET.get(
            mistral_tables.TaskTable._meta.prev_pagination_param,
            None
        )

        if prev_marker is not None:
            sort_dir = 'asc'
            marker = prev_marker
        else:
            sort_dir = 'desc'
            marker = self.request.GET.get(
                mistral_tables.TaskTable._meta.pagination_param,
                None
            )

        try:
            tasks, self._more, self._prev = api.pagination_list(
                entity="tasks",
                request=self.request,
                marker=marker,
                sort_dirs=sort_dir,
                paginate=True
            )

            if prev_marker is not None:
                tasks = sorted(
                    tasks,
                    key=lambda execution: getattr(
                        execution, 'created_at'
                    ),
                    reverse=True
                )

        except Exception as e:
            self._prev = False
            self._more = False
            msg = _('Unable to retrieve tasks list: %s') % e
            exceptions.handle(self.request, msg)

        return tasks

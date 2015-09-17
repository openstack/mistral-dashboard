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
from django.utils.translation import ugettext_lazy as _
from django.views import generic


from horizon import exceptions
from horizon import tables

from mistraldashboard import api
from mistraldashboard.default.utils import prettyprint
from mistraldashboard.tasks.tables import TaskTable


class ExecutionView(generic.TemplateView):
    template_name = 'mistral/tasks/execution.html'
    page_title = _("Execution Overview")

    def get_context_data(self, **kwargs):
        context = super(ExecutionView, self).get_context_data(**kwargs)
        task = self.get_data(self.request, **kwargs)
        execution = api.execution_get(self.request, task.workflow_execution_id)
        execution.input = prettyprint(execution.input)
        execution.output = prettyprint(execution.output)
        execution.params = prettyprint(execution.params)

        context['task'] = task
        context['execution'] = execution

        return context

    def get_data(self, request, **kwargs):
        try:
            task_id = kwargs['task_id']
            task = api.task_get(request, task_id)
        except Exception:
            msg = _('Unable to get task "%s".') % task_id
            redirect = reverse('horizon:mistral:tasks:index')
            exceptions.handle(self.request, msg, redirect=redirect)

        return task


class OverviewView(generic.TemplateView):
    template_name = 'mistral/tasks/detail.html'
    page_title = _("Task Details")

    def get_context_data(self, **kwargs):
        context = super(OverviewView, self).get_context_data(**kwargs)
        task = self.get_data(self.request, **kwargs)
        task.result = prettyprint(task.result)
        context['task'] = task
        return context

    def get_data(self, request, **kwargs):
        try:
            task_id = kwargs['task_id']
            task = api.task_get(request, task_id)
        except Exception:
            msg = _('Unable to get task "%s".') % task_id
            redirect = reverse('horizon:mistral:tasks:index')
            exceptions.handle(self.request, msg, redirect=redirect)

        return task


class IndexView(tables.DataTableView):
    table_class = TaskTable
    template_name = 'mistral/tasks/index.html'

    def get_data(self):

        return api.task_list(self.request)

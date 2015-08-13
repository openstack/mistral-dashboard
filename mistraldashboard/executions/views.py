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

from django.views import generic

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables

from mistraldashboard import api
from mistraldashboard.default.utils import prettyprint
from mistraldashboard.executions.tables import ExecutionsTable
from mistraldashboard.executions.tables import TaskTable


class IndexView(tables.DataTableView):
    table_class = ExecutionsTable
    template_name = 'mistral/executions/index.html'

    def get_data(self):
        return api.execution_list(self.request)


class TaskView(tables.DataTableView):
    table_class = TaskTable
    template_name = 'mistral/executions/index.html'

    def get_data(self):
        return api.task_list(self.request, self.kwargs['execution_id'])


class DetailView(generic.TemplateView):
    template_name = 'mistral/executions/detail.html'
    page_title = _("Execution Overview")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        execution = self.get_data(self.request, **kwargs)
        execution.input = prettyprint(execution.input)
        execution.output = prettyprint(execution.output)
        execution.params = prettyprint(execution.params)
        context['execution'] = execution
        return context

    def get_data(self, request, **kwargs):
        try:
            execution_id = kwargs['execution_id']
            execution = api.execution_get(request, execution_id)
        except Exception:
            msg = _('Unable to get execution "%s".') % execution_id
            redirect = reverse('horizon:mistral:executions:index')
            exceptions.handle(self.request, msg, redirect=redirect)

        return execution

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
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tables

from mistraldashboard import api
from mistraldashboard.default.utils import prettyprint
from mistraldashboard.executions import forms as m_forms
from mistraldashboard.executions import tables as mistral_tables
from mistraldashboard import forms as mistral_forms


def get_single_data(request, id, type="execution"):
    """Get Execution or Task data by ID.

    :param request: Request data
    :param id: Entity ID
    :param type: Request dispatch flag, Default: Execution
    """

    if type == "execution":
        try:
            execution = api.execution_get(request, id)
        except Exception:
            msg = _('Unable to get execution by its ID"%s".') % id
            redirect = reverse('horizon:mistral:executions:index')
            exceptions.handle(request, msg, redirect=redirect)

        return execution

    elif type == "task":
        try:
            task = api.task_get(request, id)
        except Exception:
            msg = _('Unable to get task by its ID "%s".') % id
            redirect = reverse('horizon:mistral:tasks:index')
            exceptions.handle(request, msg, redirect=redirect)

        return task

    elif type == "task_by_execution":
        try:
            task = api.task_list(request, id)[0]
        except Exception:
            msg = _('Unable to get task by Execution ID "%s".') % id
            redirect = reverse('horizon:mistral:executions:index')
            exceptions.handle(request, msg, redirect=redirect)

        return task


class IndexView(tables.DataTableView):
    table_class = mistral_tables.ExecutionsTable
    template_name = 'mistral/executions/index.html'

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        executions = []
        prev_marker = self.request.GET.get(
            mistral_tables.ExecutionsTable._meta.prev_pagination_param,
            None
        )

        if prev_marker is not None:
            sort_dir = 'asc'
            marker = prev_marker
        else:
            sort_dir = 'desc'
            marker = self.request.GET.get(
                mistral_tables.ExecutionsTable._meta.pagination_param,
                None
            )

        try:
            executions, self._more, self._prev = api.pagination_list(
                entity="executions",
                request=self.request,
                marker=marker,
                sort_dirs=sort_dir,
                paginate=True
            )

            if prev_marker is not None:
                executions = sorted(
                    executions,
                    key=lambda execution: getattr(
                        execution, 'created_at'
                    ),
                    reverse=True
                )

        except Exception:
            self._prev = False
            self._more = False
            msg = _('Unable to retrieve executions list.')
            exceptions.handle(self.request, msg)

        return executions


class DetailView(generic.TemplateView):
    template_name = 'mistral/executions/detail.html'
    page_title = _("Execution Overview")
    workflow_url = 'horizon:mistral:workflows:detail'
    task_url = 'horizon:mistral:tasks:execution'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        task = {}
        execution = {}
        if 'caller' in kwargs:
            if kwargs['caller'] == 'task':
                kwargs['task_id'] = kwargs['execution_id']
                del kwargs['execution_id']
                task = get_single_data(
                    self.request,
                    kwargs['task_id'],
                    "task"
                )
                execution = get_single_data(
                    self.request,
                    task.workflow_execution_id,
                )
        else:
            execution = get_single_data(
                self.request,
                kwargs['execution_id'],
            )
            task = get_single_data(
                self.request,
                self.kwargs['execution_id'],
                "task_by_execution"
            )

        execution.workflow_url = reverse(self.workflow_url,
                                         args=[execution.workflow_name])
        execution.input = prettyprint(execution.input)
        execution.output = prettyprint(execution.output)
        execution.params = prettyprint(execution.params)
        task.url = reverse(self.task_url, args=[execution.id])
        context['execution'] = execution
        context['task'] = task

        return context


class CodeView(forms.ModalFormView):
    template_name = 'mistral/default/code.html'
    modal_header = _("Code view")
    form_id = "code_view"
    form_class = mistral_forms.EmptyForm
    cancel_label = "OK"
    cancel_url = reverse_lazy("horizon:mistral:executions:index")
    page_title = _("Code view")

    def get_context_data(self, **kwargs):
        context = super(CodeView, self).get_context_data(**kwargs)
        execution = get_single_data(
            self.request,
            self.kwargs['execution_id'],
        )
        column = self.kwargs['column']
        io = {}
        if column == 'input':
            io['name'] = _('Input')
            io['value'] = execution.input = prettyprint(execution.input)
        elif column == 'output':
            io['name'] = _('Output')
            io['value'] = execution.output = prettyprint(execution.output)
        context['io'] = io

        return context


class UpdateDescriptionView(forms.ModalFormView):
    template_name = 'mistral/executions/update_description.html'
    modal_header = _("Update Execution Description")
    form_id = "update_execution_description"
    form_class = m_forms.UpdateDescriptionForm
    submit_label = _("Update")
    success_url = reverse_lazy("horizon:mistral:executions:index")
    submit_url = "horizon:mistral:executions:update_description"
    cancel_url = "horizon:mistral:executions:index"
    page_title = _("Update Execution Description")

    def get_initial(self):
        return {"execution_id": self.kwargs["execution_id"]}

    def get_context_data(self, **kwargs):
        context = super(UpdateDescriptionView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(
            self.submit_url,
            args=[self.kwargs["execution_id"]]
        )

        return context

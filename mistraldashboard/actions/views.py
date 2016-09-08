# Copyright 2015 Huawei Technologies Co., Ltd.
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

from mistraldashboard.actions import forms as mistral_forms
from mistraldashboard.actions import tables as mistral_tables
from mistraldashboard import api


class CreateView(forms.ModalFormView):
    template_name = 'mistral/actions/create.html'
    modal_header = _("Create Action")
    form_id = "create_action"
    form_class = mistral_forms.CreateForm
    submit_label = _("Create")
    submit_url = reverse_lazy("horizon:mistral:actions:create")
    success_url = reverse_lazy('horizon:mistral:actions:index')
    page_title = _("Create Action")


class UpdateView(forms.ModalFormView):
    template_name = 'mistral/actions/update.html'
    modal_header = _("Update Action")
    form_id = "update_action"
    form_class = mistral_forms.UpdateForm
    submit_label = _("Update")
    submit_url = reverse_lazy("horizon:mistral:actions:update")
    success_url = reverse_lazy('horizon:mistral:actions:index')
    page_title = _("Update Action")


class IndexView(tables.DataTableView):
    table_id = "workflow_action"
    table_class = mistral_tables.ActionsTable
    template_name = 'mistral/actions/index.html'

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        actions = []
        prev_marker = self.request.GET.get(
            mistral_tables.ActionsTable._meta.prev_pagination_param,
            None
        )

        if prev_marker is not None:
            sort_dir = 'asc'
            marker = prev_marker
        else:
            sort_dir = 'desc'
            marker = self.request.GET.get(
                mistral_tables.ActionsTable._meta.pagination_param,
                None
            )

        try:
            actions, self._more, self._prev = api.pagination_list(
                entity="actions",
                request=self.request,
                marker=marker,
                sort_keys='name',
                sort_dirs=sort_dir,
                paginate=True,
                reversed_order=True
            )

            if prev_marker is not None:
                actions = sorted(
                    actions,
                    key=lambda action: getattr(
                        action, 'name'
                    ),
                    reverse=False
                )

        except Exception as e:
            self._prev = False
            self._more = False
            msg = _('Unable to retrieve actions list: %s') % str(e)
            exceptions.handle(self.request, msg)

        return actions


class DetailView(generic.TemplateView):
    template_name = 'mistral/actions/detail.html'
    page_title = _("Action Definition")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        action = self.get_data(self.request, **kwargs)
        context['action'] = action

        return context

    def get_data(self, request, **kwargs):
        try:
            action_name = kwargs['action_name']
            action = api.action_get(request, action_name)
        except Exception:
            msg = _('Unable to get action "%s".') % action_name
            redirect = reverse('horizon:mistral:actions:index')
            exceptions.handle(self.request, msg, redirect=redirect)

        return action


class RunView(forms.ModalFormView):
    form_class = mistral_forms.RunForm
    template_name = 'mistral/actions/run.html'
    form_id = "run_action"
    success_url = reverse_lazy("horizon:mistral:actions:index")
    submit_label = _("Run")
    modal_header = _("Run Action")
    page_title = _("Run Action")
    submit_url = "horizon:mistral:actions:run"

    def get_initial(self, **kwargs):
        return {'action_name': self.kwargs['action_name']}

    def get_context_data(self, **kwargs):
        context = super(RunView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(
            self.submit_url,
            args=[self.kwargs["action_name"]]
        )

        return context

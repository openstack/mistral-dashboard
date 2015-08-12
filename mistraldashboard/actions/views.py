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
from mistraldashboard.actions.tables import ActionsTable
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
    table_class = ActionsTable
    template_name = 'mistral/actions/index.html'

    def get_data(self):
        return api.action_list(self.request)


class DetailView(generic.TemplateView):
    template_name = 'mistral/actions/detail.html'
    page_title = _("Action Definition")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        action = self.get_data(self.request, **kwargs)
        context['definition'] = action.definition

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

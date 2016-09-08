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
from mistraldashboard.workbooks import forms as mistral_forms
from mistraldashboard.workbooks import tables as mistral_tables


class IndexView(tables.DataTableView):
    table_class = mistral_tables.WorkbooksTable
    template_name = 'mistral/workbooks/index.html'

    def get_data(self):
        return api.workbook_list(self.request)


class DetailView(generic.TemplateView):
    template_name = 'mistral/workbooks/detail.html'
    page_title = _("Workbook Definition")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        workbook = self.get_data(self.request, **kwargs)
        context['definition'] = workbook.definition

        return context

    def get_data(self, request, **kwargs):
        try:
            workbook_name = kwargs['workbook_name']
            workbook = api.workbook_get(request, workbook_name)
        except Exception:
            msg = _('Unable to get workbook "%s".') % workbook_name
            redirect = reverse('horizon:mistral:workbooks:index')
            exceptions.handle(self.request, msg, redirect=redirect)

        return workbook


class SelectDefinitionView(forms.ModalFormView):
    template_name = 'mistral/workbooks/select_definition.html'
    modal_header = _("Create Workbook")
    form_id = "select_definition"
    form_class = mistral_forms.DefinitionForm
    submit_label = _("Next")
    submit_url = reverse_lazy("horizon:mistral:workbooks:select_definition")
    success_url = reverse_lazy('horizon:mistral:workbooks:create')
    page_title = _("Select Definition")

    def get_form_kwargs(self):
        kwargs = super(SelectDefinitionView, self).get_form_kwargs()
        kwargs['next_view'] = CreateView

        return kwargs


class ChangeDefinitionView(SelectDefinitionView):
    modal_header = _("Update Workbook")
    submit_url = reverse_lazy("horizon:mistral:workbooks:change_definition")
    success_url = reverse_lazy('horizon:mistral:workbooks:update')
    page_title = _("Update Definition")

    def get_form_kwargs(self):
        kwargs = super(ChangeDefinitionView, self).get_form_kwargs()
        kwargs['next_view'] = UpdateView

        return kwargs


class CreateView(forms.ModalFormView):
    template_name = 'mistral/workbooks/create.html'
    modal_header = _("Create Workbook")
    form_id = "create_workbook"
    form_class = mistral_forms.CreateForm
    submit_label = _("Create")
    submit_url = reverse_lazy("horizon:mistral:workbooks:create")
    success_url = reverse_lazy('horizon:mistral:workbooks:index')
    page_title = _("Create Workbook")

    def get_initial(self):
        initial = {}

        if 'definition' in self.kwargs:
            initial['definition'] = self.kwargs['definition']

        return initial


class UpdateView(CreateView):
    template_name = 'mistral/workbooks/update.html'
    modal_header = _("Update Workbook")
    form_id = "update_workbook"
    form_class = mistral_forms.UpdateForm
    submit_label = _("Update")
    submit_url = reverse_lazy("horizon:mistral:workbooks:update")
    page_title = _("Update Workbook")

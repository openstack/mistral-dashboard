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

from django.core.urlresolvers import reverse_lazy

from horizon import tables
from horizon import forms

from mistraldashboard import api
from mistraldashboard.workbooks.tables import WorkbooksTable
from mistraldashboard.workbooks.forms import ExecuteForm


class IndexView(tables.DataTableView):
    table_class = WorkbooksTable
    template_name = 'mistral/workbooks/index.html'

    def get_data(self):
        return api.mistralclient(self.request).workbooks.list()


class ExecuteView(forms.ModalFormView):
    form_class = ExecuteForm
    template_name = 'mistral/workbooks/execute.html'
    success_url = reverse_lazy("horizon:mistral:executions:index")

    def get_context_data(self, **kwargs):
        context = super(ExecuteView, self).get_context_data(**kwargs)
        context["workbook_name"] = self.kwargs['workbook_name']
        return context

    def get_initial(self, **kwargs):
        return {
            'workbook_name': self.kwargs['workbook_name']
        }

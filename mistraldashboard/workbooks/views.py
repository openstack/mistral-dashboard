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
from mistraldashboard.workbooks.tables import WorkbooksTable


class IndexView(tables.DataTableView):
    table_class = WorkbooksTable
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

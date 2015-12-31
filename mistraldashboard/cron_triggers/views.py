# -*- coding: utf-8 -*-
#
# Copyright 2016 - Alcatel-Lucent.
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

from horizon import tables

from mistraldashboard import api
from mistraldashboard.cron_triggers.tables import CronTriggersTable


class OverviewView(generic.TemplateView):
    template_name = 'mistral/cron_triggers/detail.html'
    page_title = _("Cron Trigger Details")
    workflow_url = 'horizon:mistral:workflows:detail'
    list_url = 'horizon:mistral:cron_triggers:index'

    def get_context_data(self, **kwargs):
        context = super(OverviewView, self).get_context_data(**kwargs)
        cron_trigger = {}
        cron_trigger = api.cron_trigger_get(
            self.request,
            kwargs['cron_trigger_name']
        )
        cron_trigger.workflow_url = reverse(
            self.workflow_url,
            args=[cron_trigger.workflow_name]
        )
        cron_trigger.list_url = reverse_lazy(self.list_url)
        context['cron_trigger'] = cron_trigger

        return context


class IndexView(tables.DataTableView):
    table_class = CronTriggersTable
    template_name = 'mistral/cron_triggers/index.html'

    def get_data(self):
        return api.cron_trigger_list(self.request)

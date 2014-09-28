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

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from horizon import exceptions
from horizon import forms
from horizon import messages

from mistraldashboard import api


class ExecuteForm(forms.SelfHandlingForm):
    workflow_name = forms.CharField(
        label=_("Workflow"),
        required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    workflow_input = forms.CharField(
        label=_("Input"),
        required=False,
        initial="{}",
        widget=forms.widgets.Textarea()
    )
    task_name = forms.CharField(
        label=_("Task name"),
        required=False,
        widget=forms.TextInput()
    )

    def handle(self, request, data):
        try:
            ex = api.mistralclient(request).executions.create(**data)

            msg = _('Execution has been created with id "%s".') % ex.id
            messages.success(request, msg)

            return True
        except Exception:
            msg = _('Failed to execute workflow "%s".') % data['workflow_name']
            redirect = reverse('horizon:mistral:workflows:index')
            exceptions.handle(request, msg, redirect=redirect)

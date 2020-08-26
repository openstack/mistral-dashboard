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

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

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
    task_name = forms.CharField(
        label=_("Task name"),
        required=False,
        widget=forms.TextInput()
    )

    def __init__(self, *args, **kwargs):
        super(ExecuteForm, self).__init__(*args, **kwargs)
        self._generate_parameter_fields(kwargs["initial"]["parameter_list"])

    def _generate_parameter_fields(self, list):
        self.workflow_parameters = []
        for entry in list.split(","):
            label, _, default = entry.partition("=")
            label = label.strip()
            if label != '':
                self.workflow_parameters.append(label)
                if default == "None":
                    default = None
                    required = False
                else:
                    required = True
                self.fields[label] = forms.CharField(label=label,
                                                     required=required,
                                                     initial=default)

    def handle(self, request, data):
        try:
            data['workflow_identifier'] = data.pop('workflow_name')
            data['workflow_input'] = {}
            for param in self.workflow_parameters:
                value = data.pop(param)
                if value == "":
                    value = None
                data['workflow_input'][param] = value
            ex = api.execution_create(request, **data)

            msg = _('Execution has been created with id "%s".') % ex.id
            messages.success(request, msg)

            return True
        except Exception:
            msg = _('Failed to execute workflow.')
            redirect = reverse('horizon:mistral:workflows:index')
            exceptions.handle(request, msg, redirect=redirect)


class DefinitionForm(forms.SelfHandlingForm):
    definition_source = forms.ChoiceField(
        label=_('Definition Source'),
        choices=[('file', _('File')),
                 ('raw', _('Direct Input'))],
        widget=forms.Select(
            attrs={'class': 'switchable',
                   'data-slug': 'definitionsource'})
    )
    definition_upload = forms.FileField(
        label=_('Definition File'),
        help_text=_('A local definition to upload.'),
        widget=forms.FileInput(
            attrs={'class': 'switched',
                   'data-switch-on': 'definitionsource',
                   'data-required-when-shown': 'true',
                   'data-definitionsource-file': _('Definition File')}
        ),
        required=False
    )
    definition_data = forms.CharField(
        label=_('Definition Data'),
        help_text=_('The raw contents of the definition.'),
        widget=forms.widgets.Textarea(
            attrs={'class': 'switched',
                   'data-switch-on': 'definitionsource',
                   'data-required-when-shown': 'true',
                   'data-definitionsource-raw': _('Definition Data'),
                   'rows': 4}
        ),
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.next_view = kwargs.pop('next_view')
        super(DefinitionForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(DefinitionForm, self).clean()

        if cleaned_data.get('definition_upload'):
            files = self.request.FILES
            cleaned_data['definition'] = files['definition_upload'].read()
        elif cleaned_data.get('definition_data'):
            cleaned_data['definition'] = cleaned_data['definition_data']
        else:
            raise forms.ValidationError(
                _('You must specify the definition source.'))
        try:
            validated = api.workflow_validate(
                self.request,
                cleaned_data['definition']
            )
        except Exception as e:
            raise forms.ValidationError(str(e))

        if not validated.get('valid'):
            raise forms.ValidationError(
                validated.get('error', _('Validated failed')))

        return cleaned_data

    def handle(self, request, data):
        kwargs = {'definition': data['definition']}
        request.method = 'GET'

        return self.next_view.as_view()(request, **kwargs)


class CreateForm(forms.SelfHandlingForm):
    definition = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={'rows': 12}
        ),
        required=False
    )

    def handle(self, request, data):
        try:
            api.workflow_create(request, data['definition'])
            msg = _('Successfully created workflow.')
            messages.success(request, msg)

            return True
        except Exception:
            msg = _('Failed to create workflow.')
            redirect = reverse('horizon:mistral:workflows:index')
            exceptions.handle(request, msg, redirect=redirect)


class UpdateForm(CreateForm):

    def handle(self, request, data):
        try:
            api.workflow_update(request, data['definition'])
            msg = _('Successfully updated workflow.')
            messages.success(request, msg)

            return True
        except Exception:
            msg = _('Failed to update workflow.')
            redirect = reverse('horizon:mistral:workflows:index')
            exceptions.handle(request, msg, redirect=redirect)

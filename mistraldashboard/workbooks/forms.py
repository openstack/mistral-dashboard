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

import six

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from mistraldashboard import api


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
            validated = api.workbook_validate(
                self.request,
                cleaned_data['definition']
            )
        except Exception as e:
            raise forms.ValidationError(six.text_type(e))

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
            attrs={'readonly': 'readonly',
                   'rows': 12}
        ),
        required=False
    )

    def handle(self, request, data):
        try:
            api.workbook_create(request, data['definition'])
            msg = _('Successfully created workbook.')
            messages.success(request, msg)

            return True
        except Exception:
            msg = _('Failed to create workbook.')
            redirect = reverse('horizon:mistral:workbooks:index')
            exceptions.handle(request, msg, redirect=redirect)


class UpdateForm(CreateForm):

    def handle(self, request, data):
        try:
            api.workbook_update(request, data['definition'])
            msg = _('Successfully updated workbook.')
            messages.success(request, msg)

            return True
        except Exception:
            msg = _('Failed to update workbook.')
            redirect = reverse('horizon:mistral:workbooks:index')
            exceptions.handle(request, msg, redirect=redirect)

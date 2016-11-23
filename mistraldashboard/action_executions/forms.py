# Copyright 2016 - Nokia.
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

from horizon import forms

from mistraldashboard import api
from mistraldashboard.handle_errors import handle_errors


class UpdateForm(forms.SelfHandlingForm):
    action_execution_id = forms.CharField(label=_("Action Execution ID"),
                                          widget=forms.HiddenInput(),
                                          required=False)
    output_source = forms.ChoiceField(
        label=_('Output'),
        help_text=_('Content for output. '
                    'Select either file, raw content or Null value.'),
        choices=[('null', _('<null> (sends empty value)')),
                 ('file', _('File')),
                 ('raw', _('Direct Input'))],
        widget=forms.Select(
            attrs={'class': 'switchable',
                   'data-slug': 'outputsource'}
        ),
        required=False
    )
    output_upload = forms.FileField(
        label=_('Output File'),
        help_text=_('A local output to upload'),
        widget=forms.FileInput(
            attrs={'class': 'switched',
                   'data-switch-on': 'outputsource',
                   'data-outputsource-file': _('Output File')}
        ),
        required=False
    )
    output_data = forms.CharField(
        label=_('Output Data'),
        help_text=_('The raw content for output'),
        widget=forms.widgets.Textarea(
            attrs={'class': 'switched',
                   'data-switch-on': 'outputsource',
                   'data-outputsource-raw': _('Output Data'),
                   'rows': 4}
        ),
        required=False
    )

    state = forms.ChoiceField(
        label=_('State'),
        help_text=_('Select state to update'),
        choices=[('null', _('<null> (sends empty value)')),
                 ('SUCCESS', _('Success')),
                 ('ERROR', _('Error'))],
        widget=forms.Select(
            attrs={'class': 'switchable'}
        ),
        required=False

    )

    def clean(self):
        cleaned_data = super(UpdateForm, self).clean()
        cleaned_data['output'] = None

        if cleaned_data.get('output_upload'):
            files = self.request.FILES
            cleaned_data['output'] = files['output_upload'].read()
        elif cleaned_data.get('output_data'):
            cleaned_data['output'] = cleaned_data['output_data']
        elif cleaned_data.get('output_source') == 'null':
            cleaned_data['output'] = None

        del cleaned_data['output_upload']
        del cleaned_data['output_data']
        del cleaned_data['output_source']

        if cleaned_data['state'] == 'null':
            cleaned_data['state'] = None

        return cleaned_data

    @handle_errors(_("Unable to update Action Execution"), [])
    def handle(self, request, data):
            return api.action_execution_update(
                request,
                data['action_execution_id'],
                data['state'],
                data['output'],
            )

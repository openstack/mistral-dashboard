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

from horizon import exceptions
from horizon import forms
from horizon import messages

from mistraldashboard import api


class UpdateDescriptionForm(forms.SelfHandlingForm):
    execution_id = forms.CharField(label=_("Execution ID"),
                                   widget=forms.HiddenInput(),
                                   required=False)
    description = forms.CharField(max_length=255,
                                  label=_("Execution description"))

    def handle(self, request, data):
        try:
            api.execution_update(
                request,
                data["execution_id"],
                "description",
                data["description"])
            msg = _('Successfully updated execution description.')
            messages.success(request, msg)

            return True

        except Exception:
            msg = _('Failed to update execution description.')
            redirect = reverse('horizon:mistral:executions:index')
            exceptions.handle(request, msg, redirect=redirect)

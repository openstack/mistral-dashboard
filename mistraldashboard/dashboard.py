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

from django.utils.translation import gettext_lazy as _

import horizon

from mistraldashboard.default import panel


class MistralDashboard(horizon.Dashboard):
    name = _("Workflow")
    slug = "mistral"
    panels = (
        'default',
        'workbooks',
        'workflows',
        'actions',
        'executions',
        'tasks',
        'action_executions',
        'cron_triggers',
    )
    default_panel = 'default'
    roles = ('admin',)


horizon.register(MistralDashboard)
MistralDashboard.register(panel.Default)

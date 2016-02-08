# Copyright 2016 - Nokia.
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
from django.utils.translation import ungettext_lazy

from horizon import tables

from mistraldashboard import api
from mistraldashboard.default.utils import humantime


class CreateCronTrigger(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Cron Trigger")
    url = "horizon:mistral:cron_triggers:create"
    classes = ("ajax-modal",)
    icon = "plus"


class DeleteCronTrigger(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Cron Trigger",
            u"Delete Cron Triggers",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Cron Trigger",
            u"Deleted Cron Triggers",
            count
        )

    def delete(self, request, cron_trigger_name):
        api.cron_trigger_delete(request, cron_trigger_name)


class WorkflowColumn(tables.Column):
    def get_link_url(self, datum):
        workflow_url = "horizon:mistral:workflows:detail"
        obj_id = datum.workflow_name
        return reverse(workflow_url, args=[obj_id])


class CronTriggersTable(tables.DataTable):
    id = tables.Column(
        "id",
        verbose_name=_("ID"),
        link="horizon:mistral:cron_triggers:detail"
    )
    name = tables.Column(
        "name",
        verbose_name=_("Name")
    )
    workflow_name = WorkflowColumn(
        "workflow_name",
        verbose_name=_("Workflow"),
        link=True
    )
    pattern = tables.Column(
        "pattern",
        verbose_name=_("Pattern"),
    )
    next_execution_time = tables.Column(
        "next_execution_time",
        verbose_name=_("Next Execution Time"),
    )
    remaining_executions = tables.Column(
        "remaining_executions",
        verbose_name=_("Remaining Executions"),
    )
    first_execution_time = tables.Column(
        "first_execution_time",
        verbose_name=_("First Execution Time"),
    )
    created_at = tables.Column(
        "created_at",
        verbose_name=_("Created at"),
        filters=[humantime]
    )
    updated_at = tables.Column(
        "updated_at",
        verbose_name=_("Updated at"),
        filters=[humantime]
    )

    def get_object_id(self, datum):
        return datum.name

    class Meta(object):
        name = "cron trigger"
        verbose_name = _("Cron Trigger")
        table_actions = (
            tables.FilterAction,
            CreateCronTrigger,
            DeleteCronTrigger
        )
        row_actions = (DeleteCronTrigger,)

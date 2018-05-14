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

from django.urls import reverse

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import exceptions
from horizon import tables

from mistraldashboard import api
from mistraldashboard.default import smart_cell
from mistraldashboard.default import utils

smart_cell.init()


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, id):
        try:
            instance = api.action_execution_get(request, id)
        except Exception as e:
            msg = _("Unable to get action execution by ID %(id)s: %(e)s.") % {
                'id': id, 'e': str(e)
            }
            exceptions.handle(request, msg)

        return instance


class DeleteActionExecution(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Action Execution",
            u"Delete Action Executions",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Action Execution",
            u"Deleted Action Executions",
            count
        )

    def delete(self, request, action_execution_id):
        api.action_execution_delete(request, action_execution_id)


class UpdateActionExecution(tables.LinkAction):
    name = "updateAE"
    verbose_name = _("Update")
    url = "horizon:mistral:action_executions:update"
    classes = ("ajax-modal",)


class TaskExecutionIDColumn(tables.Column):
    def get_link_url(self, datum):
        task_url = "horizon:mistral:tasks:detail"
        obj_id = datum.task_execution_id
        return reverse(task_url, args=[obj_id])


class WorkflowNameColumn(tables.Column):
    def get_link_url(self, datum):
        workflow_url = "horizon:mistral:workflows:detail"
        obj_id = datum.workflow_name
        return reverse(workflow_url, args=[obj_id])


class ActionExecutionsTable(tables.DataTable):

    def getHoverHelp(data):
        if hasattr(data, 'state_info') and data.state_info:

                return {'title': data.state_info}

    STATE_STATUS_CHOICES = (
        ("success", True),
        ("error", False),
        ("idle", None),
        ("running", None),
        ("canceled", None),
    )

    id = tables.Column(
        "id",
        verbose_name=_("ID"),
        link="horizon:mistral:action_executions:detail"
    )
    name = tables.Column(
        "name",
        verbose_name=_("Name")
    )
    tags = tables.Column(
        "tags",
        verbose_name=_("Tags")
    )
    workflow_name = WorkflowNameColumn(
        "workflow_name",
        verbose_name=_("Workflow Name"),
        link=True
    )
    task_execution_id = TaskExecutionIDColumn(
        "task_execution_id",
        verbose_name=_("Task Execution ID"),
        link=True
    )
    task_name = tables.Column(
        "task_name",
        verbose_name=_("Task name")
    )
    description = tables.Column(
        "description",
        verbose_name=_("Description")
    )
    input = tables.Column(
        "",
        verbose_name=_("Input"),
        empty_value=_("View"),
        link="horizon:mistral:action_executions:input",
        link_classes=("ajax-modal",)
    )
    output = tables.Column(
        "",
        verbose_name=_("Output"),
        empty_value=_("View"),
        link="horizon:mistral:action_executions:output",
        link_classes=("ajax-modal",)
    )
    created_at = tables.Column(
        "created_at",
        verbose_name=_("Created at"),
        filters=[utils.humantime]
    )
    updated_at = tables.Column(
        "updated_at",
        verbose_name=_("Updated at"),
        filters=[utils.humantime]
    )
    accepted = tables.Column(
        "accepted",
        verbose_name=_("Accepted"),
        filters=[utils.booleanfield],
    )
    state = tables.Column(
        "state",
        status=True,
        status_choices=STATE_STATUS_CHOICES,
        verbose_name=_("State"),
        filters=[utils.label],
        cell_attributes_getter=getHoverHelp
    )

    class Meta(object):
        name = "actionExecutions"
        verbose_name = _("Action Executions")
        status_columns = ["state"]
        row_class = UpdateRow
        table_actions = (
            tables.FilterAction,
            DeleteActionExecution
        )
        row_actions = (UpdateActionExecution, DeleteActionExecution)

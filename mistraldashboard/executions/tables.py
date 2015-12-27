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
from django.utils.translation import ungettext_lazy

from horizon import exceptions
from horizon import tables

from mistraldashboard import api
import mistraldashboard.default.SmartCell as SmartCell
from mistraldashboard.default.utils import humantime
from mistraldashboard.default.utils import label

SmartCell.init()


class DeleteExecution(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Execution",
            u"Delete Executions",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Execution",
            u"Deleted Executions",
            count
        )

    def delete(self, request, execution_name):
        api.execution_delete(request, execution_name)


class CancelExecution(tables.BatchAction):
    name = "cancel execution"
    classes = ("btn-danger",)

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Cancel Execution",
            u"Cancel Executions",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Canceled Execution",
            u"Canceled Executions",
            count
        )

    def allowed(self, request, instance):
        if instance.state == "RUNNING":
            return True
        return False

    def action(self, request, obj_id):
        api.execution_update(request, obj_id, "state", "ERROR")


class PauseExecution(tables.BatchAction):
    name = "pause execution"

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Pause Execution",
            u"Pause Executions",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Paused Execution",
            u"Paused Executions",
            count
        )

    def allowed(self, request, instance):
        if instance.state == "RUNNING":
            return True
        return False

    def action(self, request, obj_id):
        api.execution_update(request, obj_id, "state", "PAUSED")


class ResumeExecution(tables.BatchAction):
    name = "resume execution"

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Resume Execution",
            u"Resume Executions",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Resumed Execution",
            u"Resumed Executions",
            count
        )

    def allowed(self, request, instance):
        if instance.state == "PAUSED":
            return True
        return False

    def action(self, request, obj_id):
        api.execution_update(request, obj_id, "state", "RUNNING")


class UpdateDescription(tables.LinkAction):
    name = "updateDescription"
    verbose_name = _("Update Description")
    url = "horizon:mistral:executions:update_description"
    classes = ("ajax-modal",)


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, id):
        try:
            instance = api.execution_get(request, id)
        except Exception as e:
            msg = _("Unable to get execution by ID %(id)s: %(e)s.") % {
                'id': id, 'e': str(e)
            }
            exceptions.handle(request, msg)

        return instance


class ExecutionsTable(tables.DataTable):

    def getHoverHelp(data):
        if hasattr(data, 'state_info') and data.state_info:

                return {'title': data.state_info}

    STATE_STATUS_CHOICES = (
        ("success", True),
        ("error", False),
        ("paused", False),
        ("delayed", None),
        ("running", None),
    )

    id = tables.Column(
        "id",
        verbose_name=_("ID"),
        link="horizon:mistral:executions:detail"
    )

    workflow_name = tables.Column(
        "workflow_name",
        verbose_name=_("Workflow")
    )

    task = tables.Column(
        "task",
        verbose_name=_("Tasks"),
        empty_value=_("View"),
        link="horizon:mistral:tasks:execution"
    )

    input = tables.Column(
        "",
        verbose_name=_("Input"),
        empty_value=_("View"),
        link="horizon:mistral:executions:input",
        link_classes=("ajax-modal",)
    )

    output = tables.Column(
        "",
        verbose_name=_("Output"),
        empty_value=_("View"),
        link="horizon:mistral:executions:output",
        link_classes=("ajax-modal",)
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

    state = tables.Column(
        "state",
        verbose_name=_("State"),
        filters=[label],
        status=True,
        status_choices=STATE_STATUS_CHOICES,
        cell_attributes_getter=getHoverHelp
    )

    class Meta(object):
        name = "executions"
        verbose_name = _("Executions")
        status_columns = ["state"]
        row_class = UpdateRow
        table_actions = (DeleteExecution, tables.FilterAction)
        row_actions = (DeleteExecution, UpdateDescription,
                       PauseExecution, CancelExecution,
                       ResumeExecution, DeleteExecution)

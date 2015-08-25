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

from horizon import tables

from mistraldashboard import api
from mistraldashboard.default.utils import humantime
from mistraldashboard.default.utils import label


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


class ExecutionsTable(tables.DataTable):
    id = tables.Column(
        "id",
        verbose_name=_("ID"),
        link="horizon:mistral:executions:detail"
    )

    workflow_name = tables.Column("workflow_name", verbose_name=_("Workflow"))

    task = tables.Column(
        "task",
        verbose_name=_("Tasks"),
        empty_value=_("View"),
        link="horizon:mistral:executions:tasks"
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
        filters=[label])

    class Meta(object):
        name = "executions"
        verbose_name = _("Executions")
        table_actions = (DeleteExecution, tables.FilterAction)
        row_actions = (DeleteExecution,)


class TaskTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"))
    name = tables.Column("name", verbose_name=_("Name"))

    parameters = tables.Column("parameters", verbose_name=_("Parameters"))
    output = tables.Column("output", verbose_name=_("Output"))

    created_at = tables.Column("created_at", verbose_name=_("Created at"))
    updated_at = tables.Column("updated_at", verbose_name=_("Updated at"))

    state = tables.Column("state", verbose_name=_("State"), filters=[label])

    class Meta(object):
        name = "tasks"
        verbose_name = _("Tasks")

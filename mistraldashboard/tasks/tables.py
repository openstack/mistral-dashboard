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

from horizon import exceptions
from horizon import tables

from mistraldashboard import api
import mistraldashboard.default.SmartCell as SmartCell
from mistraldashboard.default.utils import humantime
from mistraldashboard.default.utils import label

SmartCell.init()


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, id):
        try:
            instance = api.task_get(request, id)
        except Exception as e:
            msg = _("Unable to get task by ID %(id)s: %(e)s.") % {
                'id': id, 'e': str(e)
            }
            exceptions.handle(request, msg)

        return instance


class TaskTable(tables.DataTable):

    def getHoverHelp(data):
        if hasattr(data, 'state_info') and data.state_info:

                return {'title': data.state_info}

    STATE_STATUS_CHOICES = (
        ("success", True),
        ("error", False),
        ("idle", None),
        ("running", None),
    )

    id = tables.Column(
        "id",
        verbose_name=_("ID"),
        link="horizon:mistral:tasks:detail"
    )
    name = tables.Column(
        "name",
        verbose_name=_("Name")
    )
    workflow_execution_id = tables.Column(
        "workflow_execution_id",
        verbose_name=_("Workflow Execution ID"),
        link="horizon:mistral:executions:detail_task_id"
    )
    result = tables.Column(
        "",
        verbose_name=_("Result"),
        empty_value=_("View"),
        link="horizon:mistral:tasks:result",
        link_classes=("ajax-modal",)
    )
    published = tables.Column(
        "",
        verbose_name=_("Published"),
        empty_value=_("View"),
        link="horizon:mistral:tasks:published",
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
        status=True,
        status_choices=STATE_STATUS_CHOICES,
        verbose_name=_("State"),
        filters=[label],
        cell_attributes_getter=getHoverHelp
    )

    class Meta(object):
        name = "tasks"
        verbose_name = _("Tasks")
        table_actions = (tables.FilterAction,)
        status_columns = ["state"]
        row_class = UpdateRow

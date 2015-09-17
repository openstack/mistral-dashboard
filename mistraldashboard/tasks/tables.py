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

from horizon import tables

from mistraldashboard.default.utils import humantime
from mistraldashboard.default.utils import label


class TaskTable(tables.DataTable):
    id = tables.Column(
        "id",
        verbose_name=_("ID"),
        link="horizon:mistral:tasks:detail")
    name = tables.Column("name", verbose_name=_("Name"))

    workflow_execution_id = tables.Column(
        "workflow_execution_id",
        verbose_name=_("Workflow Execution ID"),
        link="horizon:mistral:tasks:execution"
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

    state = tables.Column("state", verbose_name=_("State"), filters=[label])

    class Meta(object):
        name = "tasks"
        verbose_name = _("Tasks")
        table_actions = (tables.FilterAction,)

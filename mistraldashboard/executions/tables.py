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

from mistraldashboard.default.utils import label
from mistraldashboard.default.utils import humantime
from mistraldashboard.default.utils import prettyprint


class ExecutionsTable(tables.DataTable):
    id = tables.Column(
        "id",
        verbose_name=_("ID"),
        link="horizon:mistral:executions:tasks"
    )

    workflow_name = tables.Column("workflow_name", verbose_name=_("Workflow"))

    input = tables.Column(
        "input",
        verbose_name=_("Input"),
        filters=[prettyprint]
    )
    output = tables.Column(
        "output",
        verbose_name=_("Output"),
        filters=[prettyprint]
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

    class Meta:
        name = "executions"
        verbose_name = _("Executions")


class TaskTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"))
    name = tables.Column("name", verbose_name=_("Name"))

    parameters = tables.Column("parameters", verbose_name=_("Parameters"))
    output = tables.Column("output", verbose_name=_("Output"))

    created_at = tables.Column("created_at", verbose_name=_("Created at"))
    updated_at = tables.Column("updated_at", verbose_name=_("Updated at"))

    state = tables.Column("state", verbose_name=_("State"), filters=[label])

    class Meta:
        name = "tasks"
        verbose_name = _("Tasks")

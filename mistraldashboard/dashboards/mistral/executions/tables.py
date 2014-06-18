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
from django.template.loader import render_to_string

from horizon import tables


TYPES = {
    'SUCCESS': 'label-success',
    'ERROR': 'label-important'
}


def label(x):
    return render_to_string("mistral/executions/_label.html",
                            {"label": x,
                             "type": TYPES.get(x)})


class ExecutionsTable(tables.DataTable):
    id = tables.Column("id",
                       verbose_name=_("ID"),
                       link=("horizon:mistral:executions:tasks"))
    wb_name = tables.Column("workbook_name", verbose_name=_("Workbook"))
    state = tables.Column("state", verbose_name=_("State"), filters=[label])

    class Meta:
        name = "executions"
        verbose_name = _("Executions")


class TaskTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"))
    name = tables.Column("name", verbose_name=_("Name"))
    parameters = tables.Column("parameters", verbose_name=_("Parameters"))
    output = tables.Column("output", verbose_name=_("Output"))
    state = tables.Column("state", verbose_name=_("State"), filters=[label])

    class Meta:
        name = "tasks"
        verbose_name = _("Tasks")

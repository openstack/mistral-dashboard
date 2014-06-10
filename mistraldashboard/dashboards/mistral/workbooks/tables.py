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


class ExecuteWorkflow(tables.LinkAction):
    name = "execute"
    verbose_name = _("Execute")
    url = "horizon:mistral:workbooks:execute"
    classes = ("ajax-modal", "btn-edit")


def tags_to_string(workbook):
    return ', '.join(workbook.tags)


class WorkbooksTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"))
    description = tables.Column("description", verbose_name=_("Description"))
    tags = tables.Column(tags_to_string, verbose_name=_("Tags"))

    def get_object_id(self, datum):
        return datum.name

    class Meta:
        name = "workbooks"
        verbose_name = _("Workbooks")
        row_actions = (ExecuteWorkflow,)

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
from horizon.utils import filters

from mistraldashboard import api


class CreateWorkbook(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Workbook")
    url = "horizon:mistral:workbooks:select_definition"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateWorkbook(tables.LinkAction):
    name = "update"
    verbose_name = _("Update Workbook")
    url = "horizon:mistral:workbooks:change_definition"
    classes = ("ajax-modal",)
    icon = "pencil"


class DeleteWorkbook(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Workbook",
            u"Delete Workbooks",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Workbook",
            u"Deleted Workbooks",
            count
        )

    def delete(self, request, workbook_name):
        api.workbook_delete(request, workbook_name)


def tags_to_string(workbook):
    return ', '.join(workbook.tags) if workbook.tags else None


class WorkbooksTable(tables.DataTable):
    name = tables.Column(
        "name",
        verbose_name=_("Name"),
        link="horizon:mistral:workbooks:detail"
    )
    tags = tables.Column(tags_to_string, verbose_name=_("Tags"))
    created = tables.Column(
        "created_at",
        verbose_name=_("Created"),
        filters=(
            filters.parse_isotime,
            filters.timesince_or_never
        )
    )
    updated = tables.Column(
        "updated_at",
        verbose_name=_("Updated"),
        filters=(
            filters.parse_isotime,
            filters.timesince_or_never
        )
    )

    def get_object_id(self, datum):
        return datum.name

    class Meta(object):
        name = "workbooks"
        verbose_name = _("Workbooks")
        table_actions = (
            CreateWorkbook,
            UpdateWorkbook,
            DeleteWorkbook,
            tables.FilterAction
        )
        row_actions = (DeleteWorkbook,)

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


class CreateWorkflow(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Workflow")
    url = "horizon:mistral:workflows:select_definition"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateWorkflow(tables.LinkAction):
    name = "update"
    verbose_name = _("Update Workflow")
    url = "horizon:mistral:workflows:change_definition"
    classes = ("ajax-modal",)
    icon = "pencil"


class DeleteWorkflow(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Workflow",
            u"Delete Workflows",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Workflow",
            u"Deleted Workflows",
            count
        )

    def delete(self, request, workflow_name):
        api.workflow_delete(request, workflow_name)


class ExecuteWorkflow(tables.LinkAction):
    name = "execute"
    verbose_name = _("Execute")
    url = "horizon:mistral:workflows:execute"
    classes = ("ajax-modal", "btn-edit")


def tags_to_string(workflow):
    return ', '.join(workflow.tags) if workflow.tags else None


def cut(workflow, length=100):
    inputs = workflow.input

    if inputs and len(inputs) > length:
        return "%s..." % inputs[:length]
    else:
        return inputs


class WorkflowsTable(tables.DataTable):
    name = tables.Column(
        "name",
        verbose_name=_("Name"),
        link="horizon:mistral:workflows:detail"
    )
    tags = tables.Column(
        tags_to_string,
        verbose_name=_("Tags")
    )
    inputs = tables.Column(
        cut,
        verbose_name=_("Input")
    )
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
        name = "workflows"
        verbose_name = _("Workflows")
        table_actions = (
            CreateWorkflow,
            UpdateWorkflow,
            DeleteWorkflow,
            tables.FilterAction
        )
        row_actions = (ExecuteWorkflow, DeleteWorkflow)

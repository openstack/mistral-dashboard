# Copyright 2015 Huawei Technologies Co., Ltd.
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


class CreateAction(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Action")
    url = "horizon:mistral:actions:create"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateAction(tables.LinkAction):
    name = "update"
    verbose_name = _("Update Action")
    url = "horizon:mistral:actions:update"
    classes = ("ajax-modal",)
    icon = "pencil"


class DeleteAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Action",
            u"Delete Actions",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Action",
            u"Deleted Actions",
            count
        )

    def delete(self, request, action_name):
        api.action_delete(request, action_name)

    def allowed(self, request, action=None):
        if action:
            return not action.is_system
        else:
            return True


def tags_to_string(action):
    return ', '.join(action.tags) if action.tags else None


def cut(action, length=100):
    inputs = action.input

    if inputs and len(inputs) > length:
        return "%s..." % inputs[:length]
    else:
        return inputs


class RunAction(tables.LinkAction):
    name = "run"
    verbose_name = _("Run")
    url = "horizon:mistral:actions:run"
    classes = ("ajax-modal",)


class ActionsTable(tables.DataTable):
    name = tables.Column(
        "name",
        verbose_name=_("Name"),
        link="horizon:mistral:actions:detail"
    )
    is_system = tables.Column(
        "is_system",
        verbose_name=_("Is System")
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

    class Meta(object):
        name = "actions"
        verbose_name = _("Actions")
        table_actions = (
            CreateAction,
            UpdateAction,
            DeleteAction,
            tables.FilterAction,
        )
        row_actions = (RunAction, DeleteAction)

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

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from horizon.utils import memoized

from mistralclient.api import client as mistral_client
from mistraldashboard.handle_errors import handle_errors

SERVICE_TYPE = 'workflowv2'


@memoized.memoized
def mistralclient(request):
    return mistral_client.client(
        username=request.user.username,
        auth_token=request.user.token.id,
        project_id=request.user.tenant_id,
        # Ideally, we should get it from identity endpoint, but since
        # python-mistralclient is not supporting v2.0 API it might create
        # additional troubles for those who still rely on v2.0 stack-wise.
        auth_url=getattr(settings, 'OPENSTACK_KEYSTONE_URL'),
        # Todo: add SECONDARY_ENDPOINT_TYPE support
        endpoint_type=getattr(
            settings,
            'OPENSTACK_ENDPOINT_TYPE',
            'internalURL'
        ),
        service_type=SERVICE_TYPE
    )


def execution_create(request, **data):
    """Creates new execution."""

    return mistralclient(request).executions.create(**data)


@handle_errors(_("Unable to retrieve executions."), [])
def execution_list(request):
    """Returns all executions."""

    return mistralclient(request).executions.list()


@handle_errors(_("Unable to retrieve tasks."), [])
def task_list(request, execution_id=None):
    """Returns all tasks.

    :param execution_id: Workflow execution ID associated with list of tasks
    """

    return mistralclient(request).tasks.list(execution_id)


@handle_errors(_("Unable to retrieve workflows."), [])
def workflow_list(request):
    """Returns all workflows."""

    return mistralclient(request).workflows.list()


@handle_errors(_("Unable to retrieve workbooks."), [])
def workbook_list(request):
    """Returns all workbooks."""

    return mistralclient(request).workbooks.list()

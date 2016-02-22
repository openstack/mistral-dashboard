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

import itertools

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from horizon.utils import functions as utils
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


@handle_errors(_("Unable to retrieve list"), [])
def pagination_list(entity, request, marker='', sort_keys='', sort_dirs='asc',
                    paginate=False, reversed_order=False):
    """Retrieve a listing of specific entity and handles pagination.

    :param entity: Requested entity (String)
    :param request: Request data
    :param marker: Pagination marker for large data sets: entity id
    :param sort_keys: Columns to sort results by
    :param sort_dirs: Sorting Directions (asc/desc). Default:asc
    :param paginate: If true will perform pagination based on settings.
                     Default:False
    :param reversed_order: flag to reverse list. Default:False
    """

    limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
    page_size = utils.get_page_size(request)

    if paginate:
        request_size = page_size + 1
    else:
        request_size = limit

    if reversed_order:
        sort_dirs = 'desc' if sort_dirs == 'asc' else 'asc'

    api = mistralclient(request)
    entities_iter = getattr(api, entity).list(
        marker, limit, sort_keys, sort_dirs
    )

    has_prev_data = has_more_data = False

    if paginate:
        entities = list(itertools.islice(entities_iter, request_size))
        # first and middle page condition
        if len(entities) > page_size:
            entities.pop(-1)
            has_more_data = True
            # middle page condition
            if marker is not None:
                has_prev_data = True
        # first page condition when reached via prev back
        elif reversed_order and marker is not None:
            has_more_data = True
        # last page condition
        elif marker is not None:
            has_prev_data = True

        # restore the original ordering here
        if reversed_order:
            entities = sorted(entities,
                              key=lambda ent:
                                  (getattr(ent, sort_keys) or '').lower(),
                              reverse=(sort_dirs == 'desc')
                              )
    else:
        entities = list(entities_iter)

    return entities, has_more_data, has_prev_data


def execution_create(request, **data):
    """Creates new execution."""

    return mistralclient(request).executions.create(**data)


def execution_get(request, execution_id):
    """Get specific execution.

    :param execution_id: Execution ID
    """

    return mistralclient(request).executions.get(execution_id)


def execution_update(request, execution_id, field, value):
    """update specific execution field, either state or description.

    :param request: Request data
    :param execution_id: Execution ID
    :param field: flag - either Execution state or description
    :param value: new update value
    """

    if field == "state":
        return mistralclient(request).\
            executions.update(execution_id, value)
    elif field == "description":
        return mistralclient(request).\
            executions.update(execution_id, None, value)


def execution_delete(request, execution_name):
    """Delete execution.

    :param execution_name: Execution name
    """

    return mistralclient(request).executions.delete(execution_name)


@handle_errors(_("Unable to retrieve tasks."), [])
def task_list(request, execution_id=None):
    """Returns all tasks.

    :param execution_id: Workflow execution ID associated with list of tasks
    """

    return mistralclient(request).tasks.list(execution_id)


def task_get(request, task_id=None):
    """Get specific task.

    :param task_id: Task ID
    """

    return mistralclient(request).tasks.get(task_id)


@handle_errors(_("Unable to retrieve workflows"), [])
def workflow_list(request):
    """Returns all workflows."""

    return mistralclient(request).workflows.list()


def workflow_get(request, workflow_name):
    """Get specific workflow.

    :param workflow_name: Workflow name
    """

    return mistralclient(request).workflows.get(workflow_name)


def workflow_create(request, workflows_definition):
    """Create workflow.

    :param workflows_definition: Workflows definition
    """

    return mistralclient(request).workflows.create(workflows_definition)


def workflow_validate(request, workflow_definition):
    """Validate workflow.

    :param workflow_definition: Workflow definition
    """

    return mistralclient(request).workflows.validate(workflow_definition)


def workflow_delete(request, workflow_name):
    """Delete workflow.

    :param workflow_name: Workflow name
    """

    return mistralclient(request).workflows.delete(workflow_name)


def workflow_update(request, workflows_definition):
    """Update workflow.

    :param workflows_definition: Workflows definition
    """

    return mistralclient(request).workflows.update(workflows_definition)


@handle_errors(_("Unable to retrieve workbooks."), [])
def workbook_list(request):
    """Returns all workbooks."""

    return mistralclient(request).workbooks.list()


def workbook_get(request, workbook_name):
    """Get specific workbook.

    :param workbook_name: Workbook name
    """

    return mistralclient(request).workbooks.get(workbook_name)


def workbook_create(request, workbook_definition):
    """Create workbook.

    :param workbook_definition: Workbook definition
    """

    return mistralclient(request).workbooks.create(workbook_definition)


def workbook_validate(request, workbook_definition):
    """Validate workbook.

    :param workbook_definition: Workbook definition
    """

    return mistralclient(request).workbooks.validate(workbook_definition)


def workbook_delete(request, workbook_name):
    """Delete workbook.

    :param workbook_name: Workbook name
    """

    return mistralclient(request).workbooks.delete(workbook_name)


def workbook_update(request, workbook_definition):
    """Update workbook.

    :param workbook_definition: Workbook definition
    """

    return mistralclient(request).workbooks.update(workbook_definition)


@handle_errors(_("Unable to retrieve actions."), [])
def action_list(request):
    """Returns all actions."""

    return mistralclient(request).actions.list()


def action_get(request, action_name):
    """Get specific action.

    :param action_name: Action name
    """

    return mistralclient(request).actions.get(action_name)


def action_create(request, action_definition):
    """Create action.

    :param action_definition: Action definition
    """

    return mistralclient(request).actions.create(action_definition)


def action_update(request, action_definition):
    """Update action.

    :param action_definition: Action definition
    """

    return mistralclient(request).actions.update(action_definition)


def action_run(request, action_name, input, params):
    """Run specific action execution.

    :param action_name: Action name
    :param input: input
    :param params: params
    """

    return mistralclient(request).action_executions.create(
        action_name,
        input,
        **params
    )


def action_delete(request, action_name):
    """Delete action.

    :param action_name: Action name
    """

    return mistralclient(request).actions.delete(action_name)


@handle_errors(_("Unable to retrieve cron trigger list"), [])
def cron_trigger_list(request):
    """Returns all cron triggers.

    :param request: Request data
    """

    return mistralclient(request).cron_triggers.list()


@handle_errors(_("Unable to retrieve cron trigger"), [])
def cron_trigger_get(request, cron_trigger_name):
    """Get specific cron trigger.

    :param request: Request data
    :param cron_trigger_name: Cron trigger name
    """

    return mistralclient(request).cron_triggers.get(cron_trigger_name)


@handle_errors(_("Unable to delete cron trigger/s"), [])
def cron_trigger_delete(request, cron_trigger_name):
    """Delete Cron Trigger.

    :param request: Request data
    :param cron_trigger_name: Cron Trigger name
    """

    return mistralclient(request).cron_triggers.delete(cron_trigger_name)


def cron_trigger_create(
    request,
    cron_trigger_name,
    workflow_ID,
    workflow_input,
    workflow_params,
    pattern,
    first_time,
    count
):
    """Create Cron Trigger.

    :param request: Request data
    :param cron_trigger_name: Cron Trigger name
    :param workflow_ID: Workflow ID
    :param workflow_input: Workflow input
    :param workflow_params: Workflow params <* * * * *>
    :param pattern: <* * * * *>
    :param first_time:
           Date and time of the first execution <YYYY-MM-DD HH:MM>
    :param count: Number of wanted executions <integer>
    """

    return mistralclient(request).cron_triggers.create(
        cron_trigger_name,
        workflow_ID,
        workflow_input,
        workflow_params,
        pattern,
        first_time,
        count
    )

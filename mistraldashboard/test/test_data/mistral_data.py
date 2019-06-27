# Copyright 2015 Huawei Technologies Co., Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from mistralclient.api.v2 import action_executions
from mistralclient.api.v2 import actions
from mistralclient.api.v2 import cron_triggers
from mistralclient.api.v2 import executions
from mistralclient.api.v2 import tasks
from mistralclient.api.v2 import workbooks
from mistralclient.api.v2 import workflows

from openstack_dashboard.test.test_data import utils as test_data_utils


# Workbooks
WB_DEF = """
---
version: 2.0

name: wb

workflows:
  wf1:
    type: direct
    input:
      - param1
      - param2

    tasks:
      task1:
        action: std.http url="localhost:8989"
        on-success:
          - test_subsequent

      test_subsequent:
        action: std.http url="http://some_url" server_id=1
""".strip()

# Workflows
WF_DEF = """
version: '2.0'

flow:
  tasks:
    task1:
      action: nova.servers_get server="1"
""".strip()


def data(TEST):
    # MistralActions
    TEST.mistralclient_actions = test_data_utils.TestDataContainer()
    action_1 = actions.Action(
        actions.ActionManager(None),
        {'name': 'a',
         'id': '1',
         'is_system': True,
         'input': 'param1',
         'description': 'my cool action',
         'tags': ['test'],
         'definition': '1',
         'created_at': '1',
         'updated_at': '1'
         }
    )
    TEST.mistralclient_actions.add(action_1)

    # MistralExecutions
    TEST.mistralclient_executions = test_data_utils.TestDataContainer()
    execution_1 = executions.Execution(
        executions.ExecutionManager(None),
        {'id': '123',
         'workflow_name': 'my_wf',
         'description': '',
         'state': 'RUNNING',
         'input': '{"person": {"first_name": "John", "last_name": "Doe"}}',
         'output': "1",
         'params': "1",
         }
    )
    TEST.mistralclient_executions.add(execution_1)

    # Tasks
    TEST.mistralclient_tasks = test_data_utils.TestDataContainer()
    task_1 = tasks.Task(
        tasks.TaskManager(None),
        {'id': '1',
         'workflow_execution_id': '123',
         'name': 'my_task',
         'workflow_name': 'my_wf',
         'state': 'RUNNING',
         'type': 'ACTION',
         'tags': ['deployment', 'demo'],
         'result': "1",
         'published': '{"a":"1"}'})
    TEST.mistralclient_tasks.add(task_1)

    # Workbooks
    TEST.mistralclient_workbooks = test_data_utils.TestDataContainer()
    workbook_1 = workbooks.Workbook(
        workbooks.WorkbookManager(None),
        {'name': 'a',
         'tags': ['a', 'b'],
         'created_at': '1',
         'updated_at': '1',
         'definition': WB_DEF}
    )
    TEST.mistralclient_workbooks.add(workbook_1)

    # Workflows
    TEST.mistralclient_workflows = test_data_utils.TestDataContainer()
    workflow_1 = workflows.Workflow(
        workflows.WorkflowManager(None),
        {'name': 'a',
         'id': '1',
         'tags': ['a', 'b'],
         'input': 'param',
         'created_at': '1',
         'updated_at': '1',
         'definition': WF_DEF}
    )
    TEST.mistralclient_workflows.add(workflow_1)

    # MistralActionsExecutions
    TEST.mistralclient_action_executions = test_data_utils.TestDataContainer()
    action_executions_1 = action_executions.ActionExecution(
        action_executions.ActionExecutionManager(None),
        {'id': '1',
         'name': 'a',
         'tags': ['a', 'b'],
         'workflow_name': 'my work flow',
         'task_execution_id': '1',
         'task_name': 'b',
         'input': "1",
         'output': "1",
         'description': '',
         'created_at': '1',
         'updated_at': '1',
         'accepted': True,
         'state': 'SUCCESS'
         }
    )
    TEST.mistralclient_action_executions.add(action_executions_1)

    # MistralCronTriggers
    TEST.mistralclient_cron_triggers = test_data_utils.TestDataContainer()
    cron_triggers_1 = cron_triggers.CronTrigger(
        cron_triggers.CronTriggerManager(None),
        {'id': '1',
         'name': 'a',
         'workflow_name': 'my work flow',
         'pattern': '',
         'next_execution_time': '',
         'remaining_executions': '',
         'first_execution_time': '',
         'created_at': '1',
         'updated_at': '1'
         })
    TEST.mistralclient_cron_triggers.add(cron_triggers_1)

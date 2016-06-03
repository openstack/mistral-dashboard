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

from horizon import tables

from mistraldashboard import api
from mistraldashboard.executions.tables import ExecutionsTable
from mistraldashboard.executions.tables import TaskTable
import yaml
import json


class IndexView(tables.DataTableView):
    table_class = ExecutionsTable
    template_name = 'mistral/executions/index.html'

    def get_data(self):
        return api.mistralclient(self.request).executions.list()


class TaskView(tables.DataTableView):
    table_class = TaskTable
    template_name = 'mistral/execution/index.html'

    def _get_tasks_definition(self, cli):
        execution = cli.executions.get(self.kwargs['execution_id'])
        exec_input =  json.loads(execution.input)
        workflow = cli.workflows.get(execution.workflow_name)
        definition = yaml.load(workflow.definition)
        tasks_definitions = definition[definition.keys()[0]]["tasks"]
        return tasks_definitions, exec_input

    def _get_tasks_inputs(self, tasks_definitions, task):
        inputs = {}
        action_tag = tasks_definitions[task.name]["action"]
        task_inputs = action_tag.partition(' ')[2]
        if len(task_inputs) == 0:
            task_inputs = tasks_definitions[task.name]["input"]
            for key, val in task_inputs.iteritems():
                if type(val) == type(""):
                    val = val.replace("<% $.", "").replace(" %>", "")
                inputs[key] = val
        else:
            for input in task_inputs.split(" %> "):
                param = input.replace(" %>", "").split("=<% $.")
                if len(param) == 2:
                    inputs[param[0]] = param[1]
        return inputs

    def get_data(self):
        tasks_outputs = {}
        cli = api.mistralclient(self.request)
        task_list = cli.tasks.list(self.kwargs['execution_id'])
        tasks_definitions, exec_input = self._get_tasks_definition(cli)
        for task in task_list:
            #get the data published by the tasks
            tasks_outputs.update(json.loads(task.published))
        for task in task_list:
            task_input = {}
            inputs = self._get_tasks_inputs(tasks_definitions, task)
            for key, val in inputs.iteritems():
                if key.__contains__("password"):
                    task_input[key] = "*********"
                    continue
                try:
                    task_input[key] = exec_input[val]
                except KeyError:
                    #find the output in tasks published results
                    task_input[key] = tasks_outputs.get(val)
            task.parameters = json.dumps(task_input, ensure_ascii=False).encode('utf-8')
            if task.state == "ERROR":
                task.rerun = "re-run"
            else:
                task.rerun = ""
        return task_list

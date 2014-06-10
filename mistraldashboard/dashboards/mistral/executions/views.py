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

from mistraldashboard.dashboards.mistral import api
from mistraldashboard.dashboards.mistral.executions.tables \
    import ExecutionsTable
from mistraldashboard.dashboards.mistral.executions.tables import TaskTable


class IndexView(tables.DataTableView):
    table_class = ExecutionsTable
    template_name = 'mistral/executions/index.html'

    def get_data(self):
        client = api.mistralclient(self.request)
        return [item for wb in client.workbooks.list()
                for item in client.executions.list(wb.name)]


class TaskView(tables.DataTableView):
    table_class = TaskTable
    template_name = 'mistral/executions/index.html'

    def get_data(self):
        client = api.mistralclient(self.request)
        return [item for wb in client.workbooks.list()
                for item in client.tasks.list(wb.name,
                                              self.kwargs['execution_id'])]

# Copyright 2016 - Nokia.
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

from django.urls import re_path

from mistraldashboard.action_executions import views

ACTION_EXECUTIONS = r'^(?P<action_execution_id>[^/]+)/%s$'
TASKS = r'^(?P<task_id>[^/]+)/%s$'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(ACTION_EXECUTIONS % 'detail', views.OverviewView.as_view(),
            name='detail'),
    re_path(ACTION_EXECUTIONS % 'input', views.CodeView.as_view(),
            {'column': 'input'}, name='input'),
    re_path(ACTION_EXECUTIONS % 'output', views.CodeView.as_view(),
            {'column': 'output'}, name='output'),
    re_path(ACTION_EXECUTIONS % 'update', views.UpdateView.as_view(),
            name='update'),
    re_path(TASKS % 'task', views.FilteredByTaskView.as_view(),
            name='task')
]

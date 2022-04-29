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

from django.urls import re_path

from mistraldashboard.executions import views

EXECUTIONS = r'^(?P<execution_id>[^/]+)/%s$'
TASKS = r'^(?P<task_execution_id>[^/]+)/%s$'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(EXECUTIONS % 'detail', views.DetailView.as_view(), name='detail'),
    re_path(TASKS % 'tasks', views.TasksView.as_view(), name='tasks'),
    re_path(EXECUTIONS % 'detail_task_id', views.DetailView.as_view(),
            {'caller': 'task'}, name='detail_task_id'),
    re_path(EXECUTIONS % 'output', views.CodeView.as_view(),
            {'column': 'output'}, name='output'),
    re_path(EXECUTIONS % 'input', views.CodeView.as_view(),
            {'column': 'input'}, name='input'),
    re_path(EXECUTIONS % 'update_description',
            views.UpdateDescriptionView.as_view(),
            name='update_description'),
]

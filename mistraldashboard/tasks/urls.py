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

from mistraldashboard.tasks import views

TASKS = r'^(?P<task_id>[^/]+)/%s$'
EXECUTIONS = r'^(?P<execution_id>[^/]+)/%s$'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(TASKS % 'detail', views.OverviewView.as_view(), name='detail'),
    re_path(EXECUTIONS % 'execution',
            views.ExecutionView.as_view(),
            name='execution'),
    re_path(TASKS % 'result', views.CodeView.as_view(),
            {'column': 'result'}, name='result'),
    re_path(TASKS % 'published', views.CodeView.as_view(),
            {'column': 'published'}, name='published'),
]

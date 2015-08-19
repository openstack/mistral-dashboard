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

from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from mistraldashboard.executions.views import IndexView
from mistraldashboard.executions.views import TaskView

from mistraldashboard.executions import views

EXECUTIONS = r'^(?P<execution_id>[^/]+)/%s$'

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(EXECUTIONS % 'tasks', TaskView.as_view(), name='tasks'),
    url(EXECUTIONS % 'detail', views.DetailView.as_view(), name='detail'),
    url(EXECUTIONS % 'output', views.CodeView.as_view(),
        {'column': 'output'}, name='output'),
    url(EXECUTIONS % 'input', views.CodeView.as_view(),
        {'column': 'input'}, name='input'),
)

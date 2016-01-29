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

from django.conf.urls import url  # noqa

from mistraldashboard.executions import views

EXECUTIONS = r'^(?P<execution_id>[^/]+)/%s$'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(EXECUTIONS % 'detail', views.DetailView.as_view(), name='detail'),
    url(EXECUTIONS % 'detail_task_id', views.DetailView.as_view(),
        {'caller': 'task'}, name='detail_task_id'),
    url(EXECUTIONS % 'output', views.CodeView.as_view(),
        {'column': 'output'}, name='output'),
    url(EXECUTIONS % 'input', views.CodeView.as_view(),
        {'column': 'input'}, name='input'),
    url(EXECUTIONS % 'update_description',
        views.UpdateDescriptionView.as_view(),
        name='update_description'),
]

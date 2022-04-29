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

from mistraldashboard.workflows import views

WORKFLOWS = r'^(?P<workflow_name>[^/]+)/%s$'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^select_definition$',
            views.SelectDefinitionView.as_view(),
            name='select_definition'),
    re_path(r'^change_definition$',
            views.ChangeDefinitionView.as_view(),
            name='change_definition'),
    re_path(r'^create$', views.CreateView.as_view(), name='create'),
    re_path(r'^update$', views.UpdateView.as_view(), name='update'),
    re_path(WORKFLOWS % 'execute', views.ExecuteView.as_view(),
            name='execute'),
    re_path(WORKFLOWS % 'detail', views.DetailView.as_view(), name='detail'),
    re_path(WORKFLOWS % 'definition', views.CodeView.as_view(),
            {'column': 'definition'}, name='definition'),
    re_path(WORKFLOWS % 'input', views.CodeView.as_view(),
            {'column': 'input'}, name='input'),
]

# Copyright 2015 Huawei Technologies Co., Ltd.
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

from mistraldashboard.actions import views

ACTIONS = r'^(?P<action_name>[^/]+)/%s$'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(ACTIONS % 'detail', views.DetailView.as_view(), name='detail'),
    url(ACTIONS % 'run', views.RunView.as_view(), name='run'),
    url(r'^create$', views.CreateView.as_view(), name='create'),
    url(r'^update$', views.UpdateView.as_view(), name='update'),
]

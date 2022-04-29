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

from mistraldashboard.cron_triggers import views

CRON_TRIGGERS = r'^(?P<cron_trigger_name>[^/]+)/%s$'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(CRON_TRIGGERS % 'detail', views.OverviewView.as_view(),
            name='detail'),
    re_path(r'^create$', views.CreateView.as_view(), name='create'),
]

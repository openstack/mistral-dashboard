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

from django.conf import settings

from mistralclient.api import client as mistral_client

SERVICE_TYPE = 'workflow'


def mistralclient(request):
    return mistral_client.Client(
        username=request.user.username,
        auth_token=request.user.token.id,
        project_id=request.user.tenant_id,
        # Ideally, we should get it from identity endpoint, but since
        # python-mistralclient is not supporting v2.0 API it might create
        # additional troubles for those who still rely on v2.0 stack-wise.
        auth_url=getattr(settings, 'OPENSTACK_KEYSTONE_URL'),
        # Todo: add SECONDARY_ENDPOINT_TYPE support
        endpoint_type=getattr(settings,
                              'OPENSTACK_ENDPOINT_TYPE',
                              'internalURL'),
        service_type=SERVICE_TYPE)

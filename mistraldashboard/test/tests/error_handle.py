# Copyright 2015 ASD Technologies Co.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from mistraldashboard.handle_errors import handle_errors
from mistraldashboard.test import helpers as test


class ErrorHandleTests(test.TestCase):

    class CommonException(Exception):
        pass

    def test_args_request_view_error_handle(self):

        @handle_errors('Error message')
        def common_view(request):
            raise self.CommonException()

        self.assertRaises(self.CommonException, common_view, {})

    def test_kwargs_request_view_error_handle(self):

        @handle_errors('Error message')
        def common_view(slf, request, context=None):
            raise self.CommonException()

        with self.assertRaises(self.CommonException):
            common_view(slf=None, request={})

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

from django.template.loader import render_to_string
import iso8601
import json

TYPES = {
    'SUCCESS': 'label-success',
    'ERROR': 'label-danger',
    'DELAYED': 'label-default',
    'PAUSED': 'label-primary',
    'RUNNING': 'label-info',
}


def label(x):
    return render_to_string("mistral/default/_label.html",
                            {"label": x,
                             "type": TYPES.get(x)})


def humantime(x):
    return render_to_string("mistral/default/_humantime.html",
                            {"datetime": iso8601.parse_date(x)})


def prettyprint(x):
    short = None
    full = json.dumps(json.loads(x), indent=4, ensure_ascii=False)

    lines = full.split('\n')

    if (len(lines) > 5):
        short = '\n'.join(lines[:5] + ['...'])

    return render_to_string("mistral/default/_prettyprint.html",
                            {"full": full, "short": short})


def convert_empty_string_to_none(str):
    """Returns None if given string is empty.

    Empty string is default for Django form empty HTML input.
    python-mistral-client does not handle empty strings, only "None" type.

    :param str: string variable
    """

    return str if len(str) != 0 else None

# -*- coding: utf-8 -*-
#
# Copyright © 2015 - Alcatel-Lucent
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

"""File Overrides OpenStack Horizon Cell method to return the whole
 row data using cell_attributes_getter"""

from django import forms
from django import template

from horizon.tables import base

import six


def get_data(self, datum, column, row):
    """Fetches the data to be displayed in this cell."""
    table = row.table
    if column.auto == "multi_select":
        data = ""
        if row.can_be_selected(datum):
            widget = forms.CheckboxInput(check_test=lambda value: False)
            # Convert value to string to avoid accidental type conversion
            data = widget.render('object_ids',
                                 six.text_type(table.get_object_id(datum)),
                                 {'class': 'table-row-multi-select'})
        table._data_cache[column][table.get_object_id(datum)] = data
    elif column.auto == "form_field":
        widget = column.form_field
        if issubclass(widget.__class__, forms.Field):
            widget = widget.widget

        widget_name = "%s__%s" % \
                      (column.name,
                       six.text_type(table.get_object_id(datum)))

        # Create local copy of attributes, so it don't change column
        # class form_field_attributes
        form_field_attributes = {}
        form_field_attributes.update(column.form_field_attributes)
        # Adding id of the input so it pairs with label correctly
        form_field_attributes['id'] = widget_name

        if (template.defaultfilters.urlize in column.filters or
           template.defaultfilters.yesno in column.filters):
                data = widget.render(widget_name,
                                     column.get_raw_data(datum),
                                     form_field_attributes)
        else:
            data = widget.render(widget_name,
                                 column.get_data(datum),
                                 form_field_attributes)
        table._data_cache[column][table.get_object_id(datum)] = data
    elif column.auto == "actions":
        data = table.render_row_actions(datum)
        table._data_cache[column][table.get_object_id(datum)] = data
    else:
        data = column.get_data(datum)
        if column.cell_attributes_getter:
            # Following line is the change: cell_attributes_getter called with
            #  "datum" instead of "data"
            cell_attributes = column.cell_attributes_getter(datum) or {}
            self.attrs.update(cell_attributes)

    return data


def init():
    base.Cell.get_data = get_data

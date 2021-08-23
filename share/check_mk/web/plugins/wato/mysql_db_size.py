#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2014             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Filesize,
    Optional,
    TextAscii,
    Tuple,
    Integer,
    Percentage,
    Checkbox,
    Dictionary
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)


def _item_spec_mysql_db_size():
    return TextAscii(
        title=_("Name of the database"),
        help=_("Don't forget the instance: instance:dbname"),
    )


def _parameter_valuespec_mysql_db_size():
    return Dictionary(elements=[
        ("mysql_size",
         Optional(Tuple(elements=[
                    Filesize(title=_("warning at")),
                    Filesize(title=_("critical at")),
                ],),
                help=_("The check will trigger a warning or critical state if the size of the "
                       "database exceeds these levels."),
                title=_("Impose limits on the size of the database"))),
        ("trend_range",
         Optional(Integer(title=_("Time Range for trend computation"),
                          default_value=24,
                          minvalue=1,
                          unit=_("hours")),
                  title=_("Trend computation"),
                  label=_("Enable trend computation"))),
        ("trend_mb",
         Tuple(title=_("Levels on trends in MB per time range"),
               elements=[
                   Integer(title=_("Warning at"), unit=_("MB / range"), default_value=100),
                   Integer(title=_("Critical at"), unit=_("MB / range"), default_value=200)
               ])),
        ("trend_perc",
         Tuple(title=_("Levels for the percentual growth per time range"),
               elements=[
                   Percentage(
                       title=_("Warning at"),
                       unit=_("% / range"),
                       default_value=5,
                   ),
                   Percentage(
                       title=_("Critical at"),
                       unit=_("% / range"),
                       default_value=10,
                   ),
               ])),
        ("trend_perfdata",
         Checkbox(title=_("Trend performance data"),
                  label=_("Enable generation of performance data from trends"))),
    ])


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="mysql_db_size",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_mysql_db_size,
        parameter_valuespec=_parameter_valuespec_mysql_db_size,
        title=lambda: _("Size of MySQL databases"),
    ))


#  Copyright 2022 Joshua Brown
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# System constants
ON = 1
OFF = 0

FUNC_DC_CURRENT = 1
FUNC_DC_VOLTAGE = 0
FUNC_RESISTANCE = 2

TERMINALS_FRONT = 0
TERMINALS_REAR = 1

# Source-specific constants


# Measure-specific constants
FILTER_MOVING_AVG = 0
FILTER_REPEAT_AVG = 1

AUDIBLE_NONE = 0
AUDIBLE_FAIL = 1
AUDIBLE_PASS = 2

SENSE_2WIRE = 0
SENSE_4WIRE = 1

UNIT_AMP = 0
UNIT_OHM = 1
UNIT_VOLT = 2
UNIT_WATT = 3

# Limit test constants
FAIL_NONE = 0
FAIL_HIGH = 1
FAIL_LOW = 2
FAIL_BOTH = 3

# Math constants
MATH_MXB = 0
MATH_PERCENT = 1
MATH_RECIPROCAL = 2

# display constants
DISPLAY_SCREEN_HOME = 0
DISPLAY_SCREEN_HOME_LARGE_READING = 1
DISPLAY_SCREEN_READING_TABLE = 2
DISPLAY_SCREEN_GRAPH = 3
DISPLAY_SCREEN_HISTOGRAM = 4
DISPLAY_SCREEN_GRAPH_SWIPE = 5
DISPLAY_SCREEN_SETTINGS_SWIPE = 6
DISPLAY_SCREEN_SOURCE_SWIPE = 7
DISPLAY_SCREEN_STATS_SWIPE = 8
DISPLAY_SCREEN_USER_SWIPE = 9
DISPLAY_SCREEN_PROCESSING = 10

# Trigger model constants
TRIGGER_STATE_ABORTED = 0
TRIGGER_STATE_ABORTING = 1
TRIGGER_STATE_BUILDING = 2
TRIGGER_STATE_EMPTY = 3
TRIGGER_STATE_FAILED = 4
TRIGGER_STATE_IDLE = 5
TRIGGER_STATE_RUNNING = 6

# Event log constants
EVENTLOG_SEV_ERROR = 1
EVENTLOG_SEV_WARN = 2
EVENTLOG_SEV_WARN_OR_ERROR = 3
EVENTLOG_SEV_INFO =4
EVENTLOG_SEV_INFO_OR_ERROR = 5
EVENTLOG_SEV_INFO_OR_WARN = 6
EVENTLOG_SEV_ALL = 7

# Off mode constants
OFFMODE_NORMAL = 0
OFFMODE_ZERO = 1
OFFMODE_HIGHZ = 2
OFFMODE_GUARD = 3

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

import KeithleySeries2400InteractiveSmu_Constants as _smuconst


class EventLogConfiguration:
    """
    Placeholder docstring description
    """
    def __init__(self):
        self._mycomms = None
        # self.input = self.Input()

    def update_comms(self):
        """
        This function is used to ensure lower level consumer classes tied to\
            the driver are updated to promote instrument communications.

        :return:
        """
        # self.input._mycomms = self._mycomms

    def clear(self):
        """
        This function clears the event log.

        :return:
        """
        self._mycomms.write("eventlog.clear()")

    def getcount(self, event_type=None):
        """
        Temporary provisional docstring
        """
        event_count = 0
        if event_type is None:
            event_count = int(self._mycomms.query("print(eventlog.getcount())\
                ").rstrip())
        else:
            const_string = ""
            if event_type is _smuconst.EVENTLOG_SEV_ERROR:
                const_string = "eventlog.SEV_ERROR"
            elif event_type is _smuconst.EVENTLOG_SEV_WARN:
                const_string = "eventlog.SEV_WARN"
            elif event_type is _smuconst.EVENTLOG_SEV_WARN_OR_ERROR:
                const_string = "eventlog.SEV_WARN|eventlog.SEV_ERROR"
            elif event_type is _smuconst.EVENTLOG_SEV_INFO:
                const_string = "eventlog.SEV_INFO"
            elif event_type is _smuconst.EVENTLOG_SEV_INFO_OR_ERROR:
                const_string = "eventlog.SEV_INFO|eventlog.SEV_ERROR"
            elif event_type is _smuconst.EVENTLOG_SEV_INFO_OR_WARN:
                const_string = "eventlog.SEV_INFO|eventlog.SEV_WARN"
            elif event_type is _smuconst.EVENTLOG_SEV_ALL:
                const_string = "eventlog.SEV_ALL"
            event_count = int(self._mycomms.query(f"print(eventlog.getcount\
                ({const_string}))").rstrip())
        return event_count

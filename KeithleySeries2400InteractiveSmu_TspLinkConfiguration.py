
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

from pyparsing import line
import KeithleySeries2400InteractiveSmu_Constants as _smuconst


class TspLinkConfiguration:
    """
    Placeholder docstring description
    """
    def __init__(self):
        self._mycomms = None
        self.line = self.Line()

    def update_comms(self):
        """
        This function is used to ensure lower level consumer classes tied to\
            the driver are updated to promote instrument communications.

        :return:
        """
        self.line._mycomms = self._mycomms

    @property
    def group(self):
        """
        This attribute contains the group number of a TSP-Link node.

        :param: None
        :return group_number: The group number of the TSP-Link node (0 to 64)
        """
        self._mycomms.write("group_number = tsplink.group")
        group_number = self._mycomms.query("print(group_number)")
        return group_number

    @group.setter
    def group(self, group_number):
        """
        This attribute contains the group number of a TSP-Link node.

        :param: group_number The group number of the TSP-Link node (0 to 64)
        :return group_number: None
        """
        self._mycomms.write(f"tsplink.group = {group_number}")

    def initialize(self, expected_nodes):
        """
        This function initializes all instruments and enclosures in the\
            TSP-Link system.

        :param expected_nodes: The number of nodes expected on the system (1\
            to 32)
        :return nodes_found: The number of nodes found on the system,\
            including the node on which the command is running.
        """
        if expected_nodes is None:
            self._mycomms.write(f"tsplink.initialize({expected_nodes})")
            return None
        else:
            self._mycomms.write("nodes_found = tsplink.initialize()")
            nodes_found = self._mycomms.query("print(nodes_found)")
            return nodes_found

    class Line():
        """
        Placeholder docstring
        """
        def __init__(self):
            self._mycomms = None

        def mode(self, n, line_mode=None):
            """
            This attribute contains the group number of a TSP-Link node.

            :param n: (int) The trigger line (1 to 3).
            :param line_mode: The trigger mode. The line mode can be set,\
                for digital open drain line use\
                TSPLINK_MODE_DIGITAL_OPEN_DRAIN, for trigger open drain\
                line use TSPLINK_MODE_TRIGGER_OPEN_DRAIN, for trigger\
                synchronous master use TSPLINK_MODE_SYNCHRONOUS_MASTER,\
                for trigger synchronous acceptor use\
                TSPLINK_MODE_SYNCHRONOUS_ACCEPTOR.
            :return: None | line_mode
            """
            if line_mode is None:
                self._mycomms.write(f"tsplink.line[{n}].mode = {line_mode}")
                return None
            else:
                self._mycomms.write("mode = tsplink.line[N].mode")
                line_mode = self._mycomms.query("print(mode)")
                return line_mode

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


class DigitalIoConfiguration:
    """
    Placeholder docstring description.
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

    class Line:
        """
        This subclass supports setting/getting autozero-based attributes.
        """
        def __init__(self):
            self._mycomms = None

        def mode(self, io_line, line_mode=None):
            """
            This attribute sets the mode of the digital I/O line to be a
            digital line, trigger line, or synchronous line and sets the line
            to be input, output, or open-drain.

            :param io_line: (int) The digital I/O line: 1 to 6
            :param mode: The digital line control type and line mode -
                DIGIO_MODE_DIGITAL_IN,  DIGIO_MODE_DIGITAL_OUT,
                DIGIO_MODE_DIGITAL_OPEN_DRAIN,  DIGIO_MODE_TRIGGER_IN,
                DIGIO_MODE_TRIGGER_OUT, DIGIO_MODE_TRIGGER_OPEN_DRAIN,
                DIGIO_MODE_SYNCHRONOUS_MASTER,  DIGIO_MODE_SYNCHRONOUS_ACCEPTOR
            :return: line_mode
            """
            if line_mode is not None:
                if line_mode is _smuconst.DIGIO_MODE_DIGITAL_IN:
                    self._mycomms.write(f"digio.line[{io_line}].mode =\
                        digio.MODE_DIGITAL_IN")
                elif line_mode is _smuconst.DIGIO_MODE_DIGITAL_OUT:
                    self._mycomms.write(f"digio.line[{io_line}].mode =\
                        digio.MODE_DIGITAL_OUT")
                elif line_mode is _smuconst.DIGIO_MODE_DIGITAL_OPEN_DRAIN:
                    self._mycomms.write(f"digio.line[{io_line}].mode =\
                        digio.MODE_DIGITAL_OPEN_DRAIN")
                elif line_mode is _smuconst.DIGIO_MODE_TRIGGER_IN:
                    self._mycomms.write(f"digio.line[{io_line}].mode =\
                        digio.MODE_TRIGGER_IN")
                elif line_mode is _smuconst.DIGIO_MODE_TRIGGER_OUT:
                    self._mycomms.write(f"digio.line[{io_line}].mode =\
                        digio.MODE_TRIGGER_OUT")
                elif line_mode is _smuconst.DIGIO_MODE_TRIGGER_OPEN_DRAIN:
                    self._mycomms.write(f"digio.line[{io_line}].mode =\
                        digio.MODE_TRIGGER_OPEN_DRAIN")
                elif line_mode is _smuconst.DIGIO_MODE_SYNCHRONOUS_MASTER:
                    self._mycomms.write(f"digio.line[{io_line}].mode =\
                        digio.MODE_SYNCHRONOUS_MASTER")
                elif line_mode is _smuconst.DIGIO_MODE_SYNCHRONOUS_ACCEPTOR:
                    self._mycomms.write(f"digio.line[{io_line}].mode =\
                        digio.MODE_SYNCHRONOUS_ACCEPTOR")
                return None
            else:
                line_mode = self._mycomms.query(f"line_mode =\
                    digio.line[{io_line}].mode")
                return_val = None
                if "DIGITAL_IN" in line_mode:
                    return_val = _smuconst.DIGIO_MODE_DIGITAL_IN
                elif "DIGITAL_OUT" in line_mode:
                    return_val = _smuconst.DIGIO_MODE_DIGITAL_OUT
                elif "DIGITAL_OPEN_DRAIN" in line_mode:
                    return_val = _smuconst.DIGIO_MODE_DIGITAL_OPEN_DRAIN
                elif "TRIGGER_IN" in line_mode:
                    return_val = _smuconst.DIGIO_MODE_TRIGGER_IN
                elif "TRIGGER_OUT" in line_mode:
                    return_val = _smuconst.DIGIO_MODE_TRIGGER_OUT
                elif "TRIGGER_OPEN_DRAIN" in line_mode:
                    return_val = _smuconst.DIGIO_MODE_TRIGGER_OPEN_DRAIN
                elif "MASTER" in line_mode:
                    return_val = _smuconst.DIGIO_MODE_SYNCHRONOUS_MASTER
                elif "ACCEPTOR" in line_mode:
                    return_val = _smuconst.DIGIO_MODE_SYNCHRONOUS_ACCEPTOR
                return return_val

        def reset(self, io_line):
            """
            This function resets digital I/O line values to their factory
            defaults.

            :param io_line: (int) The digital I/O line: 1 to 6
            :return
            """
            self._mycomms.write(f"digio.line[{io_line}].reset()")

        def state(self, io_line, state=None):
            """
            This function resets digital I/O line values to their factory
            defaults.

            :param io_line: (int) The digital I/O line: 1 to 6
            :param state: Either DIGIO_STATE_LOW (0) or DIGIO_STATE_HIGH (1).\
                If no argument is passed, the default state remains None and\
                    the method acts to return the active state.
            :return
            """
            if state is None:
                self._mycomms.write(f"state = digio.line[{io_line}].state")
                state_str = self._mycomms.query("print(state)")
                if "STATE_LOW" in state_str:
                    return _smuconst.DIGIO_STATE_LOW
                elif "STATE_HIGH" in state_str:
                    return _smuconst.DIGIO_STATE_HIGH
            else:
                if state is _smuconst.DIGIO_STATE_LOW:
                    self._mycomms.write(f"digio.line[{io_line}].state =\
                        digio.STATE_LOW")
                if state is _smuconst.DIGIO_STATE_HIGH:
                    self._mycomms.write(f"digio.line[{io_line}].state =\
                        digio.STATE_HIGH")
                return None

    def readport(self):
        """
        This function reads the digital I/O port.

        :return: (int) value
        """
        self._mycomms.write("data = digio.readport()")
        value = int(self._mycomms.query("print(data)"))
        return value

    def writeport(self, data):
        """
        This function writes to all digital I/O lines.

        :param data: (int) The value to write to the port (0 to 63)
        :return: (int) value
        """
        self._mycomms.write(f"digio.writeport({data})")


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


class Buffer:
    """
    Placeholder docstring description
    """
    def __init__(self):
        self.mycomms = None

    def update_comms(self):
        """
        This function is used to ensure lower level consumer classes tied to\
            the driver are updated to promote instrument communications.

        :return:
        """
        # self.input._mycomms = self._mycomms
        print(0)

    def capacity(self, buffername="defbuffer1", buffer_capacity=None):
        """
        This attribute gets or sets the number of readings a buffer can store.\
            When the

        :param buffername: (str) The name of the reading buffer, which may be\
            a default buffer (defbuffer1 or defbuffer2) or a user-defined\
            buffer
        :param buffer_capacity: (int) The maximum number of readings the\
            buffer can store; set to 0 to maximize the buffer size
        :return:
        """
        if buffer_capacity is None:
            self.mycomms.write(f"cap = {buffername}.capacity")
            cap = int(self.mycomms.query("print(cap)").rstrip())
            return cap
        else:
            self.mycomms.write(f"{buffername}.capacity={buffer_capacity}")

    # @capacity.setter
    # def set_capacity(self, buffername, size):
    #    """This attribute sets the number of readings a buffer can store."""
    #    self.mycomms.write(f"{buffername}.capacity={size}")

    def clear(self, buffername):
        """
        This function clears all readings and statistics from the specified\
            buffer.
        """
        self.mycomms.write(f"{buffername}.clear()")

    def clearstats(self, buffername):
        """
        This function clears the statistical information associated with\
            the specified buffer.
        """
        if buffername is None:
            self.mycomms.write("buffer.clearstats()")
        else:
            self.mycomms.write(f"buffer.clearstats({buffername})")

    def dates(self, buffername, index):
        """
        This attribute contains the dates of readings that are stored in\
        the reading buffer.
        """
        return self.mycomms.query(f"print({buffername}.dates[{index}])").\
            rstrip()

    def delete(self, buffername):
        """This function deletes a user-defined reading buffer."""
        self.mycomms.write(f"buffer.delete({buffername})")

    @property
    def endindex(self, buffername):
        """This attribute indicates the last index in a reading buffer."""
        # IS THE SYNTAX FOR THIS BASS-ACKWARD IN THE REF MAN????
        return self.mycomms.query(f"print({buffername}.endindex)")

    @property
    def extraformattedvalues(self, buffername, index):
        """
        This attribute contains the measurement and the unit of measure of the\
            additional values in a reading buffer."""
        return self.mycomms.query(f"print({buffername}.extraformattedvalues[\
            {index}])")

    @property
    def extravalues(self, buffername, index):
        """
        This attribute contains the additional values in a reading buffer.
        """
        return self.mycomms.query(f"print({buffername}.extravalues[{index}])")

    @property
    def extravalueunits(self, buffername, index):
        """
        This attribute contains the units of the additional values in a\
            reading buffer.
        """
        return self.mycomms.query(f"print({buffername}.extravalueunits[\
            {index}])")

    @property
    def fillmode(self):
        """
        This attribute determines if a reading buffer is filled continuously\
            or is filled once and stops.
        """
        return ""

    @fillmode.setter
    def fillmode(self, buffername, mode):
        """
        This attribute determines if a reading buffer is filled continuously\
             or is filled once and stops.
        """
        self.mycomms.write(f"{buffername}.fillmode = {mode}")

    def getstats(self, *args):
        """
        This function returns statistics from a specified reading buffer.
        """
        return

    def make(self, buffername, buffersize, style=None):
        """
        This function creates a user-defined reading buffer.
        """
        stylestr = ""
        if style is not None:
            if style == 0:
                stylestr = ""
            elif style == 1:
                stylestr = ""

            self.mycomms.write(f"{buffername} = buffer.make({buffersize},\
                {stylestr})")
        else:
            self.mycomms.write(f"{buffername} = buffer.make({buffersize})")

    def math(self, buffername, unit, expression, *constants):
        """
        This function allows you to run a mathematical expression on a\
            measurement. The expression is applied when the measurement is\
                placed in the reading buffer.
        """
        commandstring = f"buffer.math({buffername},{unit},{expression}"

        # iterate over constants to be added if available
        if len(constants) != 0:
            for cs in constants:
                commandstring += f",{cs}"
        commandstring += ")"

        self.mycomms.write(commandstring)

    def save(self, buffername, filename, **kwargs):
        """
        This function saves data from the specified reading buffer to a USB\
            flash drive.

        :param buffername: (string) The name of the reading buffer, which may
        be a default buffer (defbuffer1 or defbuffer2) or a user-defined buffer
        :param filename: (string) A string that indicates the name of the file
        on the USB flash drive in which to save the reading buffer
        :param timeformat: (constant) Defines how date and time information
        from the buffer is saved in the file on the USB flash drive; the
        options are:
           * BUFFER_SAVE_FORMAT_TIME to save dates, times, and fractional
             seconds
           * BUFFER_SAVE_RELATIVE_TIME to save relative timestamps
           * BUFFER_SAVE_RAW_TIME to save seconds and fractional seconds
           * BUFFER_SAVE_TIMESTAMP_TIME save timestamps
        :param start: (int) Defines the starting point in the buffer to
        start saving data
        :param end: (int) Defines the ending point in the buffer to stop
        saving data
        :return:
        """
        cmd_str = f"buffer.save({buffername},\"{filename}\""
        for k, v in kwargs.items():
            if k == 'timeformat':
                if v == _smuconst.BUFFER_SAVE_FORMAT_TIME:
                    cmd_str += ",buffer.SAVE_FORMAT_TIME"
                elif v == _smuconst.BUFFER_SAVE_RAW_TIME:
                    cmd_str += ",buffer.SAVE_RAW_TIME"
                elif v == _smuconst.BUFFER_SAVE_RELATIVE_TIME:
                    cmd_str += ",buffer.SAVE_RELATIVE_TIME"
                elif v == _smuconst.BUFFER_SAVE_TIMESTAMP_TIME:
                    cmd_str += ",buffer.SAVE_TIMESTAMP_TIME"
            if k == 'start':
                cmd_str += f",{v}"
            if k == 'end':
                cmd_str += f",{v}"

        cmd_str += ")"
        self.mycomms.write(cmd_str)

    def saveappend(self, buffername, filename, **kwargs):
        """
        This function saves data from the specified reading buffer to a USB
        flash drive.

        :param buffername: (string) The name of the reading buffer, which may
        be a default buffer (defbuffer1 or defbuffer2) or a user-defined buffer
        :param filename: (string) A string that indicates the name of the file
        on the USB flash drive in which to save the reading buffer
        :param timeformat: (constant) Defines how date and time information
        from the buffer is saved in the file on the USB flash drive; the
        options are:
           * BUFFER_SAVE_FORMAT_TIME to save dates, times, and fractional
             seconds
           * BUFFER_SAVE_RELATIVE_TIME to save relative timestamps
           * BUFFER_SAVE_RAW_TIME to save seconds and fractional seconds
           * BUFFER_SAVE_TIMESTAMP_TIME save timestamps
        :param start: (int) Defines the starting point in the buffer to
        start saving data
        :param end: (int) Defines the ending point in the buffer to stop
        saving data
        :return:
        """
        cmd_str = f"buffer.saveappend({buffername},\"{filename}\""
        for k, v in kwargs.items():
            if k == 'timeformat':
                if v == _smuconst.BUFFER_SAVE_FORMAT_TIME:
                    cmd_str += ",buffer.SAVE_FORMAT_TIME"
                elif v == _smuconst.BUFFER_SAVE_RAW_TIME:
                    cmd_str += ",buffer.SAVE_RAW_TIME"
                elif v == _smuconst.BUFFER_SAVE_RELATIVE_TIME:
                    cmd_str += ",buffer.SAVE_RELATIVE_TIME"
                elif v == _smuconst.BUFFER_SAVE_TIMESTAMP_TIME:
                    cmd_str += ",buffer.SAVE_TIMESTAMP_TIME"
            if k == 'start':
                cmd_str += f",{v}"
            if k == 'end':
                cmd_str += f",{v}"

        cmd_str += ")"
        self.mycomms.write(cmd_str)

    def unit(self):
        """
        This function allows you to create up to three custom units of measure
        for use in buffers.

        param: first - (None)
        param: second = (None)
        """
        print(0)

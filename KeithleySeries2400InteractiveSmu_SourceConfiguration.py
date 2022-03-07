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


class SourceConfiguration:
    """
    Placeholder docstring description
    """
    def __init__(self):
        self._mycomms = None
        self.configlist = self.ConfigList()
        self.protect = self.Protect()
        self.ilimit = self.ILimit()
        self.vlimit = self.VLimit()

    def update_comms(self):
        """This function is used to ensure lower level consumer classes tied to the driver are updated to promote \
         instrument communications.
         """
        self.configlist._mycomms = self._mycomms
        self.protect._mycomms = self._mycomms
        self.ilimit._mycomms = self._mycomms
        self.vlimit._mycomms = self._mycomms

    class ConfigList:
        """
        Placeholder docstring description
        """
        def __init__(self):
            self._mycomms = None

        def catalog(self):
            """
            This function returns the name of one source configuration list that is stored on the instrument.

            :return: The name of a configuration list.
            """
            self._mycomms.query("print(smu.source.configlist.catalog())")

        def create(self, list_name):
            """
            This function creates an empty source configuration list.

            :param list_name:
            :return:
            """
            self._mycomms.write(f"smu.source.configlist.create({list_name}))")

        def delete(self, list_name, index=None):
            """
            This function deletes a source configuration list.

            :param list_name:
            :param index:
            :return:
            """
            if index == None:
                self._mycomms.write(f"smu.source.configlist.delete(\"{list_name}\"))")
            else:
                self._mycomms.write(f"smu.source.configlist.delete(\"{list_name}\", {index}))")

        def query(self, list_name, index, field_separator=None):
            """
            This function returns a list of TSP commands and parameter settings that are stored in the specified \
            configuration index

            :param list_name: A string that represents the name of a source configuration list
            :param index: A number that defines a specific configuration index in the configuration list
            :param field_separator: String that represents the separator for the data; use one of the following,
                            * Comma (default): ,
                            * Semicolon: ;
                            * New line: \n

            :return:
            """
            if field_separator is None:
                self._mycomms.query(f"print(smu.source.configlist.query(\"{list_name}\", {index}))")
            else:
                self._mycomms.query(f"print(smu.source.configlist.query(\"{list_name}\", {index}, {field_separator}))")

        def recall(self, list_name, index=None, source_list_name=None, source_index=None):
            """
            This function recalls a configuration index in a source configuration list and an optional source \
            configuration list.

            :param list_name:
            :param index:
            :param source_list_name:
            :param source_index:
            :return:
            """
            if source_index is None:
                if index is None:
                    self._mycomms.write(f"smu.source.configlist.recall(\"{list_name}\")")
                else:
                    self._mycomms.write(f"smu.source.configlist.recall(\"{list_name}\", {index})")
            else:
                if source_index is None:
                    self._mycomms.write(
                        f"smu.source.configlist.recall(\"{list_name}\", {index}),\"{source_list_name}\")")
                else:
                    self._mycomms.write(
                        f"smu.source.configlist.recall(\"{list_name}\", {index}),\"{source_list_name}\","
                        f" {source_index})")

        def size(self, list_name):
            """
            This function returns the size (number of configuration indexes) of a source configuration list.

            :param list_name:
            :return:
            """
            self._mycomms.write(f"index_count = smu.source.configlist.zier(\"{list_name}\")")
            return int(self._mycomms.query("print(index_count)"))

        def store(self, list_name, index=None):
            """
            This function stores the active source settings into the named configuration list.

            :param list_name:
            :param index:
            :return:
            """
            if index is None:
                self._mycomms.write(f"smu.source.configlist.store(\"{list_name}\")")
            else:
                self._mycomms.write(f"smu.source.configlist.store(\"{list_name}\", {index})")

        def storefunc(self, list_name, function, index=None):
            """
            This function allows you to store the settings for a source function into a source configuration \
            list whether or not the function is active.

            :param list_name:
            :param function:
            :param index:
            :return:
            """
            function_str = None
            if function == _smuconst.FUNC_DC_VOLTAGE:
                function_str = "smu.FUNC_DC_VOLTAGE"
            elif function == _smuconst.FUNC_DC_CURRENT:
                function_str = "smu.FUNC_DC_VOLTAGE"
            elif function == _smuconst.FUNC_RESISTANCE:
                function_str = "smu.FUNC_DC_RESISTANCE"

            if index is None:
                self._mycomms.write(f"smu.source.configlist.storefunc(\"{list_name}\", {function_str})")
            else:
                self._mycomms.write(f"smu.source.configlist.storefunc(\"{list_name}\", {function_str}, {index})")

    @property
    def delay(self):
        """
        This attribute contains the source delay.

        :return: The length of the delay
        """
        self._mycomms.write("delay_value = smu.source.delay")
        delay_value = float(self._mycomms.query("print(delay_value)").rstrip())
        return delay_value

    @delay.setter
    def delay(self, delay_value):
        """
        This attribute contains the source delay.

        :param delay_value: The length of the delay (0 to 10 ks)
        :return:
        """
        self._mycomms.write(f"smu.source.delay={delay_value}")

    class Protect:
        """
        Placeholder docstring description
        """
        def __init__(self):
            self._mycomms = None

    @property
    def func(self):
        """This attribute contains the source function, which can be voltage or current."""
        self._mycomms.write("srcfunc = smu.source.func")
        response = self._mycomms.query("print(srcfunc)").rstrip()
        # retconstval = None
        if "VOLTAGE" in response:
            retconstval = _smuconst.FUNC_DC_VOLTAGE
        else:
            retconstval = _smuconst.FUNC_DC_CURRENT
        return retconstval

    @func.setter
    def func(self, func):
        """This attribute contains the source function, which can be voltage or current."""
        if func == _smuconst.FUNC_DC_VOLTAGE:
            self._mycomms.write("smu.source.func = smu.FUNC_DC_VOLTAGE")
            # print()
        else:
            self._mycomms.write("smu.source.func = smu.FUNC_DC_CURRENT")
            # print()

    @property
    def level(self):
        """This attribute immediately selects a fixed amplitude for the selected source function."""
        self._mycomms.write("srclev = smu.source.level")
        return float(self._mycomms.query("print(srclev)").rstrip())

    @level.setter
    def level(self, value):
        """This attribute immediately selects a fixed amplitude for the selected source function."""
        self._mycomms.write(f"smu.source.level = {value}")

    class ILimit:
        """
        Placeholder docstring description
        """
        def __init__(self):
            self._mycomms = None

        @property
        def level(self):
            """This attribute selects the source limit for current measurements."""
            self._mycomms.write("ilimitlev = smu.source.ilimit.level")
            return float(self._mycomms.query("print(ilimitlev)").rstrip())

        @level.setter
        def level(self, value):
            """This attribute selects the source limit for current measurements."""
            self._mycomms.write(f"smu.source.ilimit.level = {value}")

        @property
        def tripped(self):
            """This attribute indicates if the source exceeded the limits that were set for the selected measurements."""
            self._mycomms.write("ilimittrip = smu.source.ilimit.tripped")
            return int(self._mycomms.query("print(ilimittrip)").rstrip())

    @property
    def offmode(self):
        """
        This attribute defines the state of the source when the output is turned off.

            NORMAL = 2-wire sense, voltage source with 0 V level, current limit level set to 10% full scale of present
                     range
            HIGHZ = 2-wire sense, output relay opens
            ZERO = 2-wire sense, voltage source with 0 V level, if current measure set then current limit level is not
                   changed otherwise the measurement is set to current and limit level is set to 10% full scale of
                   present range
            GUARD = 2-wire sense, current source selected and set to 0 A level, voltage limit level set to 10% full
                    scale of present range

        :return: Either OFFMODE_NORMAL, OFFMODE_HIGHZ, OFFMODE_ZERO, or OFFMODE_GUARD
        """
        self._mycomms.write("source_off_mode = smu.source.offmode")
        source_off_mode = self._mycomms.query("print(source_off_mode)").rstrip()
        if "NORMAL" in source_off_mode:
            return _smuconst.OFFMODE_NORMAL
        elif "HIGHZ" in source_off_mode:
            return _smuconst.OFFMODE_HIGHZ
        elif "ZERO" in source_off_mode:
            return _smuconst.OFFMODE_ZERO
        elif "GUARD" in source_off_mode:
            return _smuconst.OFFMODE_GUARD

    @offmode.setter
    def offmode(self, source_off_mode):
        """
        This attribute defines the state of the source when the output is turned off.

            NORMAL = 2-wire sense, voltage source with 0 V level, current limit level set to 10% full scale of present
                     range
            HIGHZ = 2-wire sense, output relay opens
            ZERO = 2-wire sense, voltage source with 0 V level, if current measure set then current limit level is not
                   changed otherwise the measurement is set to current and limit level is set to 10% full scale of
                   present range
            GUARD = 2-wire sense, current source selected and set to 0 A level, voltage limit level set to 10% full
                    scale of present range

        :param source_off_mode: Either OFFMODE_NORMAL, OFFMODE_HIGHZ, OFFMODE_ZERO, or OFFMODE_GUARD
        :return:
        """
        if source_off_mode is _smuconst.OFFMODE_NORMAL:
            self._mycomms.write("smu.source.offmode = smu.OFFMODE_NORMAL")
        elif source_off_mode is _smuconst.OFFMODE_HIGHZ:
            self._mycomms.write("smu.source.offmode = smu.OFFMODE_HIGHZ")
        elif source_off_mode is _smuconst.OFFMODE_ZERO:
            self._mycomms.write("smu.source.offmode = smu.OFFMODE_ZERO")
        elif source_off_mode is _smuconst.OFFMODE_GUARD:
            self._mycomms.write("smu.source.offmode = smu.OFFMODE_GUARD")

    @property
    def readback(self):
        """
        This attribute determines if the instrument records the measured source value or the configured source value
        when making a measurement.

        :return: Either ON (1) or OFF (0)
        """
        self._mycomms.write("readback_state = smu.source.readback")
        source_readback = self._mycomms.query("print(readback_state)")
        if "ON" in source_readback:
            return _smuconst.ON
        elif "OFF" in source_readback:
            return _smuconst.OFF
        else:
            return _smuconst.OFF  # default to the off state

    @readback.setter
    def readback(self, state):
        """
        This attribute determines if the instrument records the measured source value or the configured source value
        when making a measurement.

        :param state: Either ON (1) or OFF (0)
        :return:
        """
        if state is _smuconst.ON:
            self._mycomms.write("smu.source.readback=smu.ON")
        else:
            self._mycomms.write("smu.source.readback=smu.OFF")

    class VLimit:
        """
        Placeholder docstring description
        """
        def __init__(self):
            self._mycomms = None

        @property
        def level(self):
            """This attribute selects the source limit for voltage measurements."""
            self._mycomms.write("vlimitlev = smu.source.vlimit.level")
            return float(self._mycomms.query("print(vlimitlev)").rstrip())

        @level.setter
        def level(self, value):
            """This attribute selects the source limit for voltage measurements."""
            self._mycomms.write(f"smu.source.vlimit.level = {value}")

        @property
        def tripped(self):
            """This attribute indicates if the source exceeded the limits that were set for the selected measurements."""
            self._mycomms.write("vlimittrip = smu.source.vlimit.tripped")
            return int(self._mycomms.query("print(vlimittrip)").rstrip())

    @property
    def output(self):
        """
        This attribute enables or disables the source output.

        :return: Either ON (1) or OFF (0).
        """
        self._mycomms.write("source_output = smu.source.output")
        source_output = self._mycomms.query("print(source_output)")
        if "ON" in source_output:
            return _smuconst.ON
        elif "OFF" in source_output:
            return _smuconst.OFF
        else:
            return _smuconst.OFF     # default to the off state

    @output.setter
    def output(self, state):
        """
        This attribute enables or disables the source output.

        :param state: Either ON (1) or OFF (0)
        :return: None
        """
        if state is _smuconst.ON:
            self._mycomms.write("smu.source.output=smu.ON")
        else:
            self._mycomms.write("smu.source.output=smu.OFF")

    @property
    def range(self):
        """
        This attribute determines the positive full-scale source range.

        :return: The applied source range.
        """
        self._mycomms.write("range_value = smu.source.range")
        range_value = float(self._mycomms.query("print(range_value)").rstrip())
        return range_value

    @range.setter
    def range(self, range_value):
        """
        This attribute determines the positive full-scale source range.

        :param range_value: The applied source range.
        :return:
        """
        self._mycomms.write(f"smu.source.range={range_value}")

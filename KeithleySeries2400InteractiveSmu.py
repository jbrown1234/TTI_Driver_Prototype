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

import pyvisa as visa
import CommunicationsInterface as comms
import KeithleySeries2400InteractiveSmu_Constants as smuconst

class KeithleySeries2400InteractiveSmu():
    def __init__(self):
        self.echocommand = 0
        self.node = 1
        self.resource_mgr = None
        self.resource_id = ""
        #self.instrument_object = None
        self.instrumentcomms = comms.Communications()
        self.buffer = self.Buffer()
        self.source = self.SourceConfiguration()
        self.measure = self.MeasureConfiguration()

    class InstrumentConnection(object):
        def __init__(self):
            self.resourcerm = None

        def initialize(self):
            return

        def close(self):
            return

    def initialize(self, instrument_resource_string, *args):

        try:
            self.instrumentcomms.initialize(instrument_resource_string, *args)
            self.buffer.mycomms = self.instrumentcomms
            self.source.mycomms = self.instrumentcomms
            self.measure.mycomms = self.instrumentcomms
            self.source.update_comms()
            self.measure.update_comms()
        except:
            print("error")
        return

    def reset(self):
        self.instrumentcomms.write("reset()")

    def instrument_id_query(self):
        return self.instrumentcomms.query("*IDN?")

    def close(self):
        self.instrumentcomms.close()
        return

    def available(self, functionality):
        """
        This function checks for the presence of specific instrument functionality.

        :param functionality:
        :return:
        """
        self.instrumentcomms.write(f"presence = available({functionality})")

    def beep(self, frequency, duration):
        """
        This function generates an audible tone.

        :param frequency:
        :param duration:
        :return:
        """
        self.instrumentcomms.write(f"beeper.beep({frequency},{duration})")

    class Buffer:
        def __init__(self):
            self.mycomms = None

        #@property
        def capacity(self, buffername="defbuffer1", buffer_capacity=None):
            """
            This attribute gets or sets the number of readings a buffer can store. When the

            :param buffername: (str) The name of the reading buffer, which may be a default buffer (defbuffer1 or \
                defbuffer2) or a user-defined buffer
            :param buffer_capacity: (int) The maximum number of readings the buffer can store; set to 0 to maximize \
                the buffer size
            :return:
            """
            if buffer_capacity is None:
                self.mycomms.write(f"cap = {buffername}.capacity")
                cap = int(self.mycomms.query("print(cap)").rstrip())
                return cap
            else:
                self.mycomms.write(f"{buffername}.capacity={buffer_capacity}")

        #@capacity.setter
        #def set_capacity(self, buffername, size):
        #    """This attribute sets the number of readings a buffer can store."""
        #    self.mycomms.write(f"{buffername}.capacity={size}")

        def clear(self, buffername):
            """This function clears all readings and statistics from the specified buffer."""
            self.mycomms.write(f"{buffername}.clear()")

        def clearstats(self, buffername):
            """This function clears the statistical information associated with the specified buffer."""
            if buffername is None:
                self.mycomms.write("buffer.clearstats()")
            else:
                self.mycomms.write(f"buffer.clearstats({buffername})")

        def dates(self, buffername, index):
            """This attribute contains the dates of readings that are stored in the reading buffer."""
            return self.mycomms.query(f"print({buffername}.dates[{index}])").rstrip()

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
            """This attribute contains the measurement and the unit of measure of the additional values in a reading buffer."""
            return self.mycomms.query(f"print({buffername}.extraformattedvalues[{index}])")

        @property
        def extravalues(self, buffername, index):
            """This attribute contains the additional values in a reading buffer."""
            return self.mycomms.query(f"print({buffername}.extravalues[{index}])")

        @property
        def extravalueunits(self, buffername, index):
            """This attribute contains the units of the additional values in a reading buffer."""
            return self.mycomms.query(f"print({buffername}.extravalueunits[{index}])")

        @property
        def fillmode(self):
            """This attribute determines if a reading buffer is filled continuously or is filled once and stops."""
            return ""

        @fillmode.setter
        def fillmode(self, buffername, mode):
            """This attribute determines if a reading buffer is filled continuously or is filled once and stops."""
            self.mycomms.write(f"{buffername}.fillmode = {mode}")

        def getstats(self, *args):
            """This function returns statistics from a specified reading buffer."""
            return

        def make(self, buffername, buffersize, style=None):
            """This function creates a user-defined reading buffer."""
            stylestr = ""
            if style != None:
                if style == 0:
                    stylestr = ""
                elif style == 1:
                    stylestr = ""

                self.mycomms.write(f"{buffername} = buffer.make({buffersize}, {stylestr})")
            else:
                self.mycomms.write(f"{buffername} = buffer.make({buffersize})")

        def math(self, buffername, unit, expression, *constants):
            """This function allows you to run a mathematical expression on a measurement. The expression is applied when the measurement is placed in the reading buffer."""
            commandstring = f"buffer.math({buffername},{unit},{expression}"

            # iterate over constants to be added if available
            if len(constants) != 0:
                for cs in constants:
                    commandstring += f",{cs}"
            commandstring += ")"

            self.mycomms.write(commandstring)

        def save(self, buffername, filename, **kwargs):
            """This function saves data from the specified reading buffer to a USB flash drive."""
            for k in kwargs:
                if k == 'timeformat':
                    print("")
            f"buffer.save({buffername},\"{filename}\")"
            f"buffer.save({buffername},\"{filename}\",timeformat)"
            f"buffer.save({buffername},\"{filename}\",timeformat,start,end)"

        def saveappend(self, buffername, filename, **kwargs):
            """This function saves data from the specified reading buffer to a USB flash drive."""
            for k in kwargs:
                if k == 'timeformat':
                    print("")
            f"buffer.saveappend({buffername},\"{filename}\")"
            f"buffer.saveappend({buffername},\"{filename}\",timeformat)"
            f"buffer.saveappend({buffername},\"{filename}\",timeformat,start,end)"

        def unit(self):
            """This function allows you to create up to three custom units of measure for use in buffers."""
            f"buffer.unit(buffer.UNIT_CUSTOMN, unitOfMeasure)"

    class MeasureConfiguration:
        def __init__(self):
            self.range = None
            self.mycomms = None
            self.autozero = self.AutoZero()
            self.configlist = self.ConfigList()
            self.filter = self.Filter()
            self.limit = self.Limit()
            self.math = self.Math()
            self.rel = self.Rel()

        def update_comms(self):
            """
            This function is used to ensure lower level consumer classes tied to the driver are updated to promote \
            instrument communications.

            :return:
            """
            self.autozero.mycomms = self.mycomms
            self.configlist.mycomms = self.mycomms
            self.filter.mycomms = self.mycomms
            self.limit.mycomms = self.mycomms
            self.math.mycomms = self.mycomms
            self.rel.mycomms = self.mycomms

        @property
        def autorange(self):
            """
            This attribute determines if the measurement range is set manually or automatically for the selected \
            measure function.

            :return: Either 0 (smu.OFF) or 1 (smu.ON)
            """
            arange = None
            self.mycomms.write("autorange = smu.measure.autorange")
            response = self.mycomms.query("print(autorange)").rstrip()
            if "ON" in response:
                arange = smuconst.ON
            else:
                arange = smuconst.OFF
            return arange

        @autorange.setter
        def autorange(self, value):
            """
            This attribute determines if the measurement range is set manually or automatically for the selected \
            measure function.

            :param value: Either 1 (ON) or 0 (OFF)
            :return:
            """
            if value == smuconst.ON:
                self.mycomms.write("smu.measure.autorange=smu.ON")
            else:
                self.mycomms.write("smu.measure.autorange=smu.OFF")

        @property
        def autorangehigh(self):
            """
            When autorange is selected, this attribute represents the highest measurement range that is used when the \
            instrument selects the measurement range automatically.

            :return: highrange (float) - a value representative of a valid instrument range
            """
            highrange = None
            self.mycomms.write("highRange = smu.measure.autorangehigh")
            highrange = float(self.mycomms.query("print(highRange)").rstrip())
            return highrange

        @autorangehigh.setter
        def autorangehigh(self, range_value):
            """
            When autorange is selected, this attribute represents the highest measurement range that is used when the \
            instrument selects the measurement range automatically.

            :param range_value: (float) A value representative of a valid instrument range
            :return:
            """
            self.mycomms.write(f"smu.measure.autorangehigh={range_value}")

        @property
        def autorangelow(self):
            """
            When autorange is selected, this attribute represents the lowest measurement range that is used when the \
            instrument selects the measurement range automatically.

            :return: lowrange (float) - a value representative of a valid instrument range
            """
            lowrange = None
            self.mycomms.write("lowRange = smu.measure.autorangelow")
            highrange = float(self.mycomms.query("print(lowRange)").rstrip())
            return lowrange

        @autorangelow.setter
        def autorangelow(self, range_value):
            """
            When autorange is selected, this attribute represents the lowest measurement range that is used when the \
            instrument selects the measurement range automatically.

            :param range_value: (float) A value representative of a valid instrument range
            :return:
            """
            self.mycomms.write(f"smu.measure.autorangehigh={range_value}")

        @property
        def autorangerebound(self):
            """
            This attribute determines if the instrument restores the measure range to match the limit range after \
            making a measurement.

            :return: Either 1 (ON) or 0 (OFF)
            """
            self.mycomms.write("state = smu.measure.autorangerebound")
            response = self.mycomms.query("print(state)").rstrip()
            retconstval = None
            if "ON" in response:
                retconstval = smuconst.ON
            else:
                retconstval = smuconst.OFF
            return retconstval

        @autorangerebound.setter
        def autorangerebound(self, state):
            """
            This attribute determines if the instrument restores the measure range to match the limit range after \
            making a measurement.

            :param state: Either 1 (ON) or 0 (OFF)
            :return:
            """
            if state == smuconst.ON:
                self.mycomms.write("smu.measure.autorangerebound=smu.ON")
            else:
                self.mycomms.write("smu.measure.autorangerebound=smu.OFF")

        class AutoZero:
            def __init__(self):
                self.mycomms = None

            @property
            def enable(self):
                """
                This attribute enables or disables automatic updates to the internal reference measurements (autozero) \
                of the instrument.

                :return: Either 1 (ON) or 0 (OFF)
                """
                self.mycomms.write("state = smu.measure.autorange.enable")
                response = self.mycomms.query("print(state)").rstrip()
                retconstval = None
                if "ON" in response:
                    retconstval = smuconst.ON
                else:
                    retconstval = smuconst.OFF
                return retconstval

            @enable.setter
            def enable(self, state):
                """
                This attribute enables or disables automatic updates to the internal reference measurements (autozero) \
                of the instrument.

                :param state: Either 1 (ON) or 0 (OFF)
                :return:
                """
                if state == smuconst.ON:
                    self.mycomms.write("smu.measure.autorange.enable=smu.ON")
                else:
                    self.mycomms.write("smu.measure.autorange.enable=smu.OFF")

            def once(self):
                """
                This function causes the instrument to refresh the reference and zero measurements once.

                :return:
                """
                self.mycomms.write("smu.measure.autorange.once()")

        class ConfigList:
            def __init__(self):
                self.mycomms = None

            def catalog(self):
                """
                This function returns the name of one measure configuration list that is stored on the instrument.

                :return: The name of a configuration list.
                """
                self.mycomms.query("print(smu.measure.configlist.catalog())")

            def create(self, list_name):
                """
                This function creates an empty measure configuration list.

                :param list_name:
                :return:
                """
                self.mycomms.write(f"smu.measure.configlist.create({list_name}))")

            def delete(self, list_name, index=None):
                """
                This function deletes a measure configuration list.

                :param list_name:
                :param index:
                :return:
                """
                if index == None:
                    self.mycomms.write(f"smu.measure.configlist.delete(\"{list_name}\"))")
                else:
                    self.mycomms.write(f"smu.measure.configlist.delete(\"{list_name}\", {index}))")

            def query(self, list_name, index, field_separator=None):
                """
                This function returns a list of TSP commands and parameter settings that are stored in the specified \
                configuration index

                :param list_name: A string that represents the name of a measure configuration list
                :param index: A number that defines a specific configuration index in the configuration list
                :param field_separator: String that represents the separator for the data; use one of the following,
                                * Comma (default): ,
                                * Semicolon: ;
                                * New line: \n

                :return:
                """
                if field_separator == None:
                    self.mycomms.query(f"print(smu.measure.configlist.query(\"{list_name}\", {index}))")
                else:
                    self.mycomms.query(f"print(smu.measure.configlist.query(\"{list_name}\", {index}, {field_separator}))")

            def recall(self, list_name, index=None, source_list_name=None, source_index=None):
                """
                This function recalls a configuration index in a measure configuration list and an optional source \
                configuration list.

                :param list_name:
                :param index:
                :param source_list_name:
                :param source_index:
                :return:
                """
                if source_index == None:
                    if index == None:
                        self.mycomms.write(f"smu.measure.configlist.recall(\"{list_name}\")")
                    else:
                        self.mycomms.write(f"smu.measure.configlist.recall(\"{list_name}\", {index})")
                else:
                    if source_index == None:
                        self.mycomms.write(
                            f"smu.measure.configlist.recall(\"{list_name}\", {index}),\"{source_list_name}\")")
                    else:
                        self.mycomms.write(
                            f"smu.measure.configlist.recall(\"{list_name}\", {index}),\"{source_list_name}\","
                            f" {source_index})")

            def size(self, list_name):
                """
                This function returns the size (number of configuration indexes) of a measure configuration list.

                :param list_name:
                :return:
                """
                self.mycomms.write(f"index_count = smu.measure.configlist.zier(\"{list_name}\")")
                return int(self.mycomms.query("print(index_count)"))

            def store(self, list_name, index=None):
                """
                This function stores the active measure settings into the named configuration list.

                :param list_name:
                :param index:
                :return:
                """
                if index == None:
                    self.mycomms.write(f"smu.measure.configlist.store(\"{list_name}\")")
                else:
                    self.mycomms.write(f"smu.measure.configlist.store(\"{list_name}\", {index})")

            def storefunc(self, list_name, function, index=None):
                """
                This function allows you to store the settings for a measure function into a measure configuration \
                list whether or not the function is active.

                :param list_name:
                :param function:
                :param index:
                :return:
                """
                function_str = None
                if function == smuconst.FUNC_DC_VOLTAGE:
                    function_str = "smu.FUNC_DC_VOLTAGE"
                elif function == smuconst.FUNC_DC_CURRENT:
                    function_str = "smu.FUNC_DC_VOLTAGE"
                elif function == smuconst.FUNC_DC_RESISTANCE:
                    function_str = "smu.FUNC_DC_RESISTANCE"

                if index == None:
                    self.mycomms.write(f"smu.measure.configlist.storefunc(\"{list_name}\", {function_str})")
                else:
                    self.mycomms.write(f"smu.measure.configlist.storefunc(\"{list_name}\", {function_str}, {index})")

        @property
        def count(self):
            """
            This attribute gets the number of measurements to make when a measurement is requested.

            :return: count
            """
            self.mycomms.write("count=smu.measure.count")
            count = int(self.mycomms.query("print(count)").rstrip())
            return count

        @count.setter
        def count(self, count):
            """
            This attribute sets the number of measurements to make when a measurement is requested.

            :param count:
            :return:
            """
            self.mycomms.write(f"smu.measure.count={count}")

        @property
        def displaydigits(self):
            """
            This attribute determines the number of digits that are displayed for measurements on the front panel \
            for the selected function.
            
            :return: 
            """""
            self.mycomms.write("digits=smu.measure.displaydigits")
            digits = int(self.mycomms.query("print(digits)").rstrip())
            return digits

        @displaydigits.setter
        def displaydigits(self, digits):
            """
            This attribute determines the number of digits that are displayed for measurements on the front panel \
            for the selected function.

            :param digits:
            :return:
            """
            self.mycomms.write(f"smu.measure.displaydigits={digits}")

        @property
        def function(self):
            """
            This attribute contains the measure function, which can be voltage or current.

            :return: Either 0 (FUNC_DC_VOLTAGE) or 1 (FUNC_DC_CURRENT)
            """
            self.mycomms.write("measfunc = smu.measure.func")
            response = self.mycomms.query("print(measfunc)").rstrip()
            retconstval = None
            if "VOLTAGE" in response:
                retconstval = smuconst.FUNC_DC_VOLTAGE
            else:
                retconstval = smuconst.FUNC_DC_CURRENT
            return retconstval

        @function.setter
        def function(self, func):
            """
            This attribute contains the measure function, which can be voltage or current.

            :param func: Either 0 (FUNC_DC_VOLTAGE) or 1 (FUNC_DC_CURRENT)
            :return:
            """
            if func == smuconst.FUNC_DC_VOLTAGE:
                self.mycomms.write("smu.measure.func = smu.FUNC_DC_VOLTAGE")
                # print()
            else:
                self.mycomms.write("smu.measure.func = smu.FUNC_DC_CURRENT")

        class Filter:
            def __init__(self):
                self.mycomms = None

            @property
            def fcount(self):
                """
                This attribute sets the number of measurements that are averaged when filtering is enabled.

                :return: count
                """
                self.mycomms.write("filterCount=smu.measure.filter.count")
                count = int(self.mycomms.query("print(filterCount)").rstrip())
                return count

            @fcount.setter
            def fcount(self, count):
                """
                This attribute sets the number of measurements that are averaged when filtering is enabled.

                :param count:
                :return:
                """
                self.mycomms.write(f"smu.measure.filter.count={count}")

            @property
            def enable(self):
                """
                This attribute enables or disables the averaging filter for the selected measurement function.

                :return: Either 0 (OFF) or 1 (ON)
                """
                self.mycomms.write("filterState = smu.measure.filter.enable")
                response = self.mycomms.query("print(filterState)").rstrip()
                retconstval = None
                if "OFF" in response:
                    retconstval = smuconst.OFF
                else:
                    retconstval = smuconst.ON
                return retconstval

            @enable.setter
            def enable(self, state):
                """
                This attribute enables or disables the averaging filter for the selected measurement function.

                :param state: Either 0 (OFF) or 1 (ON)
                :return:
                """
                if state == smuconst.OFF:
                    self.mycomms.write("smu.measure.filter.enable=smu.OFF")
                else:
                    self.mycomms.write("smu.measure.filter.enable=smu.ON")

            @property
            def type(self):
                """
                This attribute gets the type of averaging filter that is used for the selected measure function when \
                the measurement filter is enabled.

                :return:
                """
                self.mycomms.write("filterType = smu.measure.filter.type")
                filtertype = self.mycomms.query("print(filterType)").rstrip()
                retconstval = None
                if "MOVING" in filtertype:
                    retconstval = smuconst.FILTER_MOVING_AVG
                else:
                    retconstval = smuconst.FILTER_REPEAT_AVG
                return retconstval

            @type.setter
            def type(self, filtertype):
                """
                This attribute sets the type of averaging filter that is used for the selected measure function when \
                the measurement filter is enabled.

                :param filtertype:
                :return:
                """
                if filtertype == smuconst.FILTER_MOVING_AVG:
                    self.mycomms.write("smu.measure.filter.type=smu.FILTER_MOVING_AVG")
                else:
                    self.mycomms.write("smu.measure.filter.enable=smu.FILTER_REPEAT_AVG")

        class Limit:
            def __init__(self):
                self.mycomms = None

            def audible(self, limit_number, state=None):
                """
                This attribute determines if the instrument beeper sounds when a limit test passes or fails.

                :param limit_number: Either 1 or 2
                :param state: Either 0 (AUDIBLE_NONE), 1 (AUDIBLE_FAIL), or 2 (AUDIBLE_PASS)
                :return: When state is not None, this function is used to return the present audible limit setting
                """
                retconstval = None

                if state is None:
                    self.mycomms.write(f"state=smu.measure.limit[{limit_number}].audible")
                    audible = self.mycomms.query("print(state)").rstrip()
                    if "NONE" in audible:
                        retconstval = smuconst.AUDIBLE_NONE
                    elif "FAIL" in audible:
                        retconstval = smuconst.AUDIBLE_FAIL
                    elif "PASS" in audible:
                        retconstval = smuconst.AUDIBLE_PASS
                else:
                    if state == smuconst.AUDIBLE_NONE:
                        self.mycomms.write(f"smu.measure.limit[{limit_number}].audible = smu.AUDIBLE_NONE")
                    elif state == smuconst.AUDIBLE_FAIL:
                        self.mycomms.write(f"smu.measure.limit[{limit_number}].audible = smu.AUDIBLE_FAIL")
                    elif state == smuconst.AUDIBLE_PASS:
                        self.mycomms.write(f"smu.measure.limit[{limit_number}].audible = smu.AUDIBLE_PASS")
                return retconstval

            def autoclear(self, limit_number, state=None):
                """
                This attribute indicates if the test result for limit Y should be cleared automatically or not.

                :param limit_number: Either 1 or 2
                :param state: Either 0 (OFF) or 1 (ON)
                :return: When state is not None, this function is used to return the present autoclear limit setting
                """
                retconstval = None

                if state is None:
                    self.mycomms.write(f"state=smu.measure.limit[{limit_number}].autoclear")
                    audible = self.mycomms.query("print(state)").rstrip()
                    if "ON" in audible:
                        retconstval = smuconst.ON
                    elif "OFF" in audible:
                        retconstval = smuconst.OFF
                else:
                    if state == smuconst.ON:
                        self.mycomms.write(f"smu.measure.limit[{limit_number}].autoclear = smu.ON")
                    elif state == smuconst.OFF:
                        self.mycomms.write(f"smu.measure.limit[{limit_number}].autoclear = smu.OFF")
                return retconstval

            def clear(self, limit_number):
                """
                This function clears the results of the limit test defined by limit_number for the selected \
                measurement function.

                :param limit_number: Either 1 or 2
                :return:
                """
                self.mycomms.write(f"smu.measure.limit[{limit_number}].clear()")

            def enable(self, limit_number, state=None):
                """
                This attribute enables or disables a limit test on the measurement from the selected measure function.

                :param limit_number: Either 1 or 2
                :param state: Either 0 (OFF) or 1 (ON)
                :return: When state is not None, this function is used to return the present enable limit setting
                """
                retconstval = None

                if state is None:
                    self.mycomms.write(f"state=smu.measure.limit[{limit_number}].enable")
                    audible = self.mycomms.query("print(state)").rstrip()
                    if "ON" in audible:
                        retconstval = smuconst.ON
                    elif "OFF" in audible:
                        retconstval = smuconst.OFF
                else:
                    if state == smuconst.ON:
                        self.mycomms.write(f"smu.measure.limit[{limit_number}].enable = smu.ON")
                    elif state == smuconst.OFF:
                        self.mycomms.write(f"smu.measure.limit[{limit_number}].enable = smu.OFF")
                return retconstval

            def fail(self, limit_number):
                """
                This attribute queries the results of a limit test.

                :param limit_number: Either 1 or 2
                :return: Either 0 (FAIL_NONE), 1 (FAIL_HIGH), 2 (FAIL_LOW), 3 (FAIL_BOTH).
                """
                retconstval = None

                self.mycomms.write(f"result=smu.measure.limit[{limit_number}].fail")
                audible = self.mycomms.query("print(result)").rstrip()

                if "NONE" in audible:
                    retconstval = smuconst.FAIL_NONE
                elif "HIGH" in audible:
                    retconstval = smuconst.FAIL_HIGH
                elif "LOW" in audible:
                    retconstval = smuconst.FAIL_LOW
                elif "BOTH" in audible:
                    retconstval = smuconst.FAIL_BOTH

                return retconstval

            def value(self, limit_number, high_or_low, value):
                """
                This function is used to either set or get the upper or lower limit for a limit test

                :param limit_number: Either 1 or 2
                :param high_or_low: Either 1 (FAIL_HIGH) or 2 (FAIL_LOW)
                :param value: The level at which either the high or low limit will be set.
                :return: When value is not None, this function is used to return the present limit value setting
                """
                limit_value = 0.0
                if value is None:
                    if high_or_low == smuconst.FAIL_HIGH:
                        self.mycomms.write(f"highLimit=smu.measure.limit[{limit_number}].high.value")
                        limit_value = self.mycomms.query("print(highLimit)").rstrip()
                    elif high_or_low == smuconst.FAIL_LOW:
                        self.mycomms.write(f"lowLimit=smu.measure.limit[{limit_number}].low.value")
                        limit_value = self.mycomms.query("print(lowLimit)").rstrip()
                else:
                    if high_or_low == smuconst.FAIL_HIGH:
                        self.mycomms.write(f"smu.measure.limit[{limit_number}].high.value = {value}")
                    elif high_or_low == smuconst.FAIL_LOW:
                        self.mycomms.write(f"smu.measure.limit[{limit_number}].low.value = {value}")

                return limit_value

        class Math:
            def __init__(self):
                self.mycomms = None

            def enable(self, state=None):
                """
                This attribute enables or disables math operations on measurements for the selected measurement \
                function.

                :param state: Either 1 (ON) or 0 (OFF)
                :return: Either 1 (ON) or 0 (OFF)
                """
                retconstval = None

                if state is None:
                    self.mycomms.write(f"state = smu.measure.math.enable")
                    state = self.mycomms.query("print(state)").rstrip()
                    if "ON" in state:
                        retconstval = smuconst.ON
                    elif "OFF" in state:
                        retconstval = smuconst.OFF
                else:
                    if state == smuconst.ON:
                        self.mycomms.write(f"smu.measure.math.enable = smu.ON")
                    elif state == smuconst.OFF:
                        self.mycomms.write(f"smu.measure.math.enable = smu.OFF")
                return retconstval

            def format(self, operation):
                """
                This attribute specifies which math operation is performed on measurements when math operations are \
                enabled.

                :param operation: Either MX+B (0), PERCENT (1), or RECIPROCAL (2)
                :return: Either MX+B (0), PERCENT (1), or RECIPROCAL (2)
                """
                retconstval = None

                if operation is None:
                    self.mycomms.write(f"operation = smu.measure.math.format")
                    operation = self.mycomms.query("print(operation)").rstrip()
                    if "MXB" in operation:
                        retconstval = smuconst.MATH_MXB
                    elif "PERCENT" in operation:
                        retconstval = smuconst.MATH_PERCENT
                    elif "RECPROCAL" in operation:
                        retconstval = smuconst.MATH_RECIPROCAL
                else:
                    if operation == smuconst.MATH_MXB:
                        self.mycomms.write(f"smu.measure.math.format = smu.MATH_MXB")
                    elif operation == smuconst.MATH_PERCENT:
                        self.mycomms.write(f"smu.measure.math.format = smu.PERCENT")
                    elif operation == smuconst.MATH_RECIPROCAL:
                        self.mycomms.write(f"smu.measure.math.format = smu.RECIPROCAL")
                return retconstval

            def mxb_bfactor(self, value):
                """
                This attribute specifies the offset, b, for the y = mx + b operation.

                :param value: The offset for the y = mx + b operation; the valid range is −1e12 to +1e12
                :return: Present setting for the b (offset) factor of the mx+b math operation.
                """
                retconstval = None

                if value is None:
                    self.mycomms.write(f"value = smu.measure.math.mxb.bfactor")
                    value = self.mycomms.query("print(value)").rstrip()
                    retconstval = value
                else:
                    self.mycomms.write(f"smu.measure.math.mxb.bfactor = {value}")
                return retconstval

            def mxb_mfactor(self, value):
                """
                This attribute specifies the scale factor, m, for the y = mx + b math operation.

                :param value: The scale factor; the valid range is −1e12 to +1e12
                :return: Present setting for the m (scale) factor of the mx+b math operation.
                """
                retconstval = None

                if value is None:
                    self.mycomms.write(f"value = smu.measure.math.mxb.mfactor")
                    value = self.mycomms.query("print(value)").rstrip()
                    retconstval = value
                else:
                    self.mycomms.write(f"smu.measure.math.mxb.mfactor = {value}")
                return retconstval

            def percent(self, value):
                """
                This attribute specifies the reference constant that is used when math operations are set to percent.

                :param value: The reference used when the math operation is set to percent; the range is −1e12 to +1e12
                :return: The percent value set for the math function.
                """
                retconstval = None

                if value is None:
                    self.mycomms.write(f"value = smu.measure.math.percent")
                    value = self.mycomms.query("print(value)").rstrip()
                    retconstval = value
                else:
                    self.mycomms.write(f"smu.measure.math.percent = {value}")
                return retconstval

        @property
        def nplc(self):
            """
            This command gets the time that the input signal is measured for the selected function.

            :return: nplc
            """
            self.mycomms.write("nplc=smu.measure.nplc")
            nplc = float(self.mycomms.query("print(nplc)").rstrip())
            return nplc

        @nplc.setter
        def nplc(self, nplc):
            """
            This command sets the time that the input signal is measured for the selected function.

            :param nplc:
            :return:
            """
            self.mycomms.write(f"smu.measure.nplc={nplc}")

        @property
        def offsetcompensation(self):
            """
            This attribute determines if offset compensation is used.

            :return: Disable with 0 (OFF); enable with 1 (ON)
            """
            retval = None
            self.mycomms.write("state = smu.measure.offsetcompensation")
            state = self.mycomms.query("print(state)").rstrip()
            if "ON" in state:
                retval = smuconst.ON
            elif "OFF" in state:
                retval = smuconst.OFF
            return retval

        @offsetcompensation.setter
        def offsetcompensation(self, state):
            """
            This attribute determines if offset compensation is used.

            :param state: To disable, 0 (OFF); to enable 1 (ON)
            :return:
            """
            if state == smuconst.ON:
                self.mycomms.write(f"smu.measure.nplc=smu.ON")
            else:
                self.mycomms.write(f"smu.measure.nplc=smu.OFF")

        @property
        def range(self):
            """
            This attribute determines the positive full-scale measure range.

            :return: The applied measure range.
            """
            retval = None
            self.mycomms.write("rangeValue = smu.measure.range")
            state = self.mycomms.query("print(rangeValue)").rstrip()
            return retval

        @range.setter
        def range(self, rangeValue):
            """
            This attribute determines the positive full-scale measure range.

            :param rangeValue: Set to the maximum expected value to be measured
            :return:
            """
            self.mycomms.write(f"smu.measure.range={rangeValue}")

        def read(self, buffer_name=None):
            """
            This function makes measurements, places them in a reading buffer, and returns the last reading.

            :param buffer_name: The name of the reading buffer, which may be a default buffer (defbuffer1 or \
            defbuffer2) or a user-defined buffer; if no buffer is defined, it defaults to defbuffer1
            :return: The last reading of the measurement process
            """
            if buffer_name is None:
                reading = float(self.mycomms.query(f"print(smu.measure.read())").rstrip())
            else:
                reading = float(self.mycomms.query(f"print(smu.measure.read(\"{buffer_name}\")").rstrip())
            return reading

        def readwithtime(self, buffer_name=None):
            """
            This function initiates measurements and returns the last actual measurement and time information in UTC \
            format without using the trigger model

            :param buffer_name: The name of the reading buffer, which may be a default buffer (defbuffer1 or \
            defbuffer2) or a user-defined buffer; if no buffer is defined, it defaults to defbuffer1
            :return: reading - The last reading of the measurement process;
                     seocnds - Seconds in UTC format;
                     fractional - Fractional seconds;
            """
            if buffer_name is None:
                self.mycomms.write(f"reading,seconds,fractional=smu.measure.readwithtime())")
            else:
                self.mycomms.write(f"reading,seconds,fractional=smu.measure.readwithtime(\"{buffer_name}\")")
            reading = float(self.mycomms.query("print(reading)").rstrip())
            seconds = int(self.mycomms.query("print(seconds)").rstrip())
            fractional = float(self.mycomms.query("print(fractional)").rstrip())
            return reading, seconds, fractional

        class Rel:
            def __init__(self):
                self.mycomms = None

            def acquire(self):
                """
                This function acquires a measurement and stores it as the relative offset value.

                :return: The internal measurement acquired for the relative offset value.
                """
                self.mycomms.write("relativeValue = smu.measure.rel.acquire()")
                relative_value = float(self.mycomms.write("print(relative_value)").rstrip())
                return relative_value

            @property
            def enable(self):
                """
                This attribute enables or disables the application of a relative offset value to the measurement.

                :return: Disabled 0 (OFF); enabled 1 (ON)
                """
                retval = None
                self.mycomms.write("relEnable = smu.measure.rel.enable")
                state = self.mycomms.query("print(relEnable)").rstrip()
                if "ON" in state:
                    retval = smuconst.ON
                elif "OFF" in state:
                    retval = smuconst.OFF
                return retval

            @enable.setter
            def enable(self, state):
                """
                This attribute enables or disables the application of a relative offset value to the measurement.

                :param state: Disable with 0 (OFF); enable with 1 (ON)
                :return:
                """
                if state == smuconst.ON:
                    self.mycomms.write("smu.measure.rel.enable = smu.ON")
                elif state == smuconst.OFF:
                    self.mycomms.write("smu.measure.rel.enable = smu.OFF")

    class SourceConfiguration:
        def __init__(self):
            self.range = None
            self.mycomms = None
            self.configlist = self.ConfigList()
            self.protect = self.Protect()
            self.ilimit = self.ILimit()
            self.vlimit = self.VLimit()

        def update_comms(self):
            """This function is used to ensure lower level consumer classes tied to the driver are updated to promote instrument communications."""
            self.configlist.mycoms = self.mycomms
            self.protect.mycoms = self.mycomms
            self.ilimit.mycomms = self.mycomms
            self.vlimit.mycomms = self.mycomms

        class ConfigList:
            def __init__(self):
                self.mycoms = None

        class Protect:
            def __init__(self):
                self.mycoms = None

        @property
        def function(self):
            """This attribute contains the source function, which can be voltage or current."""
            self.mycomms.write("srcfunc = smu.source.func")
            response = self.mycomms.query("print(srcfunc)").rstrip()
            retconstval = None
            if "VOLTAGE" in response:
                retconstval = smuconst.FUNC_DC_VOLTAGE
            else:
                retconstval = smuconst.FUNC_DC_CURRENT
            return retconstval

        @function.setter
        def function(self, func):
            """This attribute contains the source function, which can be voltage or current."""
            if func == smuconst.FUNC_DC_VOLTAGE:
                self.mycomms.write("smu.source.func = smu.FUNC_DC_VOLTAGE")
                # print()
            else:
                self.mycomms.write("smu.source.func = smu.FUNC_DC_CURRENT")
                # print()

        @property
        def level(self):
            """This attribute immediately selects a fixed amplitude for the selected source function."""
            self.mycomms.write("srclev = smu.source.level")
            return float(self.mycomms.query("print(srclev)").rstrip())

        @level.setter
        def level(self, value):
            """This attribute immediately selects a fixed amplitude for the selected source function."""
            self.mycomms.write(f"smu.source.level = {value}")

        class ILimit:
            def __init__(self):
                self.mycomms = None

            @property
            def level(self):
                """This attribute selects the source limit for current measurements."""
                self.mycomms.write("ilimitlev = smu.source.ilimit.level")
                return float(self.mycomms.query("print(ilimitlev)").rstrip())

            @level.setter
            def level(self, value):
                """This attribute selects the source limit for current measurements."""
                self.mycomms.write(f"smu.source.ilimit.level = {value}")

            @property
            def tripped(self):
                """This attribute indicates if the source exceeded the limits that were set for the selected measurements."""
                self.mycomms.write("ilimittrip = smu.source.ilimit.tripped")
                return int(self.mycomms.query("print(ilimittrip)").rstrip())

        class VLimit:
            def __init__(self):
                self.mycomms = None

            @property
            def level(self):
                """This attribute selects the source limit for voltage measurements."""
                self.mycomms.write("vlimitlev = smu.source.vlimit.level")
                return float(self.mycomms.query("print(vlimitlev)").rstrip())

            @level.setter
            def level(self, value):
                """This attribute selects the source limit for voltage measurements."""
                self.mycomms.write(f"smu.source.vlimit.level = {value}")

            @property
            def tripped(self):
                """This attribute indicates if the source exceeded the limits that were set for the selected measurements."""
                self.mycomms.write("vlimittrip = smu.source.vlimit.tripped")
                return int(self.mycomms.query("print(vlimittrip)").rstrip())

    @property
    def terminals(self):
        """
        This attribute describes which set of input and output terminals the instrument is using

        :return: Either 0 (TERMINALS_FRONT) or 1 (TERMINALS_REAR)
        """
        term = None
        self.instrumentcomms.write("terminals = smu.terminals")
        if "FRONT" in self.instrumentcomms.query("print(terminals)").rstrip():
            term = smuconst.TERMINALS_FRONT
        else:
            term = smuconst.TERMINALS_REAR
        return term

    @terminals.setter
    def terminals(self, terminals):
        """
        This attribute describes which set of input and output terminals the instrument is using

        :param terminals: Either 0 (TERMINALS_FRONT) or 1 (TERMINALS_REAR)
        :return: None
        """
        if terminals == smuconst.TERMINALS_FRONT:
            self.instrumentcomms.write("smu.terminals=smu.TERMINALS_FRONT")
        else:
            self.instrumentcomms.write("smu.terminals=smu.TERMINALS_REAR")

    class TriggerConfiguration:
        def __init__(self):
            self.mycomms = None
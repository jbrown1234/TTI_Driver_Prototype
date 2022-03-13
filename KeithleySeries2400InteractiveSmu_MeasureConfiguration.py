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


class MeasureConfiguration:
    """
    Placeholder docstring description
    """
    def __init__(self):
        self._mycomms = None
        self.autozero = self.AutoZero()
        self.configlist = self.ConfigList()
        self.filter = self.Filter()
        self.limit = self.Limit()
        self.math = self.Math()
        self.rel = self.Rel()

    def update_comms(self):
        """
        This function is used to ensure lower level consumer classes tied to
        the driver are updated to promote instrument communications.

        :return:
        """
        self.autozero._mycomms = self._mycomms
        self.configlist._mycomms = self._mycomms
        self.filter._mycomms = self._mycomms
        self.limit._mycomms = self._mycomms
        self.math._mycomms = self._mycomms
        self.rel._mycomms = self._mycomms

    @property
    def autorange(self):
        """
        This attribute determines if the measurement range is set manually or
        automatically for the selected measure function.

        :return: Either 0 (smu.OFF) or 1 (smu.ON)
        """
        arange = None
        self._mycomms.write("autorange = smu.measure.autorange")
        response = self._mycomms.query("print(autorange)").rstrip()
        if "ON" in response:
            arange = _smuconst.ON
        else:
            arange = _smuconst.OFF
        return arange

    @autorange.setter
    def autorange(self, value):
        """
        This attribute determines if the measurement range is set manually
        or automatically for the selected measure function.

        :param value: Either 1 (ON) or 0 (OFF)
        :return:
        """
        if value == _smuconst.ON:
            self._mycomms.write("smu.measure.autorange=smu.ON")
        else:
            self._mycomms.write("smu.measure.autorange=smu.OFF")

    @property
    def autorangehigh(self):
        """
        When autorange is selected, this attribute represents the highest
        measurement range that is used when the instrument selects the
        measurement range automatically.

        :return: highrange (float) - a value representative of a valid
        instrument range
        """
        highrange = None
        self._mycomms.write("highRange = smu.measure.autorangehigh")
        highrange = float(self._mycomms.query("print(highRange)").rstrip())
        return highrange

    @autorangehigh.setter
    def autorangehigh(self, range_value):
        """
        When autorange is selected, this attribute represents the highest
        measurement range that is used when the instrument selects the
        measurement range automatically.

        :param range_value: (float) A value representative of a valid
        instrument range.
        :return:
        """
        self._mycomms.write(f"smu.measure.autorangehigh={range_value}")

    @property
    def autorangelow(self):
        """
        When autorange is selected, this attribute represents the lowest
        measurement range that is used when the instrument selects the
        measurement range automatically.

        :return: lowrange (float) - a value representative of a valid
        instrument range
        """
        lowrange = None
        self._mycomms.write("lowRange = smu.measure.autorangelow")
        highrange = float(self._mycomms.query("print(lowRange)").rstrip())
        return lowrange

    @autorangelow.setter
    def autorangelow(self, range_value):
        """
        When autorange is selected, this attribute represents the lowest
        measurement range that is used when the instrument selects the
        measurement range automatically.

        :param range_value: (float) A value representative of a valid
        instrument range
        :return:
        """
        self._mycomms.write(f"smu.measure.autorangehigh={range_value}")

    @property
    def autorangerebound(self):
        """
        This attribute determines if the instrument restores the measure range
        to match the limit range after making a measurement.

        :return: Either 1 (ON) or 0 (OFF)
        """
        self._mycomms.write("state = smu.measure.autorangerebound")
        response = self._mycomms.query("print(state)").rstrip()
        retconstval = None
        if "ON" in response:
            retconstval = _smuconst.ON
        else:
            retconstval = _smuconst.OFF
        return retconstval

    @autorangerebound.setter
    def autorangerebound(self, state):
        """
        This attribute determines if the instrument restores the measure range
        to match the limit range after making a measurement.

        :param state: Either 1 (ON) or 0 (OFF)
        :return:
        """
        if state == _smuconst.ON:
            self._mycomms.write("smu.measure.autorangerebound=smu.ON")
        else:
            self._mycomms.write("smu.measure.autorangerebound=smu.OFF")

    class AutoZero:
        """
        This subclass supports setting/getting autozero-based attributes.
        """
        def __init__(self):
            self._mycomms = None

        @property
        def enable(self):
            """
            This attribute enables or disables automatic updates to the 
            internal reference measurements (autozero) of the instrument.

            :return: Either 1 (ON) or 0 (OFF)
            """
            self._mycomms.write("state = smu.measure.autorange.enable")
            response = self._mycomms.query("print(state)").rstrip()
            retconstval = None
            if "ON" in response:
                retconstval = _smuconst.ON
            else:
                retconstval = _smuconst.OFF
            return retconstval

        @enable.setter
        def enable(self, state):
            """
            This attribute enables or disables automatic updates to the
            internal reference measurements (autozero) of the instrument.

            :param state: Either 1 (ON) or 0 (OFF)
            :return:
            """
            if state == _smuconst.ON:
                self._mycomms.write("smu.measure.autorange.enable=smu.ON")
            else:
                self._mycomms.write("smu.measure.autorange.enable=smu.OFF")

        def once(self):
            """
            This function causes the instrument to refresh the reference and
            zero measurements once.

            :return:
            """
            self._mycomms.write("smu.measure.autorange.once()")

    class ConfigList:
        """
        Subclass to support the creation & utilization of configuration lists.
        """
        def __init__(self):
            self._mycomms = None

        def catalog(self):
            """
            This function returns the name of one measure configuration list
            that is stored on the instrument.

            :return: The name of a configuration list.
            """
            self._mycomms.query("print(smu.measure.configlist.catalog())")

        def create(self, list_name):
            """
            This function creates an empty measure configuration list.

            :param list_name:
            :return:
            """
            self._mycomms.write(f"smu.measure.configlist.create({list_name}))")

        def delete(self, list_name, index=None):
            """
            This function deletes a measure configuration list.

            :param list_name:
            :param index:
            :return:
            """
            if index is None:
                self._mycomms.write(f"smu.measure.configlist.delete(\"\
                    {list_name}\"))")
            else:
                self._mycomms.write(f"smu.measure.configlist.delete(\"\
                    {list_name}\", {index}))")

        def query(self, list_name, index, field_separator=None):
            """
            This function returns a list of TSP commands and parameter settings
            that are stored in the specified configuration index

            :param list_name: A string that represents the name of a measure
            configuration list.
            :param index: A number that defines a specific configuration index
            in the configuration list.
            :param field_separator: String that represents the separator for
            the data; use one of the following,
                            * Comma (default): ,
                            * Semicolon: ;
                            * New line: \n

            :return:
            """
            if field_separator is None:
                self._mycomms.query(f"print(smu.measure.\
                    configlist.query(\"{list_name}\", {index}))")
            else:
                self._mycomms.query(f"print(smu.measure.\
                    configlist.query(\"{list_name}\", {index}, \
                        {field_separator}))")

        def recall(self, list_name, index=None, source_list_name=None,
                   source_index=None):
            """
            This function recalls a configuration index in a measure
            configuration list and an optional source configuration list.

            :param list_name:
            :param index:
            :param source_list_name:
            :param source_index:
            :return:
            """
            if source_index is None:
                if index is None:
                    self._mycomms.write(f"smu.measure.configlist.recall(\"\
                        {list_name}\")")
                else:
                    self._mycomms.write(f"smu.measure.configlist.recall(\"\
                        {list_name}\", {index})")
            else:
                if source_index is None:
                    self._mycomms.write(
                        f"smu.measure.configlist.recall(\"{list_name}\",\
                        {index}),\"{source_list_name}\")")
                else:
                    self._mycomms.write(
                        f"smu.measure.configlist.recall(\"{list_name}\",\
                        {index}),\"{source_list_name}\","
                            f" {source_index})")

        def size(self, list_name):
            """
            This function returns the size (number of configuration indexes)
            of a measure configuration list.

            :param list_name:
            :return:
            """
            self._mycomms.write(f"index_count = smu.measure.configlist.zier(\"\
                {list_name}\")")
            return int(self._mycomms.query("print(index_count)"))

        def store(self, list_name, index=None):
            """
            This function stores the active measure settings into the named
            configuration list.

            :param list_name:
            :param index:
            :return:
            """
            if index is None:
                self._mycomms.write(f"smu.measure.configlist.store(\"\
                    {list_name}\")")
            else:
                self._mycomms.write(f"smu.measure.configlist.store(\"\
                    {list_name}\", {index})")

        def storefunc(self, list_name, function, index=None):
            """
            This function allows you to store the settings for a measure
            function into a measure configuration list whether or not the
            function is active.

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
                self._mycomms.write(f"smu.measure.configlist.storefunc(\"\
                    {list_name}\", {function_str})")
            else:
                self._mycomms.write(f"smu.measure.configlist.storefunc(\"\
                    {list_name}\", {function_str}, {index})")

    @property
    def count(self):
        """
        This attribute gets the number of measurements to make when a
        measurement is requested.

        :return: count
        """
        self._mycomms.write("count=smu.measure.count")
        count = int(self._mycomms.query("print(count)").rstrip())
        return count

    @count.setter
    def count(self, measure_count):
        """
        This attribute sets the number of measurements to make when a
        measurement is requested.

        :param count:
        :return: None
        """
        self._mycomms.write(f"smu.measure.count={measure_count}")

    @property
    def displaydigits(self):
        """
        This attribute determines the number of digits that are displayed for
        measurements on the front panel for the selected function.

        :return: digits
        """""
        self._mycomms.write("digits=smu.measure.displaydigits")
        digits = int(self._mycomms.query("print(digits)").rstrip())
        return digits

    @displaydigits.setter
    def displaydigits(self, digits):
        """
        This attribute determines the number of digits that are displayed for
        measurements on the front panel for the selected function.

        :param digits:
        :return:
        """
        self._mycomms.write(f"smu.measure.displaydigits={digits}")

    @property
    def function(self):
        """
        This attribute contains the measure function, which can be voltage or
        current.

        :return: Either 0 (FUNC_DC_VOLTAGE) or 1 (FUNC_DC_CURRENT)
        """
        self._mycomms.write("measfunc = smu.measure.func")
        response = self._mycomms.query("print(measfunc)").rstrip()
        retconstval = None
        if "VOLTAGE" in response:
            retconstval = _smuconst.FUNC_DC_VOLTAGE
        elif "CURRENT" in response:
            retconstval = _smuconst.FUNC_DC_CURRENT
        elif "RESISTANCE" in response:
            retconstval = _smuconst.FUNC_RESISTANCE
        return retconstval

    @function.setter
    def function(self, func):
        """
        This attribute contains the measure function, which can be voltage or
        current.

        :param func: Either 0 (FUNC_DC_VOLTAGE) or 1 (FUNC_DC_CURRENT)
        :return:
        """
        if func == _smuconst.FUNC_DC_VOLTAGE:
            self._mycomms.write("smu.measure.func = smu.FUNC_DC_VOLTAGE")
            # print()
        elif func == _smuconst.FUNC_DC_CURRENT:
            self._mycomms.write("smu.measure.func = smu.FUNC_DC_CURRENT")
        elif func == _smuconst.FUNC_RESISTANCE:
            self._mycomms.write("smu.measure.func = smu.FUNC_RESISTANCE")

    class Filter:
        """
        This subclass support setting/getting filter-based attributes.
        """
        def __init__(self):
            self._mycomms = None

        @property
        def fcount(self):
            """
            This attribute sets the number of measurements that are averaged
            when filtering is enabled.

            :return: count
            """
            self._mycomms.write("filterCount=smu.measure.filter.count")
            count = int(self._mycomms.query("print(filterCount)").rstrip())
            return count

        @fcount.setter
        def fcount(self, count):
            """
            This attribute sets the number of measurements that are averaged
            when filtering is enabled.

            :param count:
            :return:
            """
            self._mycomms.write(f"smu.measure.filter.count={count}")

        @property
        def enable(self):
            """
            This attribute enables or disables the averaging filter for the
            selected measurement function.

            :return: Either 0 (OFF) or 1 (ON)
            """
            self._mycomms.write("filterState = smu.measure.filter.enable")
            response = self._mycomms.query("print(filterState)").rstrip()
            retconstval = None
            if "OFF" in response:
                retconstval = _smuconst.OFF
            else:
                retconstval = _smuconst.ON
            return retconstval

        @enable.setter
        def enable(self, state):
            """
            This attribute enables or disables the averaging filter for the
            selected measurement function.

            :param state: Either 0 (OFF) or 1 (ON)
            :return:
            """
            if state == _smuconst.OFF:
                self._mycomms.write("smu.measure.filter.enable=smu.OFF")
            else:
                self._mycomms.write("smu.measure.filter.enable=smu.ON")

        @property
        def type(self):
            """
            This attribute gets the type of averaging filter that is used for
            the selected measure function when the measurement filter is 
            enabled.

            :return:
            """
            self._mycomms.write("filterType = smu.measure.filter.type")
            filtertype = self._mycomms.query("print(filterType)").rstrip()
            retconstval = None
            if "MOVING" in filtertype:
                retconstval = _smuconst.FILTER_MOVING_AVG
            else:
                retconstval = _smuconst.FILTER_REPEAT_AVG
            return retconstval

        @type.setter
        def type(self, filtertype):
            """
            This attribute sets the type of averaging filter that is used for
            the selected measure function when the measurement filter is
            enabled.

            :param filtertype:
            :return:
            """
            if filtertype == _smuconst.FILTER_MOVING_AVG:
                self._mycomms.write("smu.measure.filter.type=\
                    smu.FILTER_MOVING_AVG")
            else:
                self._mycomms.write("smu.measure.filter.enable=\
                    smu.FILTER_REPEAT_AVG")

    class Limit:
        """
        This subclass supports setting/getting limit-based attributes.
        """
        def __init__(self):
            self._mycomms = None

        def audible(self, limit_number, state=None):
            """
            This attribute determines if the instrument beeper sounds when a
            limit test passes or fails.

            :param limit_number: Either 1 or 2
            :param state: Either 0 (AUDIBLE_NONE), 1 (AUDIBLE_FAIL), or 2
            (AUDIBLE_PASS)
            :return: When state is not None, this function is used to return
            the present audible limit setting
            """
            retconstval = None

            if state is None:
                self._mycomms.write(f"state=smu.measure.limit[{limit_number}].\
                    audible")
                audible = self._mycomms.query("print(state)").rstrip()
                if "NONE" in audible:
                    retconstval = _smuconst.AUDIBLE_NONE
                elif "FAIL" in audible:
                    retconstval = _smuconst.AUDIBLE_FAIL
                elif "PASS" in audible:
                    retconstval = _smuconst.AUDIBLE_PASS
            else:
                if state == _smuconst.AUDIBLE_NONE:
                    self._mycomms.write(f"smu.measure.limit[{limit_number}].\
                        audible = smu.AUDIBLE_NONE")
                elif state == _smuconst.AUDIBLE_FAIL:
                    self._mycomms.write(f"smu.measure.limit[{limit_number}].\
                        audible = smu.AUDIBLE_FAIL")
                elif state == _smuconst.AUDIBLE_PASS:
                    self._mycomms.write(f"smu.measure.limit[{limit_number}].\
                        audible = smu.AUDIBLE_PASS")
            return retconstval

        def autoclear(self, limit_number, state=None):
            """
            This attribute indicates if the test result for limit Y should be
            cleared automatically or not.

            :param limit_number: Either 1 or 2
            :param state: Either 0 (OFF) or 1 (ON)
            :return: When state is not None, this function is used to return
            the present autoclear limit setting
            """
            retconstval = None

            if state is None:
                self._mycomms.write(f"state=smu.measure.limit[{limit_number}].\
                    autoclear")
                audible = self._mycomms.query("print(state)").rstrip()
                if "ON" in audible:
                    retconstval = _smuconst.ON
                elif "OFF" in audible:
                    retconstval = _smuconst.OFF
            else:
                if state == _smuconst.ON:
                    self._mycomms.write(f"smu.measure.limit[{limit_number}].\
                        autoclear = smu.ON")
                elif state == _smuconst.OFF:
                    self._mycomms.write(f"smu.measure.limit[{limit_number}].\
                        autoclear = smu.OFF")
            return retconstval

        def clear(self, limit_number):
            """
            This function clears the results of the limit test defined by
            limit_number for the selected measurement function.

            :param limit_number: Either 1 or 2
            :return:
            """
            self._mycomms.write(f"smu.measure.limit[{limit_number}].clear()")

        def enable(self, limit_number, state=None):
            """
            This attribute enables or disables a limit test on the measurement
            from the selected measure function.

            :param limit_number: Either 1 or 2
            :param state: Either 0 (OFF) or 1 (ON)
            :return: When state is not None, this function is used to return
            the present enable limit setting
            """
            retconstval = None

            if state is None:
                self._mycomms.write(f"state=smu.measure.limit[{limit_number}].\
                    enable")
                audible = self._mycomms.query("print(state)").rstrip()
                if "ON" in audible:
                    retconstval = _smuconst.ON
                elif "OFF" in audible:
                    retconstval = _smuconst.OFF
            else:
                if state == _smuconst.ON:
                    self._mycomms.write(f"smu.measure.limit[{limit_number}].\
                        enable = smu.ON")
                elif state == _smuconst.OFF:
                    self._mycomms.write(f"smu.measure.limit[{limit_number}].\
                        enable = smu.OFF")
            return retconstval

        def fail(self, limit_number):
            """
            This attribute queries the results of a limit test.

            :param limit_number: Either 1 or 2
            :return: Either 0 (FAIL_NONE), 1 (FAIL_HIGH), 2 (FAIL_LOW), 3
            (FAIL_BOTH).
            """
            retconstval = None

            self._mycomms.write(f"result=smu.measure.limit[{limit_number}].\
                fail")
            audible = self._mycomms.query("print(result)").rstrip()

            if "NONE" in audible:
                retconstval = _smuconst.FAIL_NONE
            elif "HIGH" in audible:
                retconstval = _smuconst.FAIL_HIGH
            elif "LOW" in audible:
                retconstval = _smuconst.FAIL_LOW
            elif "BOTH" in audible:
                retconstval = _smuconst.FAIL_BOTH

            return retconstval

        def value(self, limit_number, high_or_low, value):
            """
            This function is used to either set or get the upper or lower
            limit for a limit test

            :param limit_number: Either 1 or 2
            :param high_or_low: Either 1 (FAIL_HIGH) or 2 (FAIL_LOW)
            :param value: The level at which either the high or low limit will
            be set.
            :return: When value is not None, this function is used to return
            the present limit value setting
            """
            limit_value = 0.0
            if value is None:
                if high_or_low == _smuconst.FAIL_HIGH:
                    self._mycomms.write(f"highLimit=smu.measure.limit[\
                        {limit_number}].high.value")
                    limit_value = self._mycomms.query("print(highLimit)")\
                        .rstrip()
                elif high_or_low == _smuconst.FAIL_LOW:
                    self._mycomms.write(f"lowLimit=smu.measure.limit[\
                        {limit_number}].low.value")
                    limit_value = self._mycomms.query("print(lowLimit)").\
                        rstrip()
            else:
                if high_or_low == _smuconst.FAIL_HIGH:
                    self._mycomms.write(f"smu.measure.limit[{limit_number}].\
                        high.value = {value}")
                elif high_or_low == _smuconst.FAIL_LOW:
                    self._mycomms.write(f"smu.measure.limit[{limit_number}].\
                        low.value = {value}")

            return limit_value

    class Math:
        """
        This subclass supports setting/getting math attributes.
        """
        def __init__(self):
            self._mycomms = None

        def enable(self, state=None):
            """
            This attribute enables or disables math operations on measurements
            for the selected measurement function.

            :param state: Either 1 (ON) or 0 (OFF)
            :return: Either 1 (ON) or 0 (OFF)
            """
            retconstval = None

            if state is None:
                self._mycomms.write("state = smu.measure.math.enable")
                state = self._mycomms.query("print(state)").rstrip()
                if "ON" in state:
                    retconstval = _smuconst.ON
                elif "OFF" in state:
                    retconstval = _smuconst.OFF
            else:
                if state == _smuconst.ON:
                    self._mycomms.write("smu.measure.math.enable = smu.ON")
                elif state == _smuconst.OFF:
                    self._mycomms.write("smu.measure.math.enable = smu.OFF")
            return retconstval

        def format(self, operation):
            """
            This attribute specifies which math operation is performed on
            measurements when math operations are enabled.

            :param operation: Either MX+B (0), PERCENT (1), or RECIPROCAL (2)
            :return: Either MX+B (0), PERCENT (1), or RECIPROCAL (2)
            """
            retconstval = None

            if operation is None:
                self._mycomms.write("operation = smu.measure.math.format")
                operation = self._mycomms.query("print(operation)").rstrip()
                if "MXB" in operation:
                    retconstval = _smuconst.MATH_MXB
                elif "PERCENT" in operation:
                    retconstval = _smuconst.MATH_PERCENT
                elif "RECPROCAL" in operation:
                    retconstval = _smuconst.MATH_RECIPROCAL
            else:
                if operation == _smuconst.MATH_MXB:
                    self._mycomms.write("smu.measure.math.format = \
                        smu.MATH_MXB")
                elif operation == _smuconst.MATH_PERCENT:
                    self._mycomms.write("smu.measure.math.format = \
                        smu.PERCENT")
                elif operation == _smuconst.MATH_RECIPROCAL:
                    self._mycomms.write("smu.measure.math.format = \
                        smu.RECIPROCAL")
            return retconstval

        def mxb_bfactor(self, value):
            """
            This attribute specifies the offset, b, for the y = mx + b
            operation.

            :param value: The offset for the y = mx + b operation; the valid
            range is −1e12 to +1e12
            :return: Present setting for the b (offset) factor of the mx+b 
            math operation.
            """
            retconstval = None

            if value is None:
                self._mycomms.write("value = smu.measure.math.mxb.bfactor")
                value = self._mycomms.query("print(value)").rstrip()
                retconstval = value
            else:
                self._mycomms.write("smu.measure.math.mxb.bfactor = {value}")
            return retconstval

        def mxb_mfactor(self, value):
            """
            This attribute specifies the scale factor, m, for the y =
            mx + b math operation.

            :param value: The scale factor; the valid range is −1e12 to +1e12
            :return: Present setting for the m (scale) factor of the mx+b math
            operation.
            """
            retconstval = None

            if value is None:
                self._mycomms.write("value = smu.measure.math.mxb.mfactor")
                value = self._mycomms.query("print(value)").rstrip()
                retconstval = value
            else:
                self._mycomms.write("smu.measure.math.mxb.mfactor = {value}")
            return retconstval

        def percent(self, value):
            """
            This attribute specifies the reference constant that is used when
            math operations are set to percent.

            :param value: The reference used when the math operation is set
            to percent; the range is −1e12 to +1e12
            :return: The percent value set for the math function.
            """
            retconstval = None

            if value is None:
                self._mycomms.write("value = smu.measure.math.percent")
                value = self._mycomms.query("print(value)").rstrip()
                retconstval = value
            else:
                self._mycomms.write("smu.measure.math.percent = {value}")
            return retconstval

    @property
    def nplc(self):
        """
        This command gets the time that the input signal is measured for the
        selected function.

        :return: nplc
        """
        self._mycomms.write("nplc=smu.measure.nplc")
        nplc = float(self._mycomms.query("print(nplc)").rstrip())
        return nplc

    @nplc.setter
    def nplc(self, nplc):
        """
        This command sets the time that the input signal is measured for the
        selected function.

        :param nplc:
        :return:
        """
        self._mycomms.write(f"smu.measure.nplc={nplc}")

    @property
    def offsetcompensation(self):
        """
        This attribute determines if offset compensation is used.

        :return: Disable with 0 (OFF); enable with 1 (ON)
        """
        retval = None
        self._mycomms.write("state = smu.measure.offsetcompensation")
        state = self._mycomms.query("print(state)").rstrip()
        if "ON" in state:
            retval = _smuconst.ON
        elif "OFF" in state:
            retval = _smuconst.OFF
        return retval

    @offsetcompensation.setter
    def offsetcompensation(self, state):
        """
        This attribute determines if offset compensation is used.

        :param state: To disable, 0 (OFF); to enable 1 (ON)
        :return:
        """
        if state == _smuconst.ON:
            self._mycomms.write("smu.measure.offsetcompensation=smu.ON")
        else:
            self._mycomms.write("smu.measure.offsetcompensation=smu.OFF")

    @property
    def range(self):
        """
        This attribute determines the positive full-scale measure range.

        :return: The applied measure range.
        """
        self._mycomms.write("range_value = smu.measure.range")
        range_value = float(self._mycomms.query("print(range_value)").rstrip())
        return range_value

    @range.setter
    def range(self, range_value):
        """
        This attribute determines the positive full-scale measure range.

        :param range_value: Set to the maximum expected value to be measured
        :return:
        """
        self._mycomms.write(f"smu.measure.range={range_value}")

    def read(self, buffer_name=None):
        """
        This function makes measurements, places them in a reading buffer, and
        returns the last reading.

        :param buffer_name: The name of the reading buffer, which may be a
        default buffer (defbuffer1 or defbuffer2) or a user-defined buffer;
        if no buffer is defined, it defaults to defbuffer1
        :return: The last reading of the measurement process
        """
        if buffer_name is None:
            reading = float(self._mycomms.query("print(smu.measure.read())").
                            rstrip())
        else:
            reading = float(self._mycomms.query(f"print(smu.measure.read\
                ({buffer_name}))").rstrip())
        return reading

    def readwithtime(self, buffer_name=None):
        """
        This function initiates measurements and returns the last actual
        measurement and time information in UTC format without using the
        trigger model

        :param buffer_name: The name of the reading buffer, which may be a
        default buffer (defbuffer1 or defbuffer2) or a user-defined buffer;
        if no buffer is defined, it defaults to defbuffer1
        :return: reading - The last reading of the measurement process;
                 seocnds - Seconds in UTC format;
                 fractional - Fractional seconds;
        """
        if buffer_name is None:
            self._mycomms.write("reading,seconds,fractional=smu.measure.\
                readwithtime())")
        else:
            self._mycomms.write("reading,seconds,fractional=smu.measure.\
                readwithtime(\"{buffer_name}\")")
        reading = float(self._mycomms.query("print(reading)").rstrip())
        seconds = int(self._mycomms.query("print(seconds)").rstrip())
        fractional = float(self._mycomms.query("print(fractional)").rstrip())
        return reading, seconds, fractional

    class Rel:
        """
        This subclass support setting/getting of REL attributes.
        """
        def __init__(self):
            self._mycomms = None

        def acquire(self):
            """
            This function acquires a measurement and stores it as the relative
            offset value.

            :return: The internal measurement acquired for the relative offset
            value.
            """
            self._mycomms.write("relativeValue = smu.measure.rel.acquire()")
            relative_value = float(self._mycomms.write("print(relative_value)")
                                   .rstrip())
            return relative_value

        @property
        def enable(self):
            """
            This attribute enables or disables the application of a relative
            offset value to the measurement.

            :return: Disabled 0 (OFF); enabled 1 (ON)
            """
            retval = None
            self._mycomms.write("rel_enable = smu.measure.rel.enable")
            state = self._mycomms.query("print(rel_enable)").rstrip()
            if "ON" in state:
                retval = _smuconst.ON
            elif "OFF" in state:
                retval = _smuconst.OFF
            return retval

        @enable.setter
        def enable(self, state):
            """
            This attribute enables or disables the application of a relative
            offset value to the measurement.

            :param state: Disable with 0 (OFF); enable with 1 (ON)
            :return:
            """
            if state == _smuconst.ON:
                self._mycomms.write("smu.measure.rel.enable = smu.ON")
            elif state == _smuconst.OFF:
                self._mycomms.write("smu.measure.rel.enable = smu.OFF")

        @property
        def level(self):
            """
            This attribute contains the relative offset value.

            :return: Relative offset value for measurements.
            """
            self._mycomms.write("rel_level = smu.measure.rel.level")
            level = float(self._mycomms.query("print(rel_level)").rstrip())
            return level

        @level.setter
        def level(self, level):
            """
            This attribute contains the relative offset value.

            :param level: Relative offset value for measurements.
            :return:
            """
            self._mycomms.write(f"smu.measure.rel.level = {level}")

    @property
    def sense(self):
        """
        This attribute selects local (2-wire) or remote (4-wire) sensing.
        """
        self._mycomms.write("sense_type=smu.measure.sense")
        sense_type = self._mycomms.query("print(sense_type)")
        return sense_type

    @sense.setter
    def sense(self, sense_type=_smuconst.SENSE_2WIRE):

        sense_string = ""
        if sense_type is _smuconst.SENSE_2WIRE:
            sense_string = "smu.SENSE_2WIRE"
        else:
            sense_string = "smu.SENSE_4WIRE"
        self._mycomms.write(f"smu.measure.sense={sense_string}")

    @property
    def unit(self):
        """
        This attribute gets the units of measurement that are displayed on the
        front panel of the instrument and stored
        in the reading buffer.

        :return: The units of measure to be displayed for the measurement -
        UNIT_AMP, UNIT_OHM, UNIT_VOLT, or UNIT_WATT
        """
        self._mycomms.write("unit_of_measure=smu.measure.unit")
        unit_of_measure = self._mycomms.query("print(unit_of_measure)").rstrip()
        if "AMP" in unit_of_measure:
            return _smuconst.UNIT_AMP
        elif "OHM" in unit_of_measure:
            return _smuconst.UNIT_OHM
        elif "VOLT" in unit_of_measure:
            return _smuconst.UNIT_VOLT
        elif "WATT" in unit_of_measure:
            return _smuconst.UNIT_WATT
        return 0

    @unit.setter
    def unit(self, unit_of_measure=_smuconst.UNIT_AMP):
        """
        This attribute sets the units of measurement that are displayed on the
        front panel of the instrument and stored in the reading buffer.

        :param unit_of_measure: Set as either UNIT_AMP, UNIT_OHM, UNIT_VOLT, or
        UNIT_WATT.
        :return:
        """
        unit_string = ""
        if unit_of_measure is _smuconst.UNIT_AMP:
            unit_string = "smu.UNIT_AMP"
        elif unit_of_measure is _smuconst.UNIT_OHM:
            unit_string = "smu.UNIT_OHM"
        elif unit_of_measure is _smuconst.UNIT_VOLT:
            unit_string = "smu.UNIT_VOLT"
        elif unit_of_measure is _smuconst.UNIT_WATT:
            unit_string = "smu.UNIT_WATT"
        self._mycomms.write(f"smu.measure.unit={unit_string}")

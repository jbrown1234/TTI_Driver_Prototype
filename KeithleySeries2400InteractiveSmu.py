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
        """This function checks for the presence of specific instrument functionality."""
        self.instrumentcomms.write(f"presence = available({functionality})")

    def beep(self, frequency, duration):
        """This function generates an audible tone."""
        self.instrumentcomms.write(f"beeper.beep({frequency},{duration})")

    class Buffer:
        def __init__(self):
            self.mycomms = None

        #@property
        def capacity(self, buffername="defbuffer1", buffer_capacity=None):
            """
            This attribute gets or sets the number of readings a buffer can store.
            Parameters:
                buffername (str) = The name of the reading buffer, which may be a default buffer (defbuffer1 or \
                defbuffer2) or a user-defined buffer

                buffer_capacity (int) = The maximum number of readings the buffer can store; set to 0 to maximize \
                the buffer size
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
                self.mycoms = None

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

    class MeasureConfiguration:
        def __init__(self):
            self.range = None
            self.mycomms = None
            self.configlist = self.ConfigList()
            self.filter = self.Filter()
            self.limit = self.Limit()
            self.math = self.Math()
            self.rel = self.Rel()

        def update_comms(self):
            """This function is used to ensure lower level consumer classes tied to the driver are updated to promote instrument communications."""
            self.configlist.mycoms = self.mycomms
            self.filter.mycoms = self.mycomms
            self.limit.mycoms = self.mycomms
            self.math.mycoms = self.mycomms
            self.rel.mycoms = self.mycomms

        @property
        def function(self):
            """This attribute contains the measure function, which can be voltage or current."""
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
            """This attribute contains the measure function, which can be voltage or current."""
            if func == smuconst.FUNC_DC_VOLTAGE:
                self.mycomms.write("smu.measure.func = smu.FUNC_DC_VOLTAGE")
                # print()
            else:
                self.mycomms.write("smu.measure.func = smu.FUNC_DC_CURRENT")
                # print()

        class ConfigList:
            def __init__(self):
                self.mycoms = None

        class Filter:
            def __init__(self):
                self.mycoms = None

        class Limit:
            def __init__(self):
                self.mycoms = None

        class Math:
            def __init__(self):
                self.mycoms = None

        class Rel:
            def __init__(self):
                self.mycoms = None

    class TriggerConfiguration:
        def __init__(self):
            self.temp = None
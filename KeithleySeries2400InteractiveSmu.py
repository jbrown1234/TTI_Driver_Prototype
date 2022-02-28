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
import KeithleySeries2400InteractiveSmu_MeasureConfiguration as measure_config
import KeithleySeries2400InteractiveSmu_SourceConfiguration as source_config
import KeithleySeries2400InteractiveSmu_TriggerConfiguration as trigger_config
import KeithleySeries2400InteractiveSmu_DisplayConfiguration as display_config
class KeithleySeries2400InteractiveSmu():
    def __init__(self):
        self.echocommand = 0
        self.node = 1
        self.resource_mgr = None
        self.resource_id = ""
        # self.instrument_object = None
        self.instrumentcomms = comms.Communications()
        # self.buffer = self.Buffer()
        self.display = display_config.DisplayConfiguration()
        self.source = source_config.SourceConfiguration()
        self.measure = measure_config.MeasureConfiguration()
        self.trigger = trigger_config.TriggerConfiguration()

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
            #self.buffer.mycomms = self.instrumentcomms
            self.display.mycomms = self.instrumentcomms
            self.source.mycomms = self.instrumentcomms
            self.measure.mycomms = self.instrumentcomms
            self.trigger.mycomms = self.instrumentcomms
            self.source.update_comms()
            self.measure.update_comms()
            self.trigger.update_comms()
            self.display.update_comms()

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

    def waitcomplete(self):
        """
        This function waits for all previously started overlapped commands to complete.

        :return: None
        """
        self.instrumentcomms.write("waitcomplete()")

    def get_buffer_value(self, buffer_name, index, readings=False, relativetimestamps=False, formattedreadings=False,
                         fractionalseconds=False, extravalues=False, extravalueunits=False, extraformattedvalues=False,
                         dates=False, seconds=False, sourceformattedvalues=False, sourcestatuses=False,
                         sourceunits=False, statuses=False, times=False, timestamps=False, units=False):
        write_string = "print("
        #add_comma = False
        if readings:
            write_string += f"{buffer_name}.readings[{index}]"
            #add_comma = True
        elif relativetimestamps:
            #if add_comma:
            #write_string += ","
            write_string += f"{buffer_name}.relativetimestamps[{index}]"
            #add_comma = True
        elif formattedreadings:
            #if add_comma:
            #    write_string += ","
            write_string += f"{buffer_name}.fractionalseconds[{index}]"
            #add_comma = True
        elif fractionalseconds:
            #if add_comma:
            #    write_string += ","
            write_string += f"{buffer_name}.fractionalseconds[{index}]"
            #add_comma = True
        elif extravalues:
            #if add_comma:
            #    write_string += ","
            write_string += f"{buffer_name}.extravalues[{index}]"
            #add_comma = True
        elif extravalueunits:
            #if add_comma:
            #    write_string += ","
            write_string += f"{buffer_name}.extravalueunits[{index}]"
            #add_comma = True
        elif extraformattedvalues:
            #if add_comma:
            #    write_string += ","
            write_string += f"{buffer_name}.extraformattedvalues[{index}]"
            #add_comma = True
        elif dates:
            #if add_comma:
            #    write_string += ","
            write_string += f"{buffer_name}.dates[{index}]"
            #add_comma = True
        elif seconds:
            #if add_comma:
            #    write_string += ","
            write_string += f"{buffer_name}.seconds[{index}]"
            #add_comma = True
        elif sourceformattedvalues:
            #if add_comma:
            #    write_string += ","
            write_string += f"{buffer_name}.sourceformattedvalues[{index}]"
            #add_comma = True
        elif sourcestatuses:
           # if add_comma:
           #     write_string += ","
            write_string += f"{buffer_name}.sourcestatuses[{index}]"
            #add_comma = True
        elif sourceunits:
            #if add_comma:
            #    write_string += ","
            write_string += f"{buffer_name}.sourceunits[{index}]"
            #add_comma = True
        elif statuses:
            #if add_comma:
            #    write_string += ","
            write_string += f"{buffer_name}.statuses[{index}]"
            #add_comma = True
        elif times:
            #if add_comma:
            #    write_string += ","
            write_string += f"{buffer_name}.times[{index}]"
            #add_comma = True
        elif timestamps:
            #if add_comma:
            #    write_string += ","
            write_string += f"{buffer_name}.timestamps[{index}]"
            #add_comma = True
        elif units:
            #if add_comma:
            #    write_string += ","
            write_string += f"{buffer_name}.units[{index}]"
        write_string += ")"
        return self.instrumentcomms.query(write_string).rstrip()

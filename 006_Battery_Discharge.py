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
#

# *****************************************************************************
#
# Example Description:
#
#       This example code designed to discharge a battery and create a battery
#       model for use in a Keithley Model 2281S-20-6 Battery Simulator and
#       Precision DC Power Supply.  It will run
#       on any of the following Keithley instruments:
# 	        * Model 2450 SourceMeter
# 	        * Model 2460 SourceMeter
# 	        * Model 2461 SourceMeter
#
#       This code was adapted from the Keithley Applications Engineering TSP
#       script courtesy of Al Ivons.
#
# *****************************************************************************
# import time
import KeithleySeries2400InteractiveSmu as KeiSmu
import KeithleySeries2400InteractiveSmu_Constants as smuconst

smu = KeiSmu.KeithleySeries2400InteractiveSmu()

test_parameters = {
    'terminals': None
}


def configure_system():  # temporarily removed the do_beeps parameter
    """
    description

    parameter: do_beeps
    returns: None
    """
    smu.reset()
    smu.display.change_screen(smuconst.DISPLAY_SCREEN_HOME)

    smu.eventlog.clear()

    selection = input("Enter the terminals you are using: 'F' for FRONT or 'R'\
         for REAR: ")
    if "F" in selection.upper():
        smu.terminals = smuconst.TERMINALS_FRONT
        test_parameters['terminals'] = smuconst.TERMINALS_FRONT
    elif "R" in selection.upper():
        smu.terminals = smuconst.TERMINALS_REAR
        test_parameters['terminals'] = smuconst.TERMINALS_REAR
    else:
        return -1010, "configure_system aborted by user"

    # Configure the source settings
    smu.source.func = smuconst.FUNC_DC_CURRENT
    smu.source.offmode = smuconst.OFFMODE_HIGHZ
    smu.source.readback = smuconst.OFF

    # Amps; zero is default value
    smu.source.level = 0.0
    # Amps; automatically disables source autorange. Was 0.1;
    smu.source.range = 0.001
    # Seconds; automatically disables source autodelay
    smu.source.delay = 0.0

    # Configure measure settings
    smu.measure.function = smuconst.FUNC_DC_VOLTAGE
    smu.measure.sense = smuconst.SENSE_4WIRE

    temp_str = smu.localnode.model()
    if "2450" in temp_str:
        smu.measure.range = 200.0           # volts
        smu.source.vlimit.level = 210.0     # volts
    elif "2460" in temp_str:
        smu.measure.range = 100.0           # volts
        smu.source.vlimit.level = 105.0     # volts
    elif "2461" in temp_str:
        smu.measure.range = 100.0           # volts
        smu.source.vlimit.level = 105       # volts
    elif "2470" in temp_str:
        smu.measure.range = 200.0           # volts
        smu.source.vlimit.level = 210       # volts
    else:
        return -1011, "Unexpected SMU model detected; configure_system aborted"

    smu.measure.autorange = smuconst.ON
    smu.measure.nplc = 5.0

    return 0, ""


smu.initialize("USB0::0x05E6::0x2460::04312353::INSTR")
val, ret_str = configure_system()
print(f"{val}, {ret_str}")

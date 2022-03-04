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

# ********************************************************************************
#
# Example Description:
#
#       This example code designed to discharge a battery and create a battery model for use
#       in a Keithley Model 2281S-20-6 Battery Simulator and Precision DC Power Supply.  It will run
#       on any of the following Keithley instruments:
# 	        * Model 2450 SourceMeter
# 	        * Model 2460 SourceMeter
# 	        * Model 2461 SourceMeter
#
#       This code was adapted from the Keithley Applications Engineering TSP script
#       courtesy of Al Ivons.
#
# ********************************************************************************
import KeithleySeries2400InteractiveSmu as KeiSmu
import KeithleySeries2400InteractiveSmu_Constants as smuconst
import time

smu = KeiSmu.KeithleySeries2400InteractiveSmu()

test_parameters ={
    'terminals': None
}


def configure_system(do_beeps):
    smu.reset()
    smu.display.change_screen(smuconst.DISPLAY_SCREEN_HOME)

    smu.eventlog.clear()

    selection = input("Enter the terminals you are using: 'F' for FRONT or 'R' for REAR: ")
    if "F" in selection.upper():
        smu.terminals = smuconst.TERMINALS_FRONT
        test_parameters['terminals'] = smuconst.TERMINALS_FRONT
    elif "T" in selection.upper():
        smu.terminals = smuconst.TERMINALS_REAR
        test_parameters['terminals'] = smuconst.TERMINALS_REAR

    # Configure the source settings
    smu.source.func = smuconst.FUNC_DC_CURRENT
    smu.source.offmode = smuconst.OFFMODE_HIGHZ
    smu.source.readback = smuconst.OFF

    return

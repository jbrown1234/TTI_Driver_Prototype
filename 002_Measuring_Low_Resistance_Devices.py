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
#       The following sequence of commands makes 100 low-resistance measurements by sourcing
#       current and measuring resistance. In this example, the source current magnitude and limit voltage are
#       set automatically. It uses remote commands to change the front-panel display to show the GRAPH
#       swipe screen. This allows you to view numeric data at the top of the screen and graphic data at the
#       bottom of the screen.
#
# ********************************************************************************
import KeithleySeries2400InteractiveSmu as KeiSmu
import KeithleySeries2400InteractiveSmu_Constants as smuconst

mysmu = KeiSmu.KeithleySeries2400InteractiveSmu()

mysmu.initialize("USB0::0x05E6::0x2460::04312353::INSTR")

#  Reset the instrument to the default settings
mysmu.reset()

#  Configure the Simple Loop trigger model template to make 100 readings.
mysmu.trigger.model.load_simple_loop(100)

# Change the view on the front panel to the GRAPH swipe screen.
mysmu.display.change_screen(smuconst.DISPLAY_SCREEN_GRAPH)

# Set to measure resistance, use 4-wire sense, and offset compensation.
mysmu.measure.function = smuconst.FUNC_RESISTANCE
mysmu.measure.sense = smuconst.SENSE_4WIRE
mysmu.measure.offsetcompensation = smuconst.ON

#  Turn on the output
mysmu.source.output = smuconst.ON

# Initiate trigger model and wait until finished.
mysmu.trigger.model.initiate()
mysmu.waitcomplete()

# Turn off output
mysmu.source.output = smuconst.OFF

# Read the resistance and time values from defbuffer1.

print(mysmu.instrument_id_query())

mysmu.close()

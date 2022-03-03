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
#       The following sequence of commands performs a capacitor leakage measurement by sourcing 20 V and
#       measuring the resulting leakage current. The DurationLoop trigger model template applies the voltage
#       for 30 seconds and makes measurements at 200 ms intervals. After the duration time, the capacitor is
#       discharged at 0 V and the output is turned off
#
# ********************************************************************************
import KeithleySeries2400InteractiveSmu as KeiSmu
import KeithleySeries2400InteractiveSmu_Constants as smuconst
import time

gate_smu = KeiSmu.KeithleySeries2400InteractiveSmu()
drain_smu = KeiSmu.KeithleySeries2400InteractiveSmu()

gate_smu.initialize("USB0::0x05E6::0x2460::04312353::INSTR")
drain_smu.initialize("")

#  Reset the instrument to the default settings
gate_smu.reset()
gate_smu.source.configlist

# Set up the source function.
mysmu.source.func = smuconst.FUNC_DC_VOLTAGE
mysmu.source.ilimit.level = 0.1
mysmu.source.level = 20

# Set up the measure function
mysmu.measure.function = smuconst.FUNC_DC_CURRENT
mysmu.measure.unit = smuconst.UNIT_OHM
mysmu.terminals = smuconst.TERMINALS_REAR
mysmu.measure.autorange = smuconst.ON
mysmu.measure.nplc = 1.0

# Turn on the output and initiate readings.
mysmu.trigger.model.load_simple_loop(10, 0.1)
mysmu.source.output = smuconst.ON
mysmu.trigger.model.initiate()

# Wait until finished.
time.sleep(0.1)
trig_state = mysmu.trigger.model.state
while trig_state is smuconst.TRIGGER_STATE_RUNNING:
    time.sleep(0.1)
    trig_state = mysmu.trigger.model.state

# Turn off the output.
mysmu.source.output = smuconst.OFF

# Read the resistance and time values from defbuffer1.
print("Reading #\tResistance\tTime")
for i in range(1, mysmu.get_buffer_reading_count()+1, 1):
    reading_val = mysmu.get_buffer_value("defbuffer1", i, readings=True)
    reltime_val = mysmu.get_buffer_value("defbuffer1", i, relativetimestamps=True)
    print(f"{i}\t{reltime_val}\t{reading_val}")

mysmu.close()

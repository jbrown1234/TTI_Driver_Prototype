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

import KeithleySeries2400InteractiveSmu as KeiSmu
import KeithleySeries2400InteractiveSmu_Constants as smuconst

mysmu = KeiSmu.KeithleySeries2400InteractiveSmu()

mysmu.initialize("USB0::0x05E6::0x2460::04312353::INSTR")

print(mysmu.instrument_id_query())

# do a reset
mysmu.reset()

# Set up the source function
mysmu.source.func = smuconst.FUNC_DC_VOLTAGE
mysmu.source.ilimit.level = 1.0
mysmu.source.level = 20.0

# Set up measure function.
mysmu.buffer.capacity("defbuffer1", 25)
print(mysmu.buffer.capacity("defbuffer1"))
var = mysmu.buffer.capacity()
mysmu.measure.function = smuconst.FUNC_DC_CURRENT
mysmu.terminals = smuconst.TERMINALS_REAR
mysmu.measure.autorange = smuconst.ON
mysmu.measure.nplc = 1.0

# Turn on the output and initiate readings.

smu.source.output = smu.ON
trigger.model.load("DurationLoop", 60, 0.2)
trigger.model.initiate()

# Wait for the trigger model to complete.
waitcomplete()

mysmu.close()

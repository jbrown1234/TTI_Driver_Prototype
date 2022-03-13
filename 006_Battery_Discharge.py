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
# from numpy import char
# from urllib.parse import MAX_CACHE_SIZE

import KeithleySeries2400InteractiveSmu as KeiSmu
import KeithleySeries2400InteractiveSmu_Constants as smuconst

smu = KeiSmu.KeithleySeries2400InteractiveSmu()

test_parameters = {
    'terminals': None,
    'initial_voc': None,
    'comment': None,
    'discharge_type': None,
    'discharge_current': 0.0,
    'discharge_current_list': {
        'current': [],
        'duration': [],
        'average_current': None,
        'list_duration': None,
    },
    'max_discharge_current': None,
}


def configure_system(do_beeps):  # temporarily removed the do_beeps parameter
    """
    description

    parameter: do_beeps
    returns: None
    """
    smu.reset()
    smu.display.change_screen(smuconst.DISPLAY_SCREEN_HOME)

    smu.eventlog.clear()

    terminals_str = "FRONT"
    selection = input("Enter the terminals you are using: 'F' for FRONT or 'R'\
    for REAR: ")

    if "F" in selection.upper():
        smu.terminals = smuconst.TERMINALS_FRONT
        test_parameters['terminals'] = smuconst.TERMINALS_FRONT
        terminals_str = "FRONT"
    elif "R" in selection.upper():
        smu.terminals = smuconst.TERMINALS_REAR
        test_parameters['terminals'] = smuconst.TERMINALS_REAR
        terminals_str = "REAR"
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
    smu.measure.nplc = 1.0

    character_input = input(f"Make 4-wire connections to your battery at the\
        SMU {terminals_str} and then press OK.")
    if do_beeps:
        smu.beep(0.08, 2400)

    smu.source.output = smuconst.ON

    smu.buffer.clear("defbuffer2")

    # Measure voltage to set range; using defbuffer2 to collect voc values
    # Expected autorange to do this automatically, but different range
    #   boundaries in 2460/61 affect my plans.  Use scrap_reading to set
    #   the range.
    scrap_reading = smu.measure.read("defbuffer2")
    smu.measure.range = scrap_reading
    smu.source.vlimit.level = 1.05 * smu.measure.range

    test_parameters["initial_voc"] = smu.measure.read()

    smu.source.output = smuconst.OFF

    if test_parameters["initial_voc"] <= 0:
        return -1012, "Negative or zero Initial Voc detected; configure_system\
            aborted"

    tempvalue = test_parameters["initial_voc"]
    print(f"Measured battery voltage = {tempvalue} V")
    character_input = input("Type C to continue or Q to quit: ")
    if character_input.upper() is "Q":
        return -1010, "ConfigSystem aborted by user"

    return 0, ""


def configure_test(do_beeps):
    """
    Docstring placeholder
    """
    smu.eventlog.clear()

    maximum_allowed_current = 0

    if "2540" in smu.localnode.model():
        if smu.measure.range == 200:  # volts
            maximum_allowed_current = 0.105  # amps
        else:
            maximum_allowed_current = 1.05  # amps
    elif "2460" in smu.localnode.model():
        if smu.measure.range == 100:    # volts
            maximum_allowed_current = 1.05  # amps
        elif smu.measure.range == 20:   # volts
            maximum_allowed_current = 4.2  # amps
        elif smu.measure.range == 10:   # volts
            maximum_allowed_current = 5.25  # amps
        else:
            maximum_allowed_current = 7.35  # amps
    elif "2461" in smu.localnode.model():
        if smu.measure.range == 100:    # volts
            maximum_allowed_current = 1.05  # amps
        elif smu.measure.range == 20:   # volts
            maximum_allowed_current = 4.2   # amps
        elif smu.measure.range == 10:   # volts
            maximum_allowed_current = 5.25  # amps
        else:
            maximum_allowed_current = 7.35  # amps
    else:
        return -1021, "Unexpected SMU model detected; ConfigTest aborted"

    if do_beeps:
        smu.beep(0.08, 2400)
    comment = input("Enter Comment (64 char max): ")
    if comment == "" or comment is None:
        comment = "NO COMMENT"
    test_parameters["comment"] = comment

    if do_beeps:
        smu.beep(0.08, 2400)

    discharge_type = input("For constant current discharge enter \"CURR\", \
        for pulsed or list current enter \"LIST\": ")

    if "CURR" in discharge_type.upper():
        test_parameters["discharge_type"] = "CONSTANT"

        dialog_text = f"Discharge Curr (1E-6 to {maximum_allowed_current})"
        test_curr = float(input(f"{dialog_text}: "))
        test_parameters["discharge_current"] = test_curr
        test_parameters["max_discharge_current"] = \
            test_parameters["discharge_current"]
    elif "LIST" in discharge_type.upper():
        test_parameters["discharge_type"] = "LIST"

        # create the list type for holding the user-supplied list points
        test_parameters["discharge_current_list"]["current"].clear()
        test_parameters["discharge_current_list"]["duration"].clear()

        # set the type to None since it will not be used
        test_parameters["discharge_current"] = None
        number_of_list_points = int(input("Enter the number of points in list \
            (2 to 10): "))
        if number_of_list_points is None or number_of_list_points < 2 or \
           number_of_list_points > 10:
            return -1020, "configure_test aborted by user"

        average_current = 0.0
        list_duration = 0.0

        for i in range(number_of_list_points):
            user_input_string = input(f"Discharge current #{i+1} (from 0 \
            to {maximum_allowed_current}): ")

            if user_input_string is None or user_input_string == "":
                return -1020, "ConfigTest aborted by user"
            test_parameters["discharge_current_list"]["current"].append(float(
                user_input_string))

            user_input_string = input(f"Duration for current#{i+1} (500 us \
            miniumum): ")

            if user_input_string is None or user_input_string == "":
                return -1020, "ConfigTest aborted by user"
            test_parameters["discharge_current_list"]["duration"].append(float(
                user_input_string))

            average_current = average_current + test_parameters[
                "discharge_current_list"]["current"][i] * test_parameters[
                    "discharge_current_list"]["duration"][i]
            list_duration = list_duration + test_parameters[
                "discharge_current_list"]["duration"][i]

        average_current = average_current/list_duration
        test_parameters["discharge_current_list"]["average_current"] = \
            average_current
        test_parameters["discharge_current_list"]["list_duration"] = \
            list_duration

        # Iterate over the current entries in the list to determine the max
        max_specified_current = test_parameters["discharge_current_list"][
            "current"][0]
        for i in range(1, number_of_list_points):
            if test_parameters["discharge_current_list"]["current"][i] > \
               max_specified_current:
                max_specified_current = test_parameters[
                    "discharge_current_list"]["current"][i]

    return 0, "We cool"


smu.initialize("USB0::0x05E6::0x2460::04312353::INSTR")
val, ret_str = configure_system(True)
val, ret_str = configure_test(True)
print(f"{val}, {ret_str}")

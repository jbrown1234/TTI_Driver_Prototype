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


class TriggerConfiguration:
    """
    Placeholder docstring description
    """
    def __init__(self):
        self._mycomms = None
        self.model = self.Model()

    def update_comms(self):
        """
        This function is used to ensure lower level consumer classes tied to\
            the driver are updated to promote instrument communications.

        :return:
        """
        self.model._mycomms = self._mycomms
        self.model._update_comms()
        # self.configlist.mycomms = self.mycomms
        # self.filter.mycomms = self.mycomms

    class Model:
        """
        Placeholder docstring description
        """
        def __init__(self):
            self._mycomms = None
            self.setblock = self.Setblock()

        def _update_comms(self):
            """
            Placeholder
            """
            self.setblock._mycomms = self._mycomms
            self.setblock._update_comms()

        def initiate(self):
            """
            This function starts the trigger model.

            :return: None
            """
            self._mycomms.write("trigger.model.initiate()")

        def load_duration_loop(self, duration, delay=None, buffer_name=None):
            """
            This function loads a trigger-model template configuration that\
                makes continuous measurements for a specified amount of time.

            :param duration: The amount of time for which to make measurements\
                (167 ns to 100 ks)
            :param delay: The delay time before each measurement (167 ns to 10\
                ks); default is 0 for no delay
            :param buffer_name: The name of the reading buffer, which may be a\
                default buffer (defbuffer1 or defbuffer2) or a user-defined\
                    buffer; defaults to defbuffer1
            :return: None
            """
            if buffer_name is not None:
                self._mycomms.write(f"trigger.model.load(\"DurationLoop\",\
                    {duration}, {delay}, {buffer_name})")
            elif delay is not None:
                self._mycomms.write(f"trigger.model.load(\"DurationLoop\",\
                    {duration}, {delay})")
            else:
                self._mycomms.write(f"trigger.model.load(\"DurationLoop\",\
                    {duration})")

            print(0)

        def load_simple_loop(self, count, delay=None, buffer_name=None):
            """
            This function loads a trigger-model template configuration that\
                makes a specific number of measurements.

            :param count: The number of measurements the instrument will make.
            :param delay: The delay time before each measurement (167 ns to 10\
                ks); default is 0 for no delay.
            :param buffer_name: Indicates the reading buffer to use; the\
                default buffers (defbuffer1 or
            defbuffer2) or the name of a user-defined buffer; if no buffer is\
                specified, defbuffer1 is used.
            :return: None
            """
            if buffer_name is not None:
                self._mycomms.write(f"trigger.model.load(\"SimpleLoop\",\
                    {count}, {delay}, {buffer_name})")
            elif delay is not None:
                self._mycomms.write(f"trigger.model.load(\"SimpleLoop\",\
                    {count}, {delay})")
            else:
                self._mycomms.write(f"trigger.model.load(\"SimpleLoop\",\
                    {count})")

        class Setblock():
            """
            Placeholder docstring description
            """
            def __init__(self):
                self._mycomms = None
                self.branch = self.Branch()
                self.configure = self.Config()
                self.delay = self.Delay()

            def _update_comms(self):
                self.branch._mycomms = self._mycomms
                self.configure._mycomms = self._mycomms
                self.delay._mycomms = self._mycomms

                self.branch._update_comms()

            class Branch():
                """
                Placeholder
                """
                def __init__(self):
                    self._mycomms = None
                    self.limit = self.Limit()

                def _update_comms(self):
                    self.limit._mycomms = self._mycomms

                def always(self, block_number, branch_to_block):
                    """
                    This function defines a trigger-model block that always\
                        goes to a specific block.

                    :param block_number: The sequence of the block in the\
                        trigger model.
                    :param branch_to_block: The block number to execute when\
                        the trigger model reaches the Branch Always block.
                    :return: None
                    """
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        , trigger.BLOCK_BRANCH_ALWAYS, {branch_to_block})")

                def counter(self, block_number, target_count, branch_to_block):
                    """
                    This function defines a trigger-model block that branches\
                        to a specified block a specified number of times.

                    :param block_number: The sequence of the block in the\
                        trigger model.
                    :param target_count: The number of times to repeat.
                    :param branch_to_block: The block number to execute when\
                        the trigger model reaches the Branch Always block.
                    :return: None
                    """
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        , trigger.BLOCK_BRANCH_COUNTER, {target_count},\
                            {branch_to_block})")

                def delta(self, block_number, target_difference,
                          branch_to_block, measure_block=None):
                    """
                    This function defines a trigger-model block that branches\
                        to a specified block a specified number of times.

                    :param block_number: The sequence of the block in the\
                        trigger model.
                    :param target_difference: The value against which the\
                        block compares the difference between the\
                            measurements.
                    :param branch_to_block: The block number to execute when\
                        the trigger model reaches the Branch Always block.
                    :param measure_block: The block number of the measure/\
                        digitize block that makes the measurements to be\
                            compared; if this is 0 or undefined, the trigger\
                                model uses the previous measure/digitize block.
                    :return: None
                    """
                    if measure_block is None:
                        self._mycomms.write(f"trigger.model.setblock(\
                            {block_number}, trigger.BLOCK_BRANCH_DELTA,\
                                {target_difference}, {branch_to_block})")
                    else:
                        self._mycomms.write(f"trigger.model.setblock(\
                            {block_number}, trigger.BLOCK_BRANCH_DELTA,\
                                {target_difference}, {branch_to_block},\
                                    {measure_block})")

                class Limit():
                    """
                    Placeholder
                    """
                    def __init__(self):
                        self._mycomms = None

                    def constant(self, block_number, limit_type, limit_a,
                                 limit_b, branch_to_block, measure_block=None):
                        """
                        This function defines a trigger-model block that goes\
                            to a specified block if a measurement meets preset\
                                criteria.

                        :param block_number: The sequence of the block in the\
                            trigger model.
                        :param limit_type: The type of limit, which can be one\
                            of the following types: TRIGGER_LIMIT_ABOVE (0),\
                            TRIGGER_LIMIT_BELOW (1), TRIGGER_LIMIT_INSIDE (2),\
                            TRIGGER_LIMIT_OUTSIDE (3)
                        :param limit_a: The lower limit that the measurement\
                            is tested against; if limit_type is set to\
                            TRIGGER_LIMIT_ABOVE, this value is ignored; if\
                            set to TRIGGER_LIMIT_BELOW, the measurement must\
                            be below this value; if set to\
                            TRIGGER_LIMIT_INSIDE, the low limit that the\
                            measurement is compared against; if set to\
                            TRIGGER_LIMIT_OUTSIDE, the low limit that the\
                            measurement is compared against
                        :param limit_b: The upper limit that the measurement\
                            is tested against; if limit_type is set to\
                            TRIGGER_LIMIT_ABOVE, the measurement must be\
                            below; if set to TRIGGER_LIMIT_BELOW, this value\
                            is ignored;; if set to TRIGGER_LIMIT_INSIDE, the\
                            high limit that the measurement is compared\
                            against; if set to TRIGGER_LIMIT_OUTSIDE, the high\
                            limit that the measurement is compared against
                        :param branch_to_block: The block number to execute\
                            when the trigger model reaches the Branch Always \
                            block.
                        :param measure_block: The block number of the measure/\
                            digitize block that makes the measurements to be\
                            compared; if this is 0 or undefined, the trigger\
                            model uses the previous measure/digitize block.
                        :return: None
                        """
                        limit_type_str = ""
                        if limit_type is _smuconst.TRIGGER_LIMIT_ABOVE:
                            limit_type_str = "trigger.LIMIT_ABOVE"
                        elif limit_type is _smuconst.TRIGGER_LIMIT_BELOW:
                            limit_type_str = "trigger.LIMIT_BELOW"
                        elif limit_type is _smuconst.TRIGGER_LIMIT_INSIDE:
                            limit_type_str = "trigger.LIMIT_INSIDE"
                        elif limit_type is _smuconst.TRIGGER_LIMIT_OUTSIDE:
                            limit_type_str = "trigger.LIMIT_OUTSIDE"

                        if measure_block is None:
                            self._mycomms.write(f"trigger.model.setblock(\
                            {block_number},trigger.BLOCK_BRANCH_LIMIT_CONSTANT,\
                            {limit_type_str},{limit_a},{limit_b},\
                            {branch_to_block})")
                        else:
                            self._mycomms.write(f"trigger.model.setblock(\
                            {block_number},trigger.BLOCK_BRANCH_LIMIT_CONSTANT,\
                            {limit_type_str},{limit_a},{limit_b},\
                            {branch_to_block},{measure_block})")

                    def dynamic(self, block_number, limit_type, limit_number,
                                branch_to_block, measure_block=None):
                        """
                        This function defines a trigger-model block that goes\
                            to a specified block if a measurement meets preset\
                                criteria.

                        :param block_number: The sequence of the block in the\
                            trigger model.
                        :param limit_type: The type of limit, which can be one\
                            of the following types: TRIGGER_LIMIT_ABOVE (0),\
                            TRIGGER_LIMIT_BELOW (1), TRIGGER_LIMIT_INSIDE (2),\
                            TRIGGER_LIMIT_OUTSIDE (3)
                        :param limit_number: The limit number (1 or 2).
                        :param branch_to_block: The block number to execute\
                            when the trigger model reaches the Branch Always \
                            block.
                        :param measure_block: The block number of the measure/\
                            digitize block that makes the measurements to be\
                            compared; if this is 0 or undefined, the trigger\
                            model uses the previous measure/digitize block.
                        :return: None
                        """
                        limit_type_str = ""
                        if limit_type is _smuconst.TRIGGER_LIMIT_ABOVE:
                            limit_type_str = "trigger.LIMIT_ABOVE"
                        elif limit_type is _smuconst.TRIGGER_LIMIT_BELOW:
                            limit_type_str = "trigger.LIMIT_BELOW"
                        elif limit_type is _smuconst.TRIGGER_LIMIT_INSIDE:
                            limit_type_str = "trigger.LIMIT_INSIDE"
                        elif limit_type is _smuconst.TRIGGER_LIMIT_OUTSIDE:
                            limit_type_str = "trigger.LIMIT_OUTSIDE"

                        if measure_block is None:
                            self._mycomms.write(f"trigger.model.setblock(\
                            {block_number},\
                            trigger.BLOCK_BRANCH_LIMIT_DYNAMIC,\
                            {limit_type_str},{limit_number},{branch_to_block},\
                            {measure_block})")
                        else:
                            self._mycomms.write(f"trigger.model.setblock(\
                            {block_number},\
                            trigger.BLOCK_BRANCH_LIMIT_DYNAMIC,\
                            {limit_type_str},{limit_number},{branch_to_block},\
                            {measure_block})")

                def on_event(self, block_number, event, branch_to_block,
                             n=None):
                    """
                    This function branches to a specified block when a\
                        specified trigger event occurs.

                    :param block_number: The sequence of the block in the\
                        trigger model.
                    :param event: The event that must occur before the\
                        trigger model branches the specified block. Options\
                        include TRIGGER_EVENT_BLENDERn, TRIGGER_EVENT_COMMAND,\
                        TRIGGER_EVENT_DIGIOn, TRIGGER_EVENT_DISPLAY,\
                        TRIGGER_EVENT_LANn, TRIGGER_EVENT_NONE,\
                        TRIGGER_EVENT_NOTIFYn, TRIGGER_EVENT_SOURCE_LIMIT,\
                        TRIGGER_EVENT_TIMERn, TRIGGER_EVENT_TSPLINKn.
                    :param branch_to_block: The block number to execute when\
                        the trigger model reaches the Branch Always block.
                    :param n: (int) The number of either the BLENDER,\
                        DIGIO, LAN, NOTIFY, TIMER, or TSPLINK event.
                    :return: None
                    """
                    if event == _smuconst.TRIGGER_EVENT_BLENDER:
                        event_str = f"trigger.EVENT_BLENDER{n}"
                    elif event == _smuconst.TRIGGER_EVENT_COMMAND:
                        event_str = "trigger.EVENT_COMMAND"
                    elif event == _smuconst.TRIGGER_EVENT_DIGIO:
                        event_str = f"trigger.EVENT_DIGIO{n}"
                    elif event == _smuconst.TRIGGER_EVENT_DISPLAY:
                        event_str = "trigger.EVENT_DISPLAY"
                    elif event == _smuconst.TRIGGER_EVENT_LAN:
                        event_str = f"trigger.EVENT_LAN{n}"
                    elif event == _smuconst.TRIGGER_EVENT_NONE:
                        event_str = "trigger.EVENT_NONE"
                    elif event == _smuconst.TRIGGER_EVENT_NOTIFY:
                        event_str = f"trigger.EVENT_NOTIFY{n}"
                    elif event == _smuconst.TRIGGER_EVENT_SOURCE_LIMIT:
                        event_str = "trigger.EVENT_SOURCE_LIMIT"
                    elif event == _smuconst.TRIGGER_EVENT_TIMER:
                        event_str = f"trigger.EVENT_TIMER{n}"
                    elif event == _smuconst.TRIGGER_EVENT_TSPLINK:
                        event_str = f"trigger.EVENT_TSPLINK{n}"
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        ,trigger.BLOCK_BRANCH_ON_EVENT,{event_str},\
                            {branch_to_block})")

                def once(self, block_number, branch_to_block):
                    """
                    This function causes the trigger model to branch to a\
                    specified building block the first time it is encountered\
                    in the trigger model.

                    :param block_number: The sequence of the block in the\
                        trigger model.
                    :param branch_to_block: The block number to execute when\
                        the trigger model reaches the Branch Always block.
                    :return: None
                    """
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        ,trigger.BLOCK_BRANCH_ONCE,{branch_to_block})")

                def once_excluded(self, block_number, branch_to_block):
                    """
                    This function defines a trigger-model block that causes\
                        the trigger model to go to a specified building block\
                            every time the trigger model encounters it, except\
                                for the first time.

                    :param block_number: The sequence of the block in the\
                        trigger model.
                    :param branch_to_block: The block number to execute when\
                        the trigger model reaches the Branch Always block.
                    :return: None
                    """
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        ,trigger.BLOCK_BRANCH_ONCE_EXCLUDED,{branch_to_block})\
                            ")

            def buffer_clear(self, block_number, buffer_name=None):
                """
                This function defines a trigger-model block that clears the\
                    reading buffer.

                :param block_number: The sequence of the block in the\
                    trigger model.
                :param branch_to_block: The block number to execute when\
                    the trigger model reaches the Branch Always block.
                :return: None
                """
                if buffer_name is None:
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        ,trigger.BLOCK_BUFFER_CLEAR)")
                else:
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        ,trigger.BLOCK_BUFFER_CLEAR, {buffer_name})")

            class Config():
                """
                Placeholder
                """
                def __init__(self):
                    self._mycomms = None

                def next(self, block_number, configuration_list,
                         optional_configuration_list=None):
                    """
                    This function recalls the settings at the next index of a\
                        source or measure configuration list, or both a source\
                            and measure configuration list.

                    :param block_number: The sequence of the block in the\
                        trigger model.
                    :param configuration_list: A string that defines the\
                        source or measure configuration list to recall.
                    :param optional_configuration_list: The name of the second\
                        configuration list to recall the index from; must be\
                            the opposite type of list than the first; for\
                                example, if the first configuration list is a\
                                    measure list, the second configuration\
                                        list must be a source list.
                    :return: None
                    """
                    if optional_configuration_list is None:
                        self._mycomms.write(f"trigger.model.setblock({block_number}\
                            ,trigger.BLOCK_CONFIG_NEXT, \"\
                                {configuration_list}\")")
                    else:
                        self._mycomms.write(f"trigger.model.setblock({block_number}\
                            ,trigger.BLOCK_CONFIG_NEXT, \"\
                                {configuration_list}\",\"\
                                    {optional_configuration_list}\")")

                def previous(self, block_number, configuration_list,
                             optional_configuration_list=None):
                    """
                    This function defines a trigger-model block that recalls\
                    the settings stored at the previous index in a source or\
                    measure configuration list, or both a source and measure\
                    configuration list.

                    :param block_number: The sequence of the block in the\
                        trigger model.
                    :param configuration_list: A string that defines the\
                        source or measure configuration list to recall.
                    :param optional_configuration_list: The name of the second\
                        configuration list to recall the index from; must be\
                            the opposite type of list than the first; for\
                                example, if the first configuration list is a\
                                    measure list, the second configuration\
                                        list must be a source list.
                    :return: None
                    """
                    if optional_configuration_list is None:
                        self._mycomms.write(f"trigger.model.setblock({block_number}\
                            ,trigger.BLOCK_CONFIG_PREV, \"\
                                {configuration_list}\")")
                    else:
                        self._mycomms.write(f"trigger.model.setblock({block_number}\
                            ,trigger.BLOCK_CONFIG_PREV, \"\
                                {configuration_list}\",\"\
                                    {optional_configuration_list}\")")

                def recall(self, block_number, configuration_list,
                           cl_index=None, optional_configuration_list=None,
                           opt_cl_index=None):
                    """
                    This function recalls the system settings that are stored\
                    in a source or measure configuration list, or both a\
                    source and measure configuration list.

                    :param block_number: The sequence of the block in the\
                        trigger model.
                    :param configuration_list: A string that defines the\
                        source or measure configuration list to recall.
                    :param cl_index: The index in the configuration list to\
                        recall; default is 1
                    :param optional_configuration_list: The name of the second\
                        configuration list to recall the index from; must be\
                            the opposite type of list than the first; for\
                                example, if the first configuration list is a\
                                    measure list, the second configuration\
                                        list must be a source list.
                    :param opt_cl_index: The index in the configuration list\
                        to recall; default is 1
                    :return: None
                    """
                    if optional_configuration_list is None:
                        if cl_index is None:
                            self._mycomms.write(f"trigger.model.setblock({block_number}\
                                ,trigger.BLOCK_CONFIG_RECALL,\
                                    \"{configuration_list}\")")
                        else:
                            self._mycomms.write(f"trigger.model.setblock({block_number}\
                                ,trigger.BLOCK_CONFIG_RECALL,\
                                    \"{configuration_list}\",{cl_index})")
                    else:
                        if opt_cl_index is None:
                            self._mycomms.write(f"trigger.model.setblock({block_number}\
                                ,trigger.BLOCK_CONFIG_RECALL,\
                                    \"{configuration_list}\",{cl_index},\
                                        \"{optional_configuration_list}\")")
                        else:
                            self._mycomms.write(f"trigger.model.setblock({block_number}\
                                ,trigger.BLOCK_CONFIG_RECALL,\
                                    \"{configuration_list}\",{cl_index},\
                                        \"{optional_configuration_list}\",\
                                        {opt_cl_index})")

            class Delay():
                """
                Placeholder
                """
                def __init__(self):
                    self._mycomms = None

                def constant(self, block_number, delay_time):
                    """
                    This function adds a constant delay to the execution\
                    of a trigger model.

                    :param block_number: The sequence of the block in the\
                        trigger model.
                    :param delay_time: The amount of time to delay in\
                        seconds (167 ns to 10 ks, or 0 for no delay).
                    :return: None
                    """
                    self._mycomms.write(f"trigger.model.setblock(\
                        {block_number},trigger.BLOCK_DELAY_CONSTANT,\
                            {delay_time})")

                def dynamic(self, block_number, user_delay, n=None):
                    """
                    This function adds a user delay to the execution of\
                    the trigger model.

                    :param block_number: The sequence of the block in the\
                        trigger model.
                    :param user_delay: The number of the user delay:\
                        TRIGGER_USER_DELAY_Mn, where n is the number of\
                        the user delay (1 to 5) set by\
                        smu.measure.userdelay[n] or TRIGGER_USER_DELAY_Sn,\
                         where n is the number of the user delay (1 to 5)\
                        set by smu.source.userdelay[n]
                    :return: None
                    """
                    if user_delay is _smuconst.TRIGGER_USER_DELAY_M:
                        self._mycomms.write(f"trigger.model.setblock({block_number}\
                            ,trigger.BLOCK_DELAY_DYNAMIC,\
                                trigger.USER_DELAY_M{n})")
                    elif user_delay is _smuconst.TRIGGER_USER_DELAY_S:
                        self._mycomms.write(f"trigger.model.setblock({block_number}\
                            ,trigger.BLOCK_DELAY_DYNAMIC,\
                                trigger.USER_DELAY_S{n})")

            def digital_io(self, block_number, bit_pattern, bit_mask=None):
                """
                This function adds a user delay to the execution of\
                the trigger model.

                :param block_number: The sequence of the block in the\
                    trigger model.
                :param bit_pattern: (int) Sets the value that specifies the\
                    output line bit pattern (0 to 63)
                :param bit_mask: (int) Specifies the bit mask; if omitted,\
                    all lines are driven low (0 to 63)
                :return: None
                """
                if bit_mask is None:
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        ,trigger.BLOCK_DIGITAL_IO,{bit_pattern})")
                else:
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        ,trigger.BLOCK_DIGITAL_IO,{bit_pattern},\
                            {bit_mask})")

            def digitize(self, block_number, buffer_name=None, count=None):
                """
                This function defines a trigger block that makes or digitizes\
                    a measurement.

                :param block_number: The sequence of the block in the\
                    trigger model.
                :param buffer_name: The name of the buffer, which must be an\
                    existing buffer; if no buffer is defined, defbuffer1 is\
                        used.
                :param count: (int) The number of measure or digitize readings\
                    to make before moving to the next block in the trigger\
                    model. Options are: a specific value, infinite (run\
                    continuously until stopped) - TRIGGER_COUNT_INFINITE, stop\
                    infinite to stop the block - TRIGGER_COUNT_STOP, use most\
                    recent count value - TRIGGER_COUNT_AUTO.
                :return: None
                """
                if buffer_name is None:
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        ,trigger.BLOCK_MEASURE_DIGITIZE)")
                else:
                    if count is None:
                        self._mycomms.write(f"trigger.model.setblock({block_number}\
                            ,trigger.BLOCK_MEASURE_DIGITIZE,{buffer_name})")
                    else:
                        if count is _smuconst.TRIGGER_COUNT_INFINITE:
                            self._mycomms.write(f"trigger.model.setblock({block_number}\
                                ,trigger.BLOCK_MEASURE_DIGITIZE,{buffer_name},\
                                    trigger.COUNT_INFINITE)")
                        elif count is _smuconst.TRIGGER_COUNT_STOP:
                            self._mycomms.write(f"trigger.model.setblock({block_number}\
                                ,trigger.BLOCK_MEASURE_DIGITIZE,{buffer_name},\
                                    trigger.COUNT_STOP)")
                        elif count is _smuconst.TRIGGER_COUNT_AUTO:
                            self._mycomms.write(f"trigger.model.setblock({block_number}\
                                ,trigger.BLOCK_MEASURE_DIGITIZE,{buffer_name},\
                                    trigger.COUNT_AUTO)")
                        else:
                            self._mycomms.write(f"trigger.model.setblock({block_number}\
                                ,trigger.BLOCK_MEASURE_DIGITIZE,{buffer_name},\
                                    {count})")

            def log_event(self, block_number, event_number, n=1, message=None):
                """
                This function allows you to log an event in the event log when\
                    the trigger model is running.

                :param block_number: (int) The sequence of the block in the\
                    trigger model.
                :param event_number: The event number can be:
                    TRIGGER_LOG_INFOn, TRIGGER_LOG_WARNn, TRIGGER_LOG_ERRORn,\
                    where n is 1 to 4. You can define up to four of each type\
                    You can also set TRIGGER_LOG_WARN_ABORT, which aborts the\
                    trigger model immediately and posts a warning event log\
                    message.
                :param n: (int) A number 1 to 4 which specifies the\
                    event_number type selection.
                :param message: A string up to 31 characters.
                :return: None
                """
                if event_number is _smuconst.TRIGGER_LOG_ERROR:
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        ,trigger.BLOCK_LOG_EVENT, trigger.LOG_ERROR{n},\
                        \"{message}\")")
                elif event_number is _smuconst.TRIGGER_LOG_INFO:
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        ,trigger.BLOCK_LOG_EVENT, trigger.LOG_INFO{n},\
                        \"{message}\")")
                elif event_number is _smuconst.TRIGGER_LOG_WARN:
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        ,trigger.BLOCK_LOG_EVENT, trigger.LOG_WARN{n},\
                        \"{message}\")")
                elif event_number is _smuconst.TRIGGER_LOG_WARN_ABORT:
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        ,trigger.BLOCK_LOG_EVENT, trigger.LOG_WARN_ABORT,\
                        \"{message}\")")

            def measure(self, block_number, buffer_name=None, count=None):
                """
                This function defines a trigger block that makes or digitizes\
                    a measurement.

                :param block_number: (int) The sequence of the block in the\
                    trigger model.
                :param buffer_name: The name of the buffer, which must be an\
                    existing buffer; if no buffer is defined, defbuffer1 is\
                        used.
                :param count: (int) The number of measure or digitize readings\
                    to make before moving to the next block in the trigger\
                    model. Options are: a specific value, infinite (run\
                    continuously until stopped) - TRIGGER_COUNT_INFINITE, stop\
                    infinite to stop the block - TRIGGER_COUNT_STOP, use most\
                    recent count value - TRIGGER_COUNT_AUTO.
                :return: None
                """
                if buffer_name is None:
                    self._mycomms.write(f"trigger.model.setblock({block_number}\
                        ,trigger.BLOCK_MEASURE_DIGITIZE)")
                else:
                    if count is None:
                        self._mycomms.write(f"trigger.model.setblock({block_number}\
                            ,trigger.BLOCK_MEASURE_DIGITIZE,{buffer_name})")
                    else:
                        if count is _smuconst.TRIGGER_COUNT_INFINITE:
                            self._mycomms.write(f"trigger.model.setblock({block_number}\
                                ,trigger.BLOCK_MEASURE_DIGITIZE,{buffer_name},\
                                    trigger.COUNT_INFINITE)")
                        elif count is _smuconst.TRIGGER_COUNT_STOP:
                            self._mycomms.write(f"trigger.model.setblock({block_number}\
                                ,trigger.BLOCK_MEASURE_DIGITIZE,{buffer_name},\
                                    trigger.COUNT_STOP)")
                        elif count is _smuconst.TRIGGER_COUNT_AUTO:
                            self._mycomms.write(f"trigger.model.setblock({block_number}\
                                ,trigger.BLOCK_MEASURE_DIGITIZE,{buffer_name},\
                                    trigger.COUNT_AUTO)")
                        else:
                            self._mycomms.write(f"trigger.model.setblock({block_number}\
                                ,trigger.BLOCK_MEASURE_DIGITIZE,{buffer_name},\
                                    {count})")

            def nop(self, block_number):
                """
                This function creates a placeholder that performs no action\
                in the trigger model; available only using remote commands.

                :param block_number: (int) The sequence of the block in the\
                    trigger model.
                :return: None
                """
                self._mycomms.write(f"trigger.model.setblock({block_number},\
                    trigger.BLOCK_NOP)")

            def notify(self, block_number, n):
                """
                This function defines a trigger-model block that generates a\
                trigger event and immediately continues to the next block.

                :param block_number: (int) The sequence of the block in the\
                    trigger model.
                :param n: (int) The identification number of the\
                    notification; 1 to 8.
                :return: None
                """
                self._mycomms.write(f"trigger.model.setblock({block_number},\
                    trigger.BLOCK_NOTIFY, trigger.EVENT_NOTIFY{n})")

            def reset_branch_count(self, block_number, counter_block_number):
                """
                This function creates a block in the trigger model that\
                resets a branch counter to 0.

                :param block_number: (int) The sequence of the block in the\
                    trigger model.
                :param counter_block_number: (int) The block number of the\
                    counter that is to be reset.
                :return: None
                """
                self._mycomms.write(f"trigger.model.setblock({block_number},\
                    trigger.BLOCK_RESET_BRANCH_COUNT, {counter_block_number})")

            def source_output(self, block_number, output_state):
                """
                This function creates a block in the trigger model that\
                resets a branch counter to 0.

                :param block_number: (int) The sequence of the block in the\
                    trigger model.
                :param Output_state: (int) The block number of the\
                    counter that is to be reset.
                :return: None
                """
                if output_state is _smuconst.ON:
                    outstate_str = "smu.ON"
                if output_state is _smuconst.OFF:
                    outstate_str = "smu.OFF"
                self._mycomms.write(f"trigger.model.setblock({block_number},\
                    trigger.BLOCK_SOURCE_OUTPUT, {outstate_str})")

            def wait(self, block_number, event, n=None, clear=None, logic=None,
                     event2=None, n2=None, event3=None, n3=None):
                """
                This function creates a block in the trigger model that\
                resets a branch counter to 0.

                :param block_number: (int) The sequence of the block in the\
                    trigger model.
                :param event: The event that must occur before the trigger\
                    block allows trigger execution to continue.
                :param clear: To clear previously detected trigger events when\
                    entering the wait block use TRIGGER_CLEAR_ENTER. To\
                    immediately act on any previously detected triggers and\
                    not clear them (default) use TRIGGER_CLEAR_NEVER.
                :param n: (int) The number of either the BLENDER,\
                        DIGIO, LAN, NOTIFY, TIMER, or TSPLINK event.
                :pararm logic: If each event must occur before the trigger\
                    model continues use TRIGGER_WAIT_AND. If at least one of\
                    the events must occur before the trigger model continues\
                    use TRIGGER_WAIT_OR
                :param event2: The event that must occur before the trigger\
                    block allows trigger execution to continue.
                :param n2: (int) The number of either the BLENDER,\
                        DIGIO, LAN, NOTIFY, TIMER, or TSPLINK event.
                :param event3: The event that must occur before the trigger\
                    block allows trigger execution to continue.
                :param n3: (int) The number of either the BLENDER,\
                        DIGIO, LAN, NOTIFY, TIMER, or TSPLINK event.
                :return: None
                """
                cmd_str = f"trigger.model.setblock({block_number},\
                    trigger.BLOCK_WAIT, {self._get_trigger_event(event, n)}"

                if (clear is _smuconst.TRIGGER_CLEAR_ENTER) or \
                   (clear is _smuconst.TRIGGER_CLEAR_NEVER):
                    cmd_str += f",{self._get_trigger_clear_string(clear)},\
                        {self._get_trigger_wait_logic_string(logic)}"
                    if event2:
                        cmd_str += f",{self._get_trigger_event(event2, n2)}"
                        if event3:
                            cmd_str += f",\
                                {self._get_trigger_event(event3, n3)}"

                cmd_str += ")"

                self._mycomms.write(cmd_str)

            def _get_trigger_event(self, event, n=None):
                if event is _smuconst.TRIGGER_EVENT_BLENDER:
                    return f"trigger.EVENT_BLENDER{n}"
                elif event is _smuconst.TRIGGER_EVENT_COMMAND:
                    return "trigger.EVENT_COMMAND"
                elif event == _smuconst.TRIGGER_EVENT_DIGIO:
                    return f"trigger.EVENT_DIGIO{n}"
                elif event == _smuconst.TRIGGER_EVENT_DISPLAY:
                    return "trigger.EVENT_DISPLAY"
                elif event == _smuconst.TRIGGER_EVENT_LAN:
                    return f"trigger.EVENT_LAN{n}"
                elif event == _smuconst.TRIGGER_EVENT_NONE:
                    return "trigger.EVENT_NONE"
                elif event == _smuconst.TRIGGER_EVENT_NOTIFY:
                    return f"trigger.EVENT_NOTIFY{n}"
                elif event == _smuconst.TRIGGER_EVENT_SOURCE_LIMIT:
                    return "trigger.EVENT_SOURCE_LIMIT"
                elif event == _smuconst.TRIGGER_EVENT_TIMER:
                    return f"trigger.EVENT_TIMER{n}"
                elif event == _smuconst.TRIGGER_EVENT_TSPLINK:
                    return f"trigger.EVENT_TSPLINK{n}"

            def _get_trigger_clear_string(self, clear_type):
                if clear_type is _smuconst.TRIGGER_CLEAR_ENTER:
                    return "trigger.CLEAR_ENTER"
                if clear_type is _smuconst.TRIGGER_CLEAR_NEVER:
                    return "trigger.CLEAR_NEVER"

            def _get_trigger_wait_logic_string(self, logic):
                if logic is _smuconst.TRIGGER_WAIT_AND:
                    return "trigger.WAIT_AND"
                if logic is _smuconst.TRIGGER_WAIT_OR:
                    return "trigger.WAIT_OR"

        @property
        def state(self):
            """
            This function returns the present state of the trigger model.

            :return: Will return one of the following: ABORTED, ABORTING,\
                BUILDING, EMPTY, FAILED, IDLE, RUNNING
            """
            self._mycomms.write("stat, stat, n = trigger.model.state()")
            status = self._mycomms.query("print(stat)")
            if "ABORTED" in status:
                return _smuconst.TRIGGER_STATE_ABORTED
            elif "ABORTING" in status:
                return _smuconst.TRIGGER_STATE_ABORTING
            elif "BUILDING" in status:
                return _smuconst.TRIGGER_STATE_BUILDING
            elif "EMPTY" in status:
                return _smuconst.TRIGGER_STATE_EMPTY
            elif "FAIL" in status:
                return _smuconst.TRIGGER_STATE_FAILED
            elif "IDLE" in status:
                return _smuconst.TRIGGER_STATE_IDLE
            elif "RUNNING" in status:
                return _smuconst.TRIGGER_STATE_RUNNING

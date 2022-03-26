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

            def _update_comms(self):
                self.branch._mycomms = self._mycomms
                self.configure._mycomms = self._mycomms

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

                def next(self):
                    """
                    Placeholder
                    """
                    print(0)

                def previous(self):
                    """
                    Placeholder
                    """
                    print(0)

                def recall(self):
                    """
                    Placeholder
                    """
                    print(0)

            class Delay():
                """
                Placeholder
                """
                def __init__(self):
                    self._mycomms = None

                def constant(self):
                    """
                    Placeholder
                    """
                    print(0)

                def dynamic(self):
                    """
                    Placeholder
                    """
                    print(0)

            def digital_io(self):
                """
                Placeholder
                """
                print(0)

            def digitize(self):
                """
                Placeholder
                """
                print(0)

            def log_event(self):
                """
                Placeholder
                """
                print(0)

            def measure(self):
                """
                Placeholder
                """
                print(0)

            def nop(self):
                """
                Placeholder
                """
                print(0)

            def notify(self):
                """
                Placeholder
                """
                print(0)

            def reset_branch_count(self):
                """
                Placeholder
                """
                print(0)

            def source_output(self):
                """
                Placeholder
                """
                print(0)

            def wait(self):
                """
                Placeholder
                """
                print(0)

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

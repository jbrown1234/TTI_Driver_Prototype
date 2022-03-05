import KeithleySeries2400InteractiveSmu_Constants as _smuconst


class TriggerConfiguration:
    def __init__(self):
        self._mycomms = None
        self.model = self.Model()

    def update_comms(self):
        """
        This function is used to ensure lower level consumer classes tied to the driver are updated to promote \
        instrument communications.

        :return:
        """
        self.model._mycomms = self._mycomms
        # self.configlist.mycomms = self.mycomms
        # self.filter.mycomms = self.mycomms

    class Model:
        def __init__(self):
            self._mycomms = None

        def initiate(self):
            """
            This function starts the trigger model.

            :return: None
            """
            self._mycomms.write("trigger.model.initiate()")

        def load_duration_loop(self, duration, delay=None, buffer_name=None):
            """
            This function loads a trigger-model template configuration that makes continuous measurements for a
            specified amount of time.

            :param duration: The amount of time for which to make measurements (167 ns to 100 ks)
            :param delay: The delay time before each measurement (167 ns to 10 ks); default is 0 for no delay
            :param buffer_name: The name of the reading buffer, which may be a default buffer (defbuffer1 or defbuffer2) or a user-defined buffer; defaults to defbuffer1
            :return: None
            """
            if buffer_name is not None:
                self._mycomms.write(f"trigger.model.load(\"DurationLoop\", {duration}, {delay}, {buffer_name})")
            elif delay is not None:
                self._mycomms.write(f"trigger.model.load(\"DurationLoop\", {duration}, {delay})")
            else:
                self._mycomms.write(f"trigger.model.load(\"DurationLoop\", {duration})")

            print(0)

        def load_simple_loop(self, count, delay=None, buffer_name=None):
            """
            This function loads a trigger-model template configuration that makes a specific number of measurements.

            :param count: The number of measurements the instrument will make.
            :param delay: The delay time before each measurement (167 ns to 10 ks); default is 0 for no delay.
            :param buffer_name: Indicates the reading buffer to use; the default buffers (defbuffer1 or
            defbuffer2) or the name of a user-defined buffer; if no buffer is specified, defbuffer1 is used.
            :return: None
            """
            if buffer_name is not None:
                self._mycomms.write(f"trigger.model.load(\"SimpleLoop\", {count}, {delay}, {buffer_name})")
            elif delay is not None:
                self._mycomms.write(f"trigger.model.load(\"SimpleLoop\", {count}, {delay})")
            else:
                self._mycomms.write(f"trigger.model.load(\"SimpleLoop\", {count})")

        @property
        def state(self):
            """
            This function returns the present state of the trigger model.

            :return: Will return one of the following: ABORTED, ABORTING, BUILDING, EMPTY, FAILED, IDLE, RUNNING
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

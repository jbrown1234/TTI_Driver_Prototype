import CommunicationsInterface as comms
import KeithleySeries2400InteractiveSmu_Constants as smuconst

class TriggerConfiguration:
    def __init__(self):
        self.mycomms = None
        self.model = self.Model()

    def update_comms(self):
        """
        This function is used to ensure lower level consumer classes tied to the driver are updated to promote \
        instrument communications.

        :return:
        """
        self.model.mycomms = self.mycomms
        # self.configlist.mycomms = self.mycomms
        # self.filter.mycomms = self.mycomms

    class Model:
        def __init__(self):
            self.mycomms = None

        def initiate(self):
            """
            This function starts the trigger model.

            :return: None
            """
            self.mycomms.write("trigger.model.initiate()")

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
                self.mycomms.write(f"trigger.model.load(\"SimpleLoop\", {count}, {delay}, {buffer_name})")
            elif delay is not None:
                self.mycomms.write(f"trigger.model.load(\"SimpleLoop\", {count}, {delay})")
            else:
                self.mycomms.write(f"trigger.model.load(\"SimpleLoop\", {count})")
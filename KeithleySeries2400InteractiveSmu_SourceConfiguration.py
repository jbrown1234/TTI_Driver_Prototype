import CommunicationsInterface as comms
import KeithleySeries2400InteractiveSmu_Constants as smuconst


class SourceConfiguration:
    def __init__(self):
        #self.range = None
        self.mycomms = None
        self.configlist = self.ConfigList()
        self.protect = self.Protect()
        self.ilimit = self.ILimit()
        self.vlimit = self.VLimit()

    def update_comms(self):
        """This function is used to ensure lower level consumer classes tied to the driver are updated to promote \
         instrument communications.
         """
        self.configlist.mycoms = self.mycomms
        self.protect.mycoms = self.mycomms
        self.ilimit.mycomms = self.mycomms
        self.vlimit.mycomms = self.mycomms

    class ConfigList:
        def __init__(self):
            self.mycoms = None

    class Protect:
        def __init__(self):
            self.mycoms = None

    @property
    def func(self):
        """This attribute contains the source function, which can be voltage or current."""
        self.mycomms.write("srcfunc = smu.source.func")
        response = self.mycomms.query("print(srcfunc)").rstrip()
        # retconstval = None
        if "VOLTAGE" in response:
            retconstval = smuconst.FUNC_DC_VOLTAGE
        else:
            retconstval = smuconst.FUNC_DC_CURRENT
        return retconstval

    @func.setter
    def func(self, func):
        """This attribute contains the source function, which can be voltage or current."""
        if func == smuconst.FUNC_DC_VOLTAGE:
            self.mycomms.write("smu.source.func = smu.FUNC_DC_VOLTAGE")
            # print()
        else:
            self.mycomms.write("smu.source.func = smu.FUNC_DC_CURRENT")
            # print()

    @property
    def level(self):
        """This attribute immediately selects a fixed amplitude for the selected source function."""
        self.mycomms.write("srclev = smu.source.level")
        return float(self.mycomms.query("print(srclev)").rstrip())

    @level.setter
    def level(self, value):
        """This attribute immediately selects a fixed amplitude for the selected source function."""
        self.mycomms.write(f"smu.source.level = {value}")

    class ILimit:
        def __init__(self):
            self.mycomms = None

        @property
        def level(self):
            """This attribute selects the source limit for current measurements."""
            self.mycomms.write("ilimitlev = smu.source.ilimit.level")
            return float(self.mycomms.query("print(ilimitlev)").rstrip())

        @level.setter
        def level(self, value):
            """This attribute selects the source limit for current measurements."""
            self.mycomms.write(f"smu.source.ilimit.level = {value}")

        @property
        def tripped(self):
            """This attribute indicates if the source exceeded the limits that were set for the selected measurements."""
            self.mycomms.write("ilimittrip = smu.source.ilimit.tripped")
            return int(self.mycomms.query("print(ilimittrip)").rstrip())

    class VLimit:
        def __init__(self):
            self.mycomms = None

        @property
        def level(self):
            """This attribute selects the source limit for voltage measurements."""
            self.mycomms.write("vlimitlev = smu.source.vlimit.level")
            return float(self.mycomms.query("print(vlimitlev)").rstrip())

        @level.setter
        def level(self, value):
            """This attribute selects the source limit for voltage measurements."""
            self.mycomms.write(f"smu.source.vlimit.level = {value}")

        @property
        def tripped(self):
            """This attribute indicates if the source exceeded the limits that were set for the selected measurements."""
            self.mycomms.write("vlimittrip = smu.source.vlimit.tripped")
            return int(self.mycomms.query("print(vlimittrip)").rstrip())

    @property
    def output(self):
        """
        This attribute enables or disables the source output.

        :return: Either ON (1) or OFF (0).
        """
        self.mycomms.write("source_output = smu.source.output")
        source_output = self.mycomms.query("print(source_output)")
        if "ON" in source_output:
            return smuconst.ON
        elif "OFF" in source_output:
            return smuconst.OFF
        else:
            return smuconst.OFF     # default to the off state

    @output.setter
    def output(self, state):
        """
        This attribute enables or disables the source output.

        :param state: Either ON (1) or OFF (0)
        :return: None
        """
        if state is smuconst.ON:
            self.mycomms.write("smu.source.output=smu.ON")
        else:
            self.mycomms.write("smu.source.output=smu.OFF")

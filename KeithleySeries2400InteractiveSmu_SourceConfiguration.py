import CommunicationsInterface as comms
import KeithleySeries2400InteractiveSmu_Constants as smuconst


class SourceConfiguration:
    def __init__(self):
        #self.range = None
        self._mycomms = None
        self.configlist = self.ConfigList()
        self.protect = self.Protect()
        self.ilimit = self.ILimit()
        self.vlimit = self.VLimit()

    def update_comms(self):
        """This function is used to ensure lower level consumer classes tied to the driver are updated to promote \
         instrument communications.
         """
        self.configlist._mycomms = self._mycomms
        self.protect._mycomms = self._mycomms
        self.ilimit._mycomms = self._mycomms
        self.vlimit._mycomms = self._mycomms

    class ConfigList:
        def __init__(self):
            self._mycomms = None

        def catalog(self):
            """
            This function returns the name of one source configuration list that is stored on the instrument.

            :return: The name of a configuration list.
            """
            self._mycomms.query("print(smu.source.configlist.catalog())")

        def create(self, list_name):
            """
            This function creates an empty source configuration list.

            :param list_name:
            :return:
            """
            self._mycomms.write(f"smu.source.configlist.create({list_name}))")

        def delete(self, list_name, index=None):
            """
            This function deletes a source configuration list.

            :param list_name:
            :param index:
            :return:
            """
            if index == None:
                self._mycomms.write(f"smu.source.configlist.delete(\"{list_name}\"))")
            else:
                self._mycomms.write(f"smu.source.configlist.delete(\"{list_name}\", {index}))")

        def query(self, list_name, index, field_separator=None):
            """
            This function returns a list of TSP commands and parameter settings that are stored in the specified \
            configuration index

            :param list_name: A string that represents the name of a source configuration list
            :param index: A number that defines a specific configuration index in the configuration list
            :param field_separator: String that represents the separator for the data; use one of the following,
                            * Comma (default): ,
                            * Semicolon: ;
                            * New line: \n

            :return:
            """
            if field_separator == None:
                self._mycomms.query(f"print(smu.source.configlist.query(\"{list_name}\", {index}))")
            else:
                self._mycomms.query(f"print(smu.source.configlist.query(\"{list_name}\", {index}, {field_separator}))")

        def recall(self, list_name, index=None, source_list_name=None, source_index=None):
            """
            This function recalls a configuration index in a source configuration list and an optional source \
            configuration list.

            :param list_name:
            :param index:
            :param source_list_name:
            :param source_index:
            :return:
            """
            if source_index == None:
                if index == None:
                    self._mycomms.write(f"smu.source.configlist.recall(\"{list_name}\")")
                else:
                    self._mycomms.write(f"smu.source.configlist.recall(\"{list_name}\", {index})")
            else:
                if source_index == None:
                    self._mycomms.write(
                        f"smu.source.configlist.recall(\"{list_name}\", {index}),\"{source_list_name}\")")
                else:
                    self._mycomms.write(
                        f"smu.source.configlist.recall(\"{list_name}\", {index}),\"{source_list_name}\","
                        f" {source_index})")

        def size(self, list_name):
            """
            This function returns the size (number of configuration indexes) of a source configuration list.

            :param list_name:
            :return:
            """
            self._mycomms.write(f"index_count = smu.source.configlist.zier(\"{list_name}\")")
            return int(self._mycomms.query("print(index_count)"))

        def store(self, list_name, index=None):
            """
            This function stores the active source settings into the named configuration list.

            :param list_name:
            :param index:
            :return:
            """
            if index == None:
                self._mycomms.write(f"smu.source.configlist.store(\"{list_name}\")")
            else:
                self._mycomms.write(f"smu.source.configlist.store(\"{list_name}\", {index})")

        def storefunc(self, list_name, function, index=None):
            """
            This function allows you to store the settings for a source function into a source configuration \
            list whether or not the function is active.

            :param list_name:
            :param function:
            :param index:
            :return:
            """
            function_str = None
            if function == smuconst.FUNC_DC_VOLTAGE:
                function_str = "smu.FUNC_DC_VOLTAGE"
            elif function == smuconst.FUNC_DC_CURRENT:
                function_str = "smu.FUNC_DC_VOLTAGE"
            elif function == smuconst.FUNC_RESISTANCE:
                function_str = "smu.FUNC_DC_RESISTANCE"

            if index == None:
                self._mycomms.write(f"smu.source.configlist.storefunc(\"{list_name}\", {function_str})")
            else:
                self._mycomms.write(f"smu.source.configlist.storefunc(\"{list_name}\", {function_str}, {index})")

    class Protect:
        def __init__(self):
            self._mycomms = None

    @property
    def func(self):
        """This attribute contains the source function, which can be voltage or current."""
        self._mycomms.write("srcfunc = smu.source.func")
        response = self._mycomms.query("print(srcfunc)").rstrip()
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
            self._mycomms.write("smu.source.func = smu.FUNC_DC_VOLTAGE")
            # print()
        else:
            self._mycomms.write("smu.source.func = smu.FUNC_DC_CURRENT")
            # print()

    @property
    def level(self):
        """This attribute immediately selects a fixed amplitude for the selected source function."""
        self._mycomms.write("srclev = smu.source.level")
        return float(self._mycomms.query("print(srclev)").rstrip())

    @level.setter
    def level(self, value):
        """This attribute immediately selects a fixed amplitude for the selected source function."""
        self._mycomms.write(f"smu.source.level = {value}")

    class ILimit:
        def __init__(self):
            self._mycomms = None

        @property
        def level(self):
            """This attribute selects the source limit for current measurements."""
            self._mycomms.write("ilimitlev = smu.source.ilimit.level")
            return float(self._mycomms.query("print(ilimitlev)").rstrip())

        @level.setter
        def level(self, value):
            """This attribute selects the source limit for current measurements."""
            self._mycomms.write(f"smu.source.ilimit.level = {value}")

        @property
        def tripped(self):
            """This attribute indicates if the source exceeded the limits that were set for the selected measurements."""
            self._mycomms.write("ilimittrip = smu.source.ilimit.tripped")
            return int(self._mycomms.query("print(ilimittrip)").rstrip())

    class VLimit:
        def __init__(self):
            self._mycomms = None

        @property
        def level(self):
            """This attribute selects the source limit for voltage measurements."""
            self._mycomms.write("vlimitlev = smu.source.vlimit.level")
            return float(self._mycomms.query("print(vlimitlev)").rstrip())

        @level.setter
        def level(self, value):
            """This attribute selects the source limit for voltage measurements."""
            self._mycomms.write(f"smu.source.vlimit.level = {value}")

        @property
        def tripped(self):
            """This attribute indicates if the source exceeded the limits that were set for the selected measurements."""
            self._mycomms.write("vlimittrip = smu.source.vlimit.tripped")
            return int(self._mycomms.query("print(vlimittrip)").rstrip())

    @property
    def output(self):
        """
        This attribute enables or disables the source output.

        :return: Either ON (1) or OFF (0).
        """
        self._mycomms.write("source_output = smu.source.output")
        source_output = self._mycomms.query("print(source_output)")
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
            self._mycomms.write("smu.source.output=smu.ON")
        else:
            self._mycomms.write("smu.source.output=smu.OFF")

import KeithleySeries2400InteractiveSmu_Constants as _SmuConst


class LocalNodeConfiguration:
    def __init__(self):
        self._mycomms = None
        # self.input = self.Input()

    def update_comms(self):
        """
        This function is used to ensure lower level consumer classes tied to the driver are updated to promote \
        instrument communications.

        :return:
        """
        # self.input._mycomms = self._mycomms

    def model(self):
        """
        This attribute stores the model number.

        :return: The model number of the instrument
        """
        return self._mycomms.query("print(localnode.model)")


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

import KeithleySeries2400InteractiveSmu_Constants as _SmuConst


class LocalNodeConfiguration:
    """
    Placeholder docstring description
    """
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


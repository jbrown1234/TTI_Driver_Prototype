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

# import KeithleySeries2400InteractiveSmu_Constants as _smuconst


class DataQueueConfiguration:
    """
    Placeholder docstring description.
    """
    def __init__(self):
        self._mycomms = None
        # self.input = self.Input()

    def update_comms(self):
        """
        This method is used to ensure lower level consumer classes tied to\
            the driver are updated to promote instrument communications.

        :return:
        """
        # self.input._mycomms = self._mycomms
        print(0)

    def add(self, value, timeout=None):
        """
        This method adds an entry to the data queue.

        :param value: (number) The data item to add; value can be of any type
        :param timeout: (int) The maximum number of seconds to wait for space
        in the data queue
        :return result: (bool) The resulting value of True or False based on
        the success of the method
        """
        if timeout is None:
            self._mycomms.write(f"result = dataqueue.add({value})")
        else:
            self._mycomms.write(f"result = dataqueue.add({value}, {timeout})")
        result = self._mycomms.query("print(result)")
        if "true" in result.lower():
            bool_return = True
        elif "false" in result.loweer():
            bool_return = False
        return bool_return

    def capacity(self):
        """
        This constant is the maximum number of entries that you can store in
        the data queue.

        :return count: The variable that is assigned the value of
        dataqueue.CAPACITY
        """
        self._mycomms.write("count = dataqueue.CAPACITY")
        _count = int(self._mycomms.query("print(count)"))
        return _count

    def clear(self):
        """
        This method clears the data queue.

        :return: None
        """
        self._mycomms.write("count = dataqueue.clear()")

    def count(self):
        """
        This attribute contains the number of items in the data queue.

        :return: count
        """
        self._mycomms.write("count = dataqueue.count")
        _count = int(self._mycomms.query("print(count)"))
        return _count

    def next(self, timeout=None):
        """
        This method removes the next entry from the data queue.

        :param timeout: The number of seconds to wait for data in the queue
        :return value: The next entry in the data queue
        """
        if timeout is None:
            self._mycomms.write("value = dataqueue.next()")
        else:
            self._mycomms.write("value = dataqueue.next(timeout)")
        value = float(self._mycomms.query("print(value)"))
        return value 

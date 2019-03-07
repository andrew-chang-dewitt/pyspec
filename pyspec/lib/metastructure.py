"""
Create a simple SpecStruct class used as a container for Describe objects.
Helps preserve intended run order & provides a single entry point for
running all test groups in a SpecStruct.
"""

import datetime

def spec_struct():
    """
    Used to initialize a new SpecStruct instance. This is the only function
    directly exposed by the API from this module.

    Arguments: 	None
    Returns: 	An instance of the SpecStruct class with an empty
    		test_groups attribute.
    """
    return SpecStruct()

class SpecStruct:
    """
    SpecStruct initializes with just one attribute: test_groups.
    All groups will be stored here. A list is used because it preserves
    member order with a numbered index & is easily searchable.
    """
    def __init__(self):
        self.test_groups = []
        self.results = []
        self.stats = StatsObj()

    def add_group(self, group):
        """
        Use add_group to add a new group to the SpecStruct instance.
        All groups should be added in the order they are intended to be run.
        """
        self.test_groups.append(group)

        return self.test_groups

    def remove_group(self, group):
        """
        Use to remove a group by providing the group desired to be removed as
        the argument. Just a simple wrapper for list.remove()
        """
        self.test_groups.remove(group)

        return self.test_groups

    def run_all(self, mute=False):
        """
        This function is the single entry point for running all tests held in
        test_groups. This allows any other program interfacing with the library
        to not need to know anything about how individual test groups are
        structured.
        """
        for group in self.test_groups:
            self.run_one(group)

        if not mute:
            for line in self.results:
                print(line)

        return self.results

    def run_one(self, group):
        """
        A simple wrapper to a Describe object's `run()` method. Includes a
        guard against calling `run()` on an inner test group since this would
        result in an AttributeError.
        """
        if not group.outer:
            group.run()

            for line in group.results:
                self.results.append(line)

class StatsObj:
    """
    A class for creating & tracking statistics for the SpecStruct class
    """

    def __init__(self):
        self.number_of_tests = None
        self.success_failure_rate = None
        self._time_started = None
        self._time_ended = None

    @property
    def total_time_elapsed(self):
        """
        Property getter for total_time_elapsed
        """
        if self._time_started is None or self._time_ended is None:
            return datetime.timedelta(0)

        return self._time_ended - self._time_started

    def start_time_tracking(self):
        """
        Method used to start tracking time for total elapsed
        """
        self._time_started = datetime.datetime.now()

        return self

    def stop_time_tracking(self):
        """
        Method used to stop time tracking
        """
        self._time_ended = datetime.datetime.now()

        return self

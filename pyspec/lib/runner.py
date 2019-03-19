"""
Create a simple Runner class used as a container for Describe objects.
Helps preserve intended run order & provides a single entry point for
running all test groups in a Runner.
"""

import datetime
from pub_sub import pub_sub

def runner(passed_pub_sub=None):
    """
    Used to initialize a new Runner instance. This is the only function
    directly exposed by the API from this module.

    Arguments: 	None
    Returns: 	An instance of the Runner class with an empty
    		test_groups attribute.
    """
    result = Runner()

    if passed_pub_sub:
        used_pub_sub = passed_pub_sub
    else:
        used_pub_sub = pub_sub

    used_pub_sub.topic('new test group').sub(result.add_group)
    used_pub_sub.topic('run requested').sub(result.run_all)

    return result

class Runner:
    """
    Runner initializes with just one attribute: test_groups.
    All groups will be stored here. A list is used because it preserves
    member order with a numbered index & is easily searchable.
    """
    def __init__(self):
        self.test_groups = []
        self.results = []
        self.stats = StatsObj()

    def add_group(self, group):
        """
        Use add_group to add a new group to the Runner instance.
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

    def run_all(self, muted=False):
        """
        This function is the single entry point for running all tests held in
        test_groups. This allows any other program interfacing with the library
        to not need to know anything about how individual test groups are
        structured.
        """
        # start time tracking for stats
        self.stats.start_time_tracking()

        for group in self.test_groups:
            self.run_one(group)

        # end time tracking for stats
        self.stats.stop_time_tracking()
        # compile stats into final line & append for printout
        self.results.append(self.stats.get_stats_string())

        if not muted:
            for line in self.results:
                print(line)

        return self.results

    def run_one(self, group):
        """
        A simple wrapper to a Describe object's `run()` method. Includes a
        guard against calling `run()` on an inner test group since this would
        result in an AttributeError.
        """
        # increment number of tests counter by number of tests in group
        self.stats.number_of_tests += len(group.tests)
        # parse for failed tests & increment failure counter
        for test in group.tests:
            if not test.success:
                self.stats.number_of_failed_tests += 1

        # also increment both stats for tests in inner groups
        for inner in group.inners:
            self.stats.number_of_tests += len(inner.tests)

            for test in inner.tests:
                if not test.success:
                    self.stats.number_of_failed_tests += 1

        if not group.outer:
            group.run(True)

            for line in group.results:
                self.results.append(line)

class StatsObj:
    """
    A class for creating & tracking statistics for the Runner class
    """

    def __init__(self):
        self.number_of_tests = 0
        self.number_of_failed_tests = 0
        self._time_started = None
        self._time_ended = None

    def start_time_tracking(self):
        """
        Method used to start tracking time for total elapsed
        """
        if self._time_started is None:
            self._time_started = datetime.datetime.now()

        return self

    def stop_time_tracking(self):
        """
        Method used to stop time tracking
        """
        self._time_ended = datetime.datetime.now()

        return self

    def get_stats_string(self):
        """
        Compiles stats into a human-readable string for printing with
        test results.
        """
        return (
            f'\n'
            f'Tests ran: {self.number_of_tests}\n'
            f'Success rate: {self.success_failure_rate * 100}%\n'
            f'Total time: {self.total_time_elapsed} microseconds\n'
        )

    @property
    def total_time_elapsed(self):
        """
        Property getter for total_time_elapsed in microseconds
        """
        if self._time_started is None or self._time_ended is None:
            return datetime.timedelta(0)

        return (self._time_ended - self._time_started).microseconds

    @property
    def success_failure_rate(self):
        """
        Property getter for failure rate, derived from number_of_tests &
        number_of_failed_tests
        """
        try:
            return (self.number_of_tests - self.number_of_failed_tests) / self.number_of_tests
        except ZeroDivisionError:
            return 0

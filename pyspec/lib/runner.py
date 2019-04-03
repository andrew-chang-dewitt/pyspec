"""
Create a simple Runner class used as a container for Describe objects.
Helps preserve intended run order & provides a single entry point for
running all test groups in a Runner.
"""

from pub_sub import stable
from pyspec.lib.stats import StatsObj

PUB_SUB = stable.event('pyspec')

def runner(alt_pub_sub=None):
    """
    Used to initialize a new Runner instance. This is the only function
    directly exposed by the API from this module.

    Arguments: 	None
    Returns: 	An instance of the Runner class with an empty
    		test_groups attribute.
    """
    if alt_pub_sub:
        used_pub_sub = alt_pub_sub
    else:
        used_pub_sub = PUB_SUB

    result = Runner(used_pub_sub)

    used_pub_sub.topic('new test group').sub(result.add_group)
    used_pub_sub.topic('run requested').sub(result.run_all)

    return result

class Runner:
    """
    Runner initializes with just one attribute: test_groups.
    All groups will be stored here. A list is used because it preserves
    member order with a numbered index & is easily searchable.
    """
    def __init__(self, passed_pub_sub):
        self.pub_sub = passed_pub_sub
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

        self.pub_sub.topic('run results').pub(self)
        return self

    def run_one(self, group):
        """
        A simple wrapper to a Describe object's `run()` method. Includes a
        guard against calling `run()` on an inner test group since this would
        result in an AttributeError.
        """
        # increment number of tests counter by number of tests in group
        self.stats.number_of_tests += len(group.tests)
        if not group.outer:
            group.run(True)

            for line in group.results:
                self.results.append(line)

        # parse for failed tests & increment failure counter
        for test in group.tests:
            if not test.result['success']:
                self.stats.number_of_failed_tests += 1

        # also increment both stats for tests in inner groups
        for inner in group.inners:
            self.stats.number_of_tests += len(inner.tests)

            for test in inner.tests:
                if not test.result['success']:
                    self.stats.number_of_failed_tests += 1

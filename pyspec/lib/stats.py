import datetime


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
            return (self.number_of_tests -
                    self.number_of_failed_tests) / self.number_of_tests
        except ZeroDivisionError:
            return 0

"""tests for SpecStruct metastructure"""

import pyspec
from pub_sub import stable

STATS_OBJ = pyspec.describe('generate stats info in the runner metastructure')

STATS_OBJ.test_run = pyspec.cli.run_tests.RunTests(stable.event('temp spec')).one_file(
    'tests/test_examples/temp_spec',
    True
)

print(f'test run: { STATS_OBJ.test_run }')
print(STATS_OBJ.test_run.pub_sub.name)
print(f'Runner test_groups is {STATS_OBJ.test_run.test_groups}')
for item in STATS_OBJ.test_run.test_groups:
    print(item.description)
print(STATS_OBJ.test_run.stats.get_stats_string())

STATS_OBJ.it(
    'has a stats object',
    lambda: STATS_OBJ.test_run.stats
).should.be_a(pyspec.lib.runner.StatsObj)

STATS_OBJ.it(
    'tracks number the number of tests',
    lambda: STATS_OBJ.test_run.stats.number_of_tests
).should.eq(2)

STATS_OBJ.it(
    'tracks the success/failure rate',
    lambda: STATS_OBJ.test_run.stats.success_failure_rate
).should.eq(.5)

STATS_OBJ.it(
    'tracks time on spec_struct() using methods on Stats class',
    lambda: STATS_OBJ.test_run.stats
).should.have_methods('start_time_tracking', 'stop_time_tracking')

STATS_OBJ.it(
    'tracks time elapsed for running tests',
    lambda: STATS_OBJ.test_run.stats.total_time_elapsed > 0
).should.eq(True)

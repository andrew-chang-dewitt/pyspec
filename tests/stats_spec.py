"""tests for SpecStruct metastructure"""

import pyspec

RUNNER = pyspec.spec_struct()

STATS = pyspec.describe('fetch stats info', RUNNER)

def test_stats():
    """
    Test run to get stats
    """
    STATS.test_group = pyspec.describe('test stats')
    STATS.test_group.it('can do stuff', 1).should.eq(1)
    STATS.test_results = STATS.test_group.run(True)
    stats_line = STATS.test_results[-1]

    return stats_line

STATS.it(
    'prints stats on the last line of a test',
    test_stats
    ).should.eq('Total time:')

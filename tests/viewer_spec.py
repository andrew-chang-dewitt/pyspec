from api import (describe, view)

view_available = describe('view information on available tests')

def test_groups():
    return view.test_groups('tests.runner_spec')

view_available.test_groups = test_groups

view_available.it('can compile & return a list object',
                  view_available.test_groups).should.be_a(list)

view_available.it('is a list with the containing the correct members',
                  view_available.test_groups).should.include('expectations',
                                                             'common',
                                                             'failures',
                                                             'outer',
                                                             'inner',
                                                             'list_groups')

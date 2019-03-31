"""
A module with custom classes for modifying Click
"""

import traceback
import click

class ErrorHandlingGroup(click.Group):
    """
    Wrapping the entire click command group in a try:except statement
    to handle errors more gracefully
    """
    
    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except Exception as err:
            click.echo(err)
            click.echo(traceback.format_exc())

class NoRunnerError(Exception):
    def __init__(self, module_name):
        msg = (f'The _spec module {module_name} has no RUNNER object, '
               f'please configure one with SpectStruct to use the Pyspec CLI')

        super().__init__(msg)

from time import sleep

import click

from picalendar.api import show_events


@click.group()
def cli():
    """
    Display upcoming events on a 16x2 LCD
    """
    pass


cli.add_command(show_events.show)


if __name__ == '__main__':
    cli()

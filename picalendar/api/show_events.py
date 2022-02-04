from time import sleep

import click

from picalendar import drivers
from picalendar.api.fetch_events import get_events


@click.command('show')
@click.option('-n', '--number', type=int, default=10,
              show_default=True, help='Number of events')
def show(number: int) -> None:
    """
    Retrieve and display upcoming events on a LCD
    """
    display = drivers.Lcd()
    events = get_events(number)
    try:
        if len(events) == 0:
            while True:
                display_message(display, 1, empty=True)
                sleep(5)
        else:
            while True:
                display_message(display, 1, events)
                sleep(5)
    except KeyboardInterrupt:
        display.lcd_clear()


def display_message(display: drivers.Lcd, row: int, events=None, empty=False) -> None:
    """
    Helper funtion for displaying events on a LCD
    """
    COLS = 16
    if empty == True:
        display.lcd_display_string('No upcoming', 1)
        display.lcd_display_string('events found :(', 2)
    else:
        for event in events:
            message = event.get('summary', '')
            start = event.get('start', '')
            end = event.get('end', '')

            if 'T' in start:
                start = start.replace('T', ' ')
            else:
                difference = COLS - len(start)
                start = start + ' ' * difference

            if 'T' in end:
                end = end.replace('T', ' ')
            else:
                difference = COLS - len(end)
                end = end + ' ' * difference

            display.lcd_display_string(f'{start}', 1)
            if len(message) > COLS:
                for i in range(0, len(message), COLS):
                    text_to_show = message[i: i + COLS].lstrip()
                    if len(text_to_show) < COLS:
                        difference = COLS - len(text_to_show)
                        text_to_show = text_to_show + ' ' * difference
                    display.lcd_display_string(text_to_show, 2)
                    sleep(4)
                    display.lcd_display_string(f'{end}', 1)

            else:
                if len(message) < COLS:
                    difference = COLS - len(message)
                    message = message + ' ' * difference
                display.lcd_display_string(message, 2)
                sleep(4)

            display.lcd_display_string(f'{end}', 1)
            sleep(4)

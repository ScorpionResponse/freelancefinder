"""Decorators used for harvesting sources."""

import datetime

import wrapt


def periodically(period='daily', check_name='last_processed', fail_return=None):
    """Ensure that the wrapped function only runs once per period."""
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        """Wrap function to enfore period."""
        source = instance.source

        timecheck = None

        if period == 'daily':
            timecheck = datetime.datetime.today().strftime("%Y-%m-%d")
        elif period == 'hourly':
            timecheck = datetime.datetime.today().strftime("%Y-%m-%d-%H")
        elif period == 'minutely':
            timecheck = datetime.datetime.today().strftime("%Y-%m-%d-%H-%M")

        if source.config.filter(config_key=check_name, config_value=timecheck).exists():
            return fail_return
        source.config.update_or_create(config_key=check_name, defaults={'config_value': timecheck})

        return wrapped(*args, **kwargs)
    return wrapper

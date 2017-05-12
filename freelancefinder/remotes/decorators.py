"""Decorators used for harvesting sources."""

import datetime

import wrapt

STRFTIME_MAP = {
    'daily': "%Y-%m-%d",
    'twice_daily': "%Y-%m-%d-%p",
    'hourly': "%Y-%m-%d-%H",
    'minutely': "%Y-%m-%d-%H-%M",
}


def periodically(period='daily', check_name='last_processed', fail_return=None):
    """Ensure that the wrapped function only runs once per period."""
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        """Wrap function to enfore period."""
        source = instance.source

        # Get our period defining key
        strftime_format = STRFTIME_MAP[period]
        timecheck = datetime.datetime.today().strftime(strftime_format)

        # Check if we've already got the value (aka already run this period)
        if source.config.filter(config_key=check_name, config_value=timecheck).exists():
            return fail_return

        # Call the function
        retval = wrapped(*args, **kwargs)

        # Update SourceConfig and return value
        source.config.update_or_create(config_key=check_name, defaults={'config_value': timecheck})
        return retval
    return wrapper

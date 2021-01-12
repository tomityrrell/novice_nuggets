'''
novice nugget #2: temporary dictionary state

Many times I've wanted to subset a dict, eg to remove large or sensitive values for logging,
and recently I saw code that replaced a dict value that's too big to log:

    content = data['content']
    data['content'] = 'too big to log'
    log.info('data=%s', data)
    data['content'] = content

There's no bug here, but I'd prefer code that better reflects the temporary nature of the dict's modified state.  How would you do this?

And only because we promised to try working recursion into this month's nugget: what if the keys_to_replace could be at any depth?  [Feel
free to make simplifying assumptions here.]

The code I saw was part of a bigger function, but here it's convenient to make it a function on its own.  You just need to modify the
shrink_for_novice_nuggets_2.pylogging function.  The main function checks that content is abbreviated in the log, but afterward remains unchanged.
'''

import pprint
import logging


# Solution 1: Using a custom Formatter to truncate logged messages
# https://stackoverflow.com/questions/16799075/in-a-python-logging-is-there-a-formatter-to-truncate-the-string

# Create loggers
default_logger = logging.getLogger("default")
truncated_logger = logging.getLogger("truncated")

# Create handlers
default_handler = logging.StreamHandler()
truncated_handler = logging.StreamHandler()

# Create formatters, limit message to 100 characters
truncated_formatter = logging.Formatter('%(message).100s... (too big to log)')

# Add formatters to handlers
truncated_handler.setFormatter(truncated_formatter)

# Add handlers to logger
default_logger.addHandler(default_handler)
truncated_logger.addHandler(truncated_handler)


# Solution 2:  Using a Pretty Printer!
# https://stackoverflow.com/questions/20514525/automatically-shorten-long-strings-when-dumping-with-pretty-print
# https://stackoverflow.com/questions/38533282/python-pretty-print-dictionary-of-lists-abbreviate-long-lists

# We extend the base class to truncate any strings that are longer than 20 characters
class TruncatedPrinter(pprint.PrettyPrinter):
    def _format(self, object, *args, **kwargs):
        if isinstance(object, str):
            if len(object) > 20:
                object = object[:20] + '... (too big to log)'
        return pprint.PrettyPrinter._format(self, object, *args, **kwargs)


# We can also handle recursive structures right out of the box with PrettyPrinter's depth parameter, and dictionary
# keys are sorted by default
truncated_printer = TruncatedPrinter(depth=1)


if __name__ == '__main__':
    data = {1: 2, 'a': 'b', 'content': 'abc' * 10_000}
    default_logger.warning("Default logger:  %s", data)

    # Solution 1
    truncated_logger.warning("Truncated logger:  %s", data)

    # Solution 2
    truncated_printer.pprint(data)

    # Create a nested dictionary
    big_data = {1: 2, 'a': 'b', 'content': 'abc' * 10_000, 'data': data}
    truncated_printer.pprint(big_data)


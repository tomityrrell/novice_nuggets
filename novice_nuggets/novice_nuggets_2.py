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
shrink_for_logging function.  The main function checks that content is abbreviated in the log, but afterward remains unchanged.
'''

import logging
log = logging.getLogger()


def shrink_for_logging(data):

    content = data['content']
    data['content'] = 'too big to log'
    log.info('data=%s', data)
    data['content'] = content


def main():

    class LogCatcher(logging.StreamHandler):
        # handler to collect log output for testing.
        def emit(self, record):
            msg = record.getMessage()
            print(msg)
            # check 1: ensure dict content is abbreviated.
            assert "'content': 'too big to log'" in msg

    log.setLevel('INFO')
    log.addHandler(LogCatcher())

    data = {1: 2, 'a': 'b', 'content': 'abc' * int(1e4)}

    shrink_for_logging(data)

    # check 2: ensure dict has not changed
    assert data == {1: 2, 'a': 'b', 'content': 'abc' * int(1e4)}, \
            'dictionary should not have changed but did'


if __name__ == '__main__': import sys; sys.exit(main())

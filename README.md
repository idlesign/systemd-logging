# systemd-logging

<https://github.com/idlesign/systemd-logging>

[![release](https://img.shields.io/pypi/v/systemd-logging.svg)](https://pypi.python.org/pypi/systemd-logging)
[![lic](https://img.shields.io/pypi/l/systemd-logging.svg)](https://pypi.python.org/pypi/systemd-logging)
[![coverage](https://img.shields.io/coveralls/idlesign/systemd-logging/master.svg)](https://coveralls.io/r/idlesign/systemd-logging)

## Description

*Simplifies logging for systemd*

**Requires Python 3.10+**

* No need to compile (pure Python), uses `libsystemd.so`.
* Simplified configuration.
* Just logging. Nothing more.

## Usage

```python
import logging

from systemdlogging.toolbox import init_systemd_logging

# This one line in most cases would be enough.
# By default it attaches systemd logging handler to a root Python logger.
init_systemd_logging()  # Returns True if initialization went fine.

# Now you can use logging as usual.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug('My debug message')

try:
    raise ValueError('Log me please')

except ValueError:
    # Additional context can be passed in extra.context.
    logger.exception('Something terrible just happened', extra={
        'message_id': True,  # Generate message ID automatically.
        'context': {
            'FIELD1': 'one',
            'FIELD2': 'two',
        }
    }, stack_info=True)
```

systemd-logging
===============
https://github.com/idlesign/systemd-logging

|release| |lic| |ci| |coverage|

.. |release| image:: https://img.shields.io/pypi/v/systemd-logging.svg
    :target: https://pypi.python.org/pypi/systemd-logging

.. |lic| image:: https://img.shields.io/pypi/l/systemd-logging.svg
    :target: https://pypi.python.org/pypi/systemd-logging

.. |ci| image:: https://img.shields.io/travis/idlesign/systemd-logging/master.svg
    :target: https://travis-ci.org/idlesign/systemd-logging

.. |coverage| image:: https://img.shields.io/coveralls/idlesign/systemd-logging/master.svg
    :target: https://coveralls.io/r/idlesign/systemd-logging


Description
-----------

*Simplifies logging for systemd*

**Requires Python 3.6+**

* No need to compile (pure Python), uses ``libsystemd.so``.
* Simplified configuration.
* Just logging. Nothing more.


Usage
-----

.. code-block:: python

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


Read the docs to find out more.


Documentation
-------------

https://systemd-logging.readthedocs.org/

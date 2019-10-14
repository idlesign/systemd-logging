Quickstart
==========


.. code-block:: python

    import logging

    from systemdlogging.toolbox import init_systemd_logging

    # This one line in most cases would be enough.
    init_systemd_logging()
    # By default it attaches systemd logging handler to a root Python logger.

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


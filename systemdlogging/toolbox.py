import logging
import os
import syslog
import uuid
from typing import Optional

from .backend_ctyped import send


PRIORITY_MAP = {
    logging.CRITICAL: syslog.LOG_CRIT,
    logging.ERROR: syslog.LOG_ERR,
    logging.WARNING: syslog.LOG_WARNING,
    logging.INFO: syslog.LOG_INFO,
    logging.DEBUG: syslog.LOG_DEBUG,
}


def log_message(*, level: int, msg: str, context: Optional[dict] = None) -> bool:
    """Sends a message to systemd.

    .. warning:: Low level function. You may want to
        use more convenient `init_systemd_logging()` or `SystemdHandler` and `SystemdFormatter`.

    Natively supported fields:
        http://0pointer.de/public/systemd-man/systemd.journal-fields.html


    :param level: Logging level.
    :param msg: Message text to send.
    :param context: Additional context to send within message.

    """
    args = {
        'PRIORITY': PRIORITY_MAP.get(level, level),
    }

    args.update(context or {})

    return send(
        b'MESSAGE=%s', msg.encode(),  # Prevents %-formatting in messages.
        *[f'{key}={val}'.encode() for key, val in args.items()],
        None
    ) == 0


class SystemdHandler(logging.Handler):
    """Allows passing log messages to systemd.

    Additional information may be passed in ``extra`` dictionary:

        * context - Dictionary with additional information to attach to a message.
        * message_id - Message ID (usually UUID to assign to the message).
            If ``True`` ID will be generated automatically

    .. code-block: python

        logger.exception('This is my exceptional log entry.', extra={
            'message_id': True,
            'context': {
                'MY_FIELD': 'My value',
            }
        }, stack_info=True)

    Fills in the following fields automatically:

        * CODE_FILE - Filename
        * CODE_LINE - Code line number
        * CODE_FUNC - Code function name
        * CODE_MODULE - Python module name
        * LOGGER - Logger name
        * THREAD_ID - Thread ID if any
        * THREAD_NAME - Thread name if any
        * PROCESS_NAME - Process name if any
        * PRIORITY - Priority based on logging level

    Optionally fills in:
        * TRACEBACK - Traceback information if available
        * STACK - Stacktrace information if available
        * MESSAGE_ID - Message ID (if context.message_id=True)

    """

    syslog_id: str = ''
    """SYSLOG_IDENTIFIER to add to message. If not set command name is used."""

    def emit(self, record: logging.LogRecord):

        context = {
            # Generic
            'CODE_FILE': record.pathname,
            'CODE_LINE': record.lineno,
            'CODE_FUNC': record.funcName,
            # Custom
            'CODE_MODULE': record.module,
            'LOGGER': record.name,
            'THREAD_ID': record.thread,
            'THREAD_NAME': record.threadName,
            'PROCESS_NAME': record.processName,
        }

        try:
            exc_info = record.exc_info
            if exc_info:
                context['TRACEBACK'] = self.formatter.formatException(exc_info)

            stack_info = record.stack_info
            if stack_info:
                context['STACK'] = self.formatter.formatStack(stack_info)

            syslog_id = self.syslog_id
            if syslog_id:
                context['SYSLOG_IDENTIFIER'] = syslog_id

            msg = self.format(record)

            message_id = getattr(record, 'message_id', None)

            if message_id:

                if message_id is True:
                    # Generate message ID automatically.
                    message_id = uuid.uuid3(uuid.NAMESPACE_OID, '|'.join(str(val) for val in (
                        msg, record.levelno, record.pathname, record.funcName
                    ))).hex

                context['MESSAGE_ID'] = message_id

            context_ = getattr(record, 'context', {})
            context.update(context_)

            log_message(level=record.levelno, msg=msg, context=context)

        except Exception:  # pragma: nocover
            self.handleError(record)


class SystemdFormatter(logging.Formatter):
    """Formatter for systemd."""

    def format(self, record):
        # This one is just like its parent just doesn't
        # append traceback etc. to the message.
        record.message = record.getMessage()
        return self.formatMessage(record)


def check_for_systemd() -> bool:
    """Checks whether current process is run under systemd
    (and thus its output is connected to journald).

    """
    return bool(os.environ.get('INVOCATION_ID'))  # Works with systemd v232+


def init_systemd_logging(*, logger: Optional[logging.Logger] = None, syslog_id: str = '') -> bool:
    """Initializes logging to send log messages to systemd.

    Returns boolean indicating initialization went fine (see also `check_for_systemd()`).

    If it wasn't one may either to fallback to another logging handler
    or leave it as it is possibly sacrificing some log context.

    :param logger: Logger to attach systemd logging handler to.
        If not set handler is attached to a root logger.

    :param syslog_id: Value to be used in SYSLOG_IDENTIFIER message field.

    """
    systemd_ok = check_for_systemd()

    if systemd_ok:
        handler = SystemdHandler()
        handler.syslog_id = syslog_id
        handler.setFormatter(SystemdFormatter())

        logger = logger or logging.getLogger()
        logger.addHandler(handler)

    return systemd_ok

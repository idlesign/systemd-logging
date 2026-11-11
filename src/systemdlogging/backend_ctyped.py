import logging

from ctyped.exceptions import CtypedException
from ctyped.toolbox import Library

LOGGER = logging.getLogger(__name__)


def send_stub(*fmt):  # pragma: nocover
    """Dummy send function to be used when the real one
    is not available (e.g. no libsystemd found).

    """
    return None


try:
    lib = Library('libsystemd.so', prefix='sd_journal_')

except CtypedException:  # pragma: nocover

    send = send_stub

    LOGGER.warning("systemd library is not available and won't be used for logging")

else:

    @lib.function()
    def send(*fmt) -> int:  # pragma: nocover
        ...


    lib.bind_types()

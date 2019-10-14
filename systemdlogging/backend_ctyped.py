from ctyped.toolbox import Library


lib = Library('libsystemd.so', prefix='sd_journal_')


@lib.function()
def send(*fmt) -> int:  # pragma: nocover
    ...


lib.bind_types()

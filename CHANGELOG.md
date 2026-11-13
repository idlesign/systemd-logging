# systemd-logging changelog

### Unreleased
* ** check_for_systemd() now verifies JOURNAL_STREAM against the actual stdout/stderr descriptors, falling back to INVOCATION_ID (close #1).

### v1.0.1 [2022-01-28]
* ** Prevent segfaults for values having format placeholders like %s (see #6).

### v1.0.0 [2021-07-14]
* ** Celebrating 1.0.0.
* ** CtypedException is now hidden to improve plugability (see #5).

### v0.3.1 [2021-01-25]
* ** Proper % handling in messages (see #3).

### v0.3.0 [2020-01-28]
* ++ init_systemd_logging() now tries to detect systemd and returns boolean.

### v0.2.0 [2019-10-15]
* ++ Added an option to set SYSLOG_IDENTIFIER.
* ** Removed PROCESS_ID field in favor of _PID.

### v0.1.0 [2019-10-14]
* ++ Basic functionality.

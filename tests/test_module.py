import logging
import os
from sys import version_info

from systemdlogging.toolbox import init_systemd_logging

LINE_NO = '19' if version_info >= (3, 8) else '25'


def raiseme():
    logger = logging.getLogger('mysystemdlogger')
    logger.setLevel(logging.DEBUG)

    try:
        raise ValueError('durutum')

    except ValueError:

        logger.exception('My message', extra={
            'message_id': True,
            'context': {
                'FIELD1': 'one',
                'FIELD2': 'two',
            }
        }, stack_info=True)


def test_basic(monkeypatch):

    assert not init_systemd_logging(syslog_id='logtest')

    os.environ['INVOCATION_ID'] = 'dummy-invocation-id'

    assert init_systemd_logging(syslog_id='logtest')

    send_log = []

    def send_mock(*args):

        args = list(args)
        assert isinstance(args[0], bytes)
        assert args.pop() is None

        entry = {}
        for arg in args:
            key, _, val = arg.decode().partition('=')
            entry[key] = val

        send_log.append(entry)

    monkeypatch.setattr('systemdlogging.toolbox.send', send_mock)

    raiseme()

    assert len(send_log) == 1
    entry = send_log[0]

    assert entry['MESSAGE'] == '%s'
    assert entry['My message'] == ''

    assert entry['PRIORITY'] == '3'
    assert entry['CODE_FILE'].endswith('tests/test_module.py')
    assert entry['CODE_LINE'] == LINE_NO
    assert entry['CODE_FUNC'] == 'raiseme'
    assert entry['CODE_MODULE'] == 'test_module'
    assert entry['LOGGER'] == 'mysystemdlogger'
    assert entry['SYSLOG_IDENTIFIER'] == 'logtest'
    assert entry['THREAD_ID']
    assert entry['THREAD_NAME']
    assert entry['PROCESS_NAME']
    assert 'ValueError: durutum' in entry['TRACEBACK']
    assert f', line {LINE_NO}, in raiseme' in entry['STACK']
    assert entry['MESSAGE_ID']
    assert entry['FIELD1'] == 'one'
    assert entry['FIELD2'] == 'two'

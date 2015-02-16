#!/usr/bin/env python2

import sys

from logging import *
from logging.handlers import SysLogHandler
from argparse import ArgumentParser


def parse():
    """Parse commandline arguments"""

    parser = ArgumentParser()
    parser.add_argument('--facility', '-f', help='Syslog facility', default='user')
    parser.add_argument('--tag', '-t', help='Syslog tag')
    parser.add_argument('--cee', '-c', help='Add CEE cookie', action='store_true')

    return parser.parse_args()


def get_facility(facility):
    """Get facility"""

    facility_names = SysLogHandler.facility_names
    if facility not in facility_names:
        raise TypeError("{} is not a valid facility".format(facility))
    else:
        facility = facility_names.get(args.facility)
        return facility

if __name__ == "__main__":
    args = parse()
    extra = {'tag': args.tag}

    log = getLogger()
    log.setLevel(INFO)

    try:
        facility = get_facility(args.facility)
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        sys.exit(1)

    log_handle = SysLogHandler(address='/dev/log', facility=facility)
    fmt = Formatter('%(tag)s: %(message)s')
    log_handle.setFormatter(fmt)
    log.addHandler(log_handle)
    log = LoggerAdapter(log, extra)

    while True:
        line = sys.stdin.readline()
        if not line:
            break
        if args.cee:
            line = '@cee: ' + line
        log.info(line)

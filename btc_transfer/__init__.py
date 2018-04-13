#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import argparse
import logging


def setup_logging():
    parser = argparse.ArgumentParser(
            description=('Tool to send tokens from a smart contract'
                         ' based on BTC transactions'))

    parser.add_argument(
        '-s', '--silent',
        help="Print debugging statements",
        action="store_const", dest="loglevel", const=logging.CRITICAL,
        default=logging.WARNING,
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    parser.add_argument(
        '-vv', '--debug',
        help="Print debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
    )

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)


def main():
    setup_logging()

    from . import rpc_server
    server = rpc_server.SendTokensServer()
    server.run()
    return 0

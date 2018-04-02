#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

from .wallet import EthWallet
import server

default_wallet = EthWallet()


def main():
    server = SendTokensServer()
    server.run()

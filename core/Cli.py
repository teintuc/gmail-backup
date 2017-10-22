#!/usr/bin/env python

import sys
import signal
import argparse

from core.Mail import client
from core.Backup import backup
from core.Config import configuration

class cliHandler:

    __mailRsc = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.__signal_handler)

    def __signal_handler(self, signal, frame):
        sys.exit(0)

    def appArgs(self):
        parser = argparse.ArgumentParser()
        self.__args = parser.parse_args()

    def appConfig(self):
        configRsc = configuration()
        self.__config = configRsc.get()

    def run(self):
        self.appArgs()
        self.appConfig()
        # Get a backup resource in order to save the mails
        self.backupRsc = backup(self.__config.get('backup', 'path'))
        # Create a mail client and save the emails
        self.__mailRsc = client()
        self.__mailRsc.connect(self.__config.get('server', 'address'), self.__config.get('server', 'email'), self.__config.get('server', 'pass'))
        self.__mailRsc.saveMailbox(self.__config.get('server', 'mailbox'), self.backupRsc.save)
        self.__mailRsc.close()

        return 0

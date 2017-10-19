#!/usr/bin/env python

import argparse
from core.Config import configuration

class cliHandler:
    def appArgs(self):
        parser = argparse.ArgumentParser()
        self.__args = parser.parse_args()

    def appConfig(self):
        configRsc = configuration()
        self.__config = configRsc.get()

    def run(self):
        self.appArgs()
        self.appConfig()
        print(self.__config)
        return 0

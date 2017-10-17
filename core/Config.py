#!/usr/bin/env python

import os
import errno
import configparser

class configuration:

    __configPath = ".gmailbackup"

    __configFileName = "config"

    def __init__(self):
        # Set config file path
        self.__configFilePath = os.environ["HOME"] + "/" + self.__configPath + "/" + self.__configFileName

    def __makeConfigDir(self):
        # Attempt to create the configuration directory
        configDir = os.environ["HOME"] + "/" + self.__configPath
        try:
            os.makedirs(configDir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise  # raises the error again
            else:
                print("Backup directory: " + configDir + " already exists")

    def __generateConfiguration(self, configRsc):
        self.__makeConfigDir()
        configRsc.add_section('Section1')
        # configRsc.set('Section1', 'an_int', '15')

        # Writing our configuration file to 'example.cfg'
        with open(self.__configFilePath, 'wb') as configfile:
            configRsc.write(configfile)

    def getConfig(self):
        configRsc = configparser.RawConfigParser()
        if not os.path.exists(self.__configFilePath):
            print("Configuration file " + self.__configFilePath + " not found. Generating it ....")
            self.__generateConfiguration(configRsc)

        return configRsc.read(self.__configFilePath)

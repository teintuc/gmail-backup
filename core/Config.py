#!/usr/bin/env python

import os
import configparser

from core.Utils import Ui
from core.Utils import FileSystem

class configuration:

    __configPath = ".gmailbackup"

    __configFileName = "config"

    __configFileMode = 0o600

    __configSections = [
        'server',
        'backup'
    ]

    __userDataQuery = [
            ('server', 'address', 'Server address', None),
            ('server', 'directory', 'Email directory (ex: INBOX)', None),
            ('server', 'email', 'Email address', None),
            ('server', 'pass', 'Email password', None),
            ('backup', 'path', 'Backup directory', os.path.expanduser)
    ]

    def __init__(self):
        # Get a config parse rsc
        self.__configRsc = configparser.RawConfigParser()
        # Set config file path
        self.__configDir = os.path.join(os.environ["HOME"], self.__configPath)
        self.__configFilePath = os.path.join(self.__configDir, self.__configFileName)

    def __getUserData(self):
        # Set the sections
        for section in self.__configSections:
            self.__configRsc.add_section(section)
        # Set the values
        uiRsc = Ui()
        for section, key, prompt, modifier in self.__userDataQuery:
            answer = uiRsc.getValue(prompt)
            if len(answer) > 0:
                # If we have a modifier
                if modifier != None:
                    answer = modifier(answer)
                # Set the answer in the configuration
                self.__configRsc.set(section, key, answer)

    def __generate(self):
        self.__getUserData()

        # Writing our configuration
        fsRsc = FileSystem()
        fsRsc.makeDirs(self.__configDir)
        with open(self.__configFilePath, 'w') as configfile:
            self.__configRsc.write(configfile)
            configfile.close()
        os.chmod(self.__configFilePath, self.__configFileMode)

    def get(self):
        # If we don't have a config file, we generate it with information from the user
        if not os.path.exists(self.__configFilePath):
            print("Configuration file %s not found. Generating it ...." % self.__configFilePath)
            self.__generate()

        # What ever happen, we read the configuration
        self.__configRsc.read(self.__configFilePath)
        return self.__configRsc

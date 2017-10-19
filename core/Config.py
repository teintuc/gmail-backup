#!/usr/bin/env python

import os
import sys
import errno
import configparser

class configuration:

    __configPath = ".gmailbackup"

    __configFileName = "config"

    __configFileMode = 0o400

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
        self.__configFilePath = os.environ["HOME"] + "/" + self.__configPath + "/" + self.__configFileName

    def __makeDir(self):
        # Attempt to create the configuration directory
        configDir = os.environ["HOME"] + "/" + self.__configPath
        try:
            os.makedirs(configDir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise  # raises the error again
            else:
                print("Backup directory: " + configDir + " already exists")

    def __getUserData(self):
        for section in self.__configSections:
            self.__configRsc.add_section(section)

        for section, key, prompt, modifier in self.__userDataQuery:
            answer = self.__writePrompt(prompt)
            if len(answer) > 0:
                # If we have a modifier
                if modifier != None:
                    answer = modifier(answer)
                # Set the answer in the configuration
                self.__configRsc.set(section, key, answer)

    def __writePrompt(self, prompt):
        sys.stdout.write(prompt + ": ")
        sys.stdout.flush()
        return input()

    def __generate(self):
        self.__getUserData()

        # Writing our configuration
        self.__makeDir()
        with open(self.__configFilePath, 'w') as configfile:
            self.__configRsc.write(configfile)
            configfile.close()
        os.chmod(self.__configFilePath, self.__configFileMode)

    def get(self):
        # If we don't have a config file, we generate it with information from the user
        if not os.path.exists(self.__configFilePath):
            print("Configuration file " + self.__configFilePath + " not found. Generating it ....")
            self.__generate()

        # What ever happen, we read the configuration
        self.__configRsc.read(self.__configFilePath)
        return self.__configRsc

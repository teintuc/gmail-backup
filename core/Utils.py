#!/usr/bin/env python

import os
import sys
import errno

class FileSystem:
    def makeDirs(self, path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise  # raises the error again

    def writeToFile(self, path, content, openMode = 'wb', mode = 0o644):
        fd = open(path, openMode)
        fd.write(content)
        fd.close()
        os.chmod(path, mode)

    def readFromFile(self, path):
        fd = open(path, 'r')
        content = fd.readline()
        fd.close()
        return content

class Ui:
    def getValue(self, prompt):
        sys.stdout.write(prompt + ": ")
        sys.stdout.flush()
        return input()

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

class Ui:
    def getValue(self, prompt):
        sys.stdout.write(prompt + ": ")
        sys.stdout.flush()
        return input()

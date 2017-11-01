#!/usr/bin/env python

import os
import time
import email
import datetime
import mimetypes

from core.Utils import FileSystem

class backup:

    __timeMarkFileName = '.lastMail'

    __multiKeyWord = 'multipart'

    __defaultExt = '.bin'

    def __init__(self, backupDir):
        self.__backupDir = backupDir
        self.__fsRsc = FileSystem()
        # Create the base backup dir
        self.__fsRsc.makeDirs(self.__backupDir)
        # Last mail file path
        self.__lastMailFilePath = os.path.join(self.__backupDir, self.__timeMarkFileName)

    def __formatDate(self, rawEmailDate, outFormat = '%d/%m/%Y %H:%M:%S'):
        parsedEmailDate = email.utils.parsedate(rawEmailDate)
        timeStamp = time.mktime(parsedEmailDate)
        d = datetime.datetime.fromtimestamp(timeStamp)
        return datetime.date.strftime(d, outFormat)

    def __getPartFileName(self, part, partIndex):
        filename = part.get_filename()
        if not filename:
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                # Use a generic bag-of-bits extension
                ext = self.__defaultExt
            filename = 'part-%03d%s' % (partIndex, ext)
        return filename

    def __savePart(self, part, partIndex):
        filename = self.__getPartFileName(part, partIndex)
        self.__fsRsc.writeToFile(os.path.join(self.__currentBackupEmailPath, filename), part.get_payload(decode=True))

    def __saveLastMailDate(self, date):
        self.__fsRsc.writeToFile(self.__lastMailFilePath, date+'\n', 'w')

    def getLastMailDate(self):
        if not os.path.exists(self.__lastMailFilePath):
            return None

        return self.__fsRsc.readFromFile(self.__lastMailFilePath).rstrip()

    def save(self, rawEmail):
        msg = email.message_from_string(rawEmail.decode("utf-8"))
        emailFrom = email.utils.parseaddr(msg['From'])[1]
        emailDate = self.__formatDate(msg['Date'], '%A %d %b %Y %H:%M:%S')
        self.__currentBackupEmailPath = os.path.join(self.__backupDir, emailFrom, emailDate)
        print("> %s => %s" % (emailDate, emailFrom))

        partIndex = 0
        self.__fsRsc.makeDirs(self.__currentBackupEmailPath)
        for part in msg.walk():
            if part.get_content_maintype() == self.__multiKeyWord:
                continue

            self.__savePart(part, partIndex)
            partIndex += 1
        # Save the email date
        self.__saveLastMailDate(self.__formatDate(msg['Date'], '%d-%b-%Y'))

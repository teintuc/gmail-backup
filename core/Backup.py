#!/usr/bin/env python

import os
import time
import email
import datetime
import mimetypes

from core.Utils import FileSystem

class backup:

    __multiKeyWord = 'multipart'

    __defaultExt = '.bin'

    def __init__(self, backupDir):
        self.__backupDir = backupDir
        self.__fsRsc = FileSystem()
        self.__fsRsc.makeDirs(self.__backupDir)

    def __parseEmail(self, rawEmailAddress):
        return email.utils.parseaddr(rawEmailAddress)[1]

    def __formatDate(self, rawEmailDate, outFormat = '%d/%m/%Y %H:%M:%S'):
        parsedEmailDate = email.utils.parsedate(rawEmailDate)
        emailTimeStamp = time.mktime(parsedEmailDate)
        d = datetime.datetime.fromtimestamp(emailTimeStamp)
        return datetime.date.strftime(d, outFormat)

    def __createEmailBackupPath(self, msg):
        emailFrom = self.__parseEmail(msg['From'])
        emailDate = self.__formatDate(msg['Date'], '%A %d %b %Y %H:%M:%S')
        self.__currentBackupEmailPath = os.path.join(self.__backupDir, emailFrom, emailDate)
        self.__fsRsc.makeDirs(self.__currentBackupEmailPath)

    def __savePart(self, part, index):
        if part.get_content_maintype() == self.__multiKeyWord:
            return

        filename = part.get_filename()
        if not filename:
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                # Use a generic bag-of-bits extension
                ext = self.__defaultExt
            filename = 'part-%03d%s' % (index, ext)

        self.__fsRsc.writeToFile(os.path.join(self.__currentBackupEmailPath, filename), part.get_payload(decode=True))

    def save(self, rawEmail):
        msg = email.message_from_string(rawEmail.decode("utf-8"))
        self.__createEmailBackupPath(msg)
        print("> %s => %s" % (self.__formatDate(msg['Date']), self.__parseEmail(msg['From'])))
        index = 0
        for part in msg.walk():
            self.__savePart(part, index)
            index += 1

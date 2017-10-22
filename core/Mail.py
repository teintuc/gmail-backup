#!/usr/bin/env python

import imaplib

class client:

    __rfc = '(RFC822)'

    __search = 'ALL'

    __selectedMailbox = False

    def connect(self, address, login, password):
        self.__imapRsc = imaplib.IMAP4_SSL(address)
        self.__imapRsc.login(login, password)

    def __selectDir(self, mailbox):
        self.__imapRsc.select(mailbox)
        self.__selectedMailbox = True

    def saveMailbox(self, mailbox, callback = None):
        self.__imapRsc.list()
        self.__selectDir(mailbox)

        typ, data = self.__imapRsc.search(None, self.__search)
        for num in data[0].split():
            typ, data = self.__imapRsc.fetch(num, self.__rfc)
            if callback is not None:
                callback(data[0][1])

    def close(self):
        if self.__selectedMailbox is True:
            self.__imapRsc.close()
        self.__imapRsc.logout()

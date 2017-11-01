#!/usr/bin/env python

import imaplib

class client:

    __rfc = '(RFC822)'

    __defaultSearchCriteria = 'ALL'

    __selectedMailbox = False

    def connect(self, address, login, password):
        self.__imapRsc = imaplib.IMAP4_SSL(address)
        self.__imapRsc.login(login, password)

    def __selectDir(self, mailbox):
        self.__imapRsc.select(mailbox)
        self.__selectedMailbox = True

    def __getSearchCriteria(self, lastMailDate):
        criteria = self.__defaultSearchCriteria
        if lastMailDate is not None:
            criteria = 'SINCE ' + lastMailDate
        return criteria


    def saveMailbox(self, mailbox, lastMailDate, callback = None):
        self.__selectDir(mailbox)

        ret, data = self.__imapRsc.search(None, self.__getSearchCriteria(lastMailDate))
        if ret != 'OK':
            print("No email found")
            return

        for num in data[0].split():
            ret, data = self.__imapRsc.fetch(num, self.__rfc)
            if ret != 'OK':
                print("Can't fetch the email")
                continue

            if callback is not None:
                callback(data[0][1])

    def close(self):
        if self.__selectedMailbox is True:
            self.__imapRsc.close()
        self.__imapRsc.logout()

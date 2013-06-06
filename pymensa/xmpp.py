#!/usr/bin/python
# coding: utf-8
"""
    Modul zum senden von XMPP-Nachrichten
"""
__author__ = 'Henning Dickten'

import sys
from pyxmpp2.simple import send_message


class XmppClient(object):
    """
    Modul für die Kommunikation über XMPP


    """
    def __init__(self, parsed_config):
        self.user = parsed_config.get('xmpp', 'user')
        self.passwd = parsed_config.get('xmpp', 'passwd')
        #self.rescource = parsed_config.get('xmpp', 'rescource')

    def send_message(self, target_jid, message, **kwargs):
        """
        Sendet eine Nachricht an den Empfänger target_jid
        """
        if sys.version_info.major < 3:
            message = message.encode('utf-8')
            target_jid = target_jid.encode('utf-8')

        send_message(self.user, self.passwd, target_jid, message, **kwargs)

    def send_group_message(self, group, message, **kwargs):
        """
        Sendet eine Nachricht an eine Empfängergruppe weiter
        """
        for jid in group:
            self.send_message(jid.decode('utf-8'), message, **kwargs)


if __name__ == '__main__':
    pass

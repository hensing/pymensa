#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    PyMensa convenience functions
"""
__author__ = 'Henning Dickten'

from os import path
from warnings import warn
from ConfigParser import SafeConfigParser

from . import menuparser
from .database import MenuDatabase
from .xmpp import XmppClient


def todays_menu_to_string(menu, discard_soft_hyphen=False):
    """
    Returns the menu as string

    if 'discard_soft_hyphen' is True, all \'\\xad\' will be discarded
    """
    export = u'Heute in der ♥ Mensa ♥:\n=======================\n'

    for entry in menu:
        temp = '\n' + entry.counter + ':'
        temp += '\n    ' + entry.dish
        if entry.info is not None:
            temp += '\n    ' + entry.info
        if entry.price is not None:
            temp += '\n    ' + entry.price
        export += temp

    if discard_soft_hyphen is True:
        return export.replace(u'\xad', u'')
    else:
        return export


def safe_get_todays_menu(config):
    """
    Conveniencefunction to get the menu with retry on error
    """
    db_path = path.expanduser(config.get('database', 'path'))
    if path.exists(db_path) is not True:
        warn('Database does not exists! Creating ...')
        create_db(config)
        update_db(config)

    menu_db = MenuDatabase(db_path)

    try:
        menu = menu_db.get_todays_menu()
    except IndexError:
        # day not found:
        update_db(config)
        try:
            menu = menu_db.get_todays_menu()
        except IndexError:
            warn("nothing found for today!")
            raise SystemExit(1)
    return menu


def create_db(config):
    """
    Creates a new mensamenu database
    """
    db_path = path.expanduser(config.get('database', 'path'))
    if path.exists(db_path):
        warn('Database already existss!\n')
    else:
        menu_db = MenuDatabase(db_path)
        menu_db.create_db()


def update_db(config):
    """
    updates the mensamenu database
    """
    db_path = path.expanduser(config.get('database', 'path'))
    if path.exists(db_path) is not True:
        warn('Database does not exists! Creating ...')
        create_db(config)

    if config.get('debug', 'debug') == '1':
        print('Updating ...')

    menu_db = MenuDatabase(db_path)
    parser = config.get('mensa', 'parser')
    myparser = menuparser.Parser()
    myparser = eval("menuparser." + parser + '()')
    menu_list = myparser.get_menu()
    menu_db.update_db(menu_list)


def print_todays_menu(config):
    """
    prints todays mensamenu
    """
    menu = safe_get_todays_menu(config)
    print('')
    print(todays_menu_to_string(menu, discard_soft_hyphen=True))
    print('')


def send_xmpp(config):
    """
    sends todays menu via xmpp to all groupmembers
    """
    xclient = XmppClient(config)
    menu = safe_get_todays_menu(config)
    menu_str = todays_menu_to_string(menu)
    group = config.get('gruppen', 'mensagang').split()
    xclient.send_group_message(group, menu_str)


def parse_config(configfile=None):
    """
    returns the parsed config (for a given configfile)
    """
    if configfile is None:
        configfile = path.expanduser('~/.mensa.conf')
    config = SafeConfigParser()
    config.read(configfile)
    return config


if __name__ == "__main__":
    print("Hello Kitty!\n")
    CONF = parse_config()
    print_todays_menu(CONF)

#!/usr/bin/python
# coding: utf-8
"""
    Database-Module for the Mensa-Menu
"""
__author__ = 'Henning Dickten'

import sqlite3

from datetime import date

from definitions import Entry

LAYOUT = ("menu("
          "id INTEGER PRIMARY KEY AUTOINCREMENT,"
          "date DATE,"
          "counter TEXT,"
          "dish TEXT,"
          "info TEXT,"
          "price TEXT,"
          "UNIQUE (date, counter)"
          ")")


class MenuDatabase(object):
    """
    Class for the Mensa-Menu SQL-Database

    Methods:
    ========
    create_db
        creates a new table

    update_db: menu_list
        adds new entries into the db

    get_todays_menu
        returns the menu for today
    """
    def __init__(self, fname):
        "Loads the menu-database from the given filename"

        self.connection = sqlite3.connect(fname)
        self.cursor = self.connection.cursor()

    def create_db(self):
        "Creates the table"
        self.cursor.execute("CREATE TABLE " + LAYOUT + ";")

    def update_db(self, menu_list):
        "Inserts all menu entries into the table"
        self.cursor.executemany(
            "INSERT OR IGNORE INTO `menu` "
            "(`date`, `counter`, `dish`, `info`, `price`)"
            "VALUES (?, ?, ?, ?, ?)", menu_list)
        self.connection.commit()

    def get_menu(self, date_val):
        "Returns the menu for the given datetime.date object"

        try:
            self.cursor.execute(
                "SELECT * FROM menu WHERE `date` == '%s';" % date_val)
        except sqlite3.OperationalError:
            raise RuntimeError("table not found")

        # collect results:
        results = self.cursor.fetchall()

        # nothing found:
        if len(results) == 0:
            raise IndexError("date not found")

        # 'parse' results
        today = []
        for res in results:
            today.append(Entry(*res[1:]))
        return today

    def get_todays_menu(self):
        "Returns the menu for today"
        return self.get_menu(date.today())

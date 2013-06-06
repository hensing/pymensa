#!/usr/bin/python
# coding: utf-8
"""
    Basic definitions for the Mensa-Menu
"""
__author__ = 'Henning Dickten'


from collections import namedtuple


class Entry(namedtuple('entry', ['date', 'counter', 'dish', 'info', 'price'])):
    "A Mensa-Menu-Entry"

    #TODO: def __str__

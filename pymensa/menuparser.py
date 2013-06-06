#!/usr/bin/python
# coding: utf-8
"""
    Modul zum Parsen der Mensapläne
"""
__author__ = 'Henning Dickten'


import urllib2
import lxml.html

from datetime import date, timedelta

from definitions import Entry


class Parser(object):
    def __init__(self, url=None):
        """
        menu-parsen

        Parameter:
        ==========
        url: string of the location of the menu
            default=None

        """
        self.url = url
        self.the_page = None
        self.menu = None

    def _get_html(self):
        "gets the html-page as string"
        #user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
        #headers = { 'User-Agent' : user_agent }
        #req = urllib2.Request(url, '', headers)
        req = urllib2.Request(self.url)
        response = urllib2.urlopen(req)
        self.the_page = response.read()

    def parse_html(self):
        "parses the menu from html"
        if self.the_page is None:
            self._get_html()

    def get_menu(self):
        "Returns the menu"
        if self.menu is None:
            self.parse_html()
        return self.menu


class BonnVenusberg(Parser):
    def __init__(self, url=None):
        """
        Menu Parser for Mensa Bonn Venusberg

        Parameter:
        ==========
        url: string of the location of the menu
            default=None
        """
        Parser.__init__(self)
        if url is None:
            self.url = "http://bonn.my-mensa.de/essen.php?v=4568053&"\
                       "mensa=venusberg_bistro"
        else:
            self.url = url

    def parse_html(self):
        "parses the menu from html"
        self.menu = []

        Parser.parse_html(self)
        tree = lxml.html.fromstring(self.the_page)

        # get every day via <ul data-role="listview">
        for day_elem in tree.xpath("//ul[@data-role='listview']"):
            # get date via id from parent
            day_str = day_elem.getparent().getparent().get(
                'id').split('_')[-1]
            day_dtime = date(int(day_str[:4]), 1, 1) + timedelta(
                days=int(day_str[4:]))

            # get dishes (2 listitems per dish):
            for dish in day_elem.getchildren()[::2]:
                # workaround for 'Salatbuffet'
                temp_counter = dish.find('div')
                if temp_counter is None:
                    continue
                else:
                    dish_counter = temp_counter.text

                # get counter and infos:
                dish_next = dish.getnext()
                dish_name = dish_next.find('a/h3').text
                dish_info = dish_next.find("a/p[@class='ct']").text
                dish_price = dish_next.find("a/p[@class='ct next']").text

                self.menu.append(Entry(day_dtime, dish_counter,
                                       dish_name, dish_info, dish_price))


class BonnPoppelsdorf(BonnVenusberg):
    def __init__(self, url=None):
        """
        Menu Parser for Mensa Bonn Poppelsdorf

        Parameter:
        ==========
        url: string of the location of the menu
            default=None
        """
        Parser.__init__(self)
        if url is None:
            self.url = "http://bonn.my-mensa.de/essen.php?v=4568053&"\
                       "mensa=kueche_poppelsdorf"
        else:
            self.url = url


if __name__ == '__main__':
    pass

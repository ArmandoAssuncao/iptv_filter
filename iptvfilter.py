#!/usr/bin/env python
# coding: utf-8

# Define your IPTV URL in an enviroment variable named IPTV_M3U_URL
# Define your blacklist groups in an enviroment variable named BLACKLIST_GROUPS

import requests
import os
import re

#This class will handles any incoming request
class IPTVFilter():

    def __init__(self, url, blacklist_groups, separator):
        self.IPTV_M3U_URL = url
        self.blacklist_groups = blacklist_groups
        self.separator = separator

    def generate_list(self):
        self.blacklist_groups = self.blacklist_groups.replace(self.separator, '|')

        r = requests.get(self.IPTV_M3U_URL)

        list_text = r.text

        string_regex = r'(.*group-title="(?:{0})".*\n.*\n)'.format(self.blacklist_groups)
        list_regex = re.compile(string_regex, re.MULTILINE)

        new_list = list_regex.sub('', list_text)

        return new_list

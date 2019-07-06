#!/usr/bin/env python
# coding: utf-8

import os
import re
import requests

class IPTVFilter():

    def __init__(self, url, blacklist_groups, separator):
        self.IPTV_M3U_URL = url
        self.blacklist_groups = blacklist_groups
        self.separator = separator

    def __join_m3u(m3u_list):
        list_comp_path = 'storage/list_complement.m3u'
        if os.path.isfile(list_comp_path):
            list_comp_file = open(list_comp_path, 'r')
            list_comp_text = list_comp_file.read().split('\n', 1)[1]
            return m3u_list + "\n" + list_comp_text

    def generate_list(self):
        self.blacklist_groups = self.blacklist_groups.replace(self.separator, '|')

        r = requests.get(self.IPTV_M3U_URL)

        list_text = r.text
        list_text = IPTVFilter.__join_m3u(list_text)

        string_regex = r'(.*group-title="(?:{0})".*\n.*\n)'.format(self.blacklist_groups)
        list_regex = re.compile(string_regex, re.MULTILINE)

        new_list = list_regex.sub('', list_text)

        return new_list

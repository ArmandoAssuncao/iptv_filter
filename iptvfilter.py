#!/usr/bin/env python
# coding: utf-8

import os, re
from datetime import datetime, timedelta
import requests

class IPTVFilter():

    def __init__(self, url, blacklist_groups, separator):
        self.IPTV_M3U_URL = url
        self.blacklist_groups = blacklist_groups
        self.separator = separator

    def __get_list_m3u(self):
        use_cache = False
        if os.path.exists('storage/cache_time'):
            cache_time = open('storage/cache_time', 'r').read().rstrip()
            use_cache = (datetime.strptime(cache_time, '%d/%m/%Y').date() + timedelta(days=3)) >= datetime.now().date()

        list_m3u = ''
        if use_cache:
            list_m3u = open('storage/list.m3u', 'r').read()
        else:
            r = requests.get(self.IPTV_M3U_URL)
            list_m3u = r.text

            if not os.path.exists('storage'):
                os.makedirs('storage')

            file_list = open('storage/list.m3u', 'w')
            file_list.write(r.text)
            file_list.close()

            file_cache = open('storage/cache_time', 'w')
            file_cache.write(datetime.now().strftime('%d/%m/%Y'))
            file_cache.close()

        return list_m3u


    def __join_m3u(self, m3u_list):
        list_comp_path = 'storage/list_complement.m3u'
        if os.path.isfile(list_comp_path):
            list_comp_file = open(list_comp_path, 'r')
            list_comp_text = list_comp_file.read().split('\n', 1)[1]
            return m3u_list + "\n" + list_comp_text

        return m3u_list

    def generate_list(self):
        self.blacklist_groups = self.blacklist_groups.replace(self.separator, '|')

        list_text = self.__get_list_m3u()
        list_text = self.__join_m3u(list_text)

        string_regex = r'(.*group-title="(?:{0})".*\n.*\n)'.format(self.blacklist_groups)
        list_regex = re.compile(string_regex, re.MULTILINE)

        new_list = list_regex.sub('', list_text)

        return new_list

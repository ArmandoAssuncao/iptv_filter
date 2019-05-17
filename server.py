#!/usr/bin/env python
# coding: utf-8
from flask import Flask
from iptvfilter import IPTVFilter
import os

app = Flask(__name__)
IPTV_M3U_URL = os.environ['IPTV_M3U_URL']
BLACKLIST_GROUPS = os.environ['BLACKLIST_GROUPS']

@app.route("/list")
def send_file():
    iptv_filter = IPTVFilter(IPTV_M3U_URL, BLACKLIST_GROUPS)
    iptv_list = iptv_filter.generate_list()
    iptv_list = iptv_list.encode("utf-8")
    file_binary = bytearray(iptv_list)
    response = app.make_response(file_binary)
    response.headers.set('Content-type','audio/mpegurl')
    response.headers.set('Content-Disposition', 'attachment', filename='list.m3u')
    return response

if __name__ == "__main__":
    app.run()

#!/usr/bin/env python
# coding: utf-8
import os
from flask import Flask, request, Response

import importlib
dotenv_spec = importlib.util.find_spec('dotenv')
dotenv_found = dotenv_spec is not None
if dotenv_found:
  from dotenv import load_dotenv
  load_dotenv()

from iptvfilter import IPTVFilter

IPTV_M3U_URL = os.environ['IPTV_M3U_URL']
BLACKLIST_GROUPS = os.environ['BLACKLIST_GROUPS']
API_KEY = os.environ['API_KEY']
SEPARATOR = ';'
NAME_NEW_FILE = 'list.m3u'

app = Flask(__name__)

@app.route("/list")
def send_file():
    if API_KEY != request.args.get('api_key'):
        return Response('api_key unauthorized', status=403, mimetype='text/plain')

    iptv_filter = IPTVFilter(IPTV_M3U_URL, BLACKLIST_GROUPS, SEPARATOR)
    iptv_list = iptv_filter.generate_list()
    iptv_list = iptv_list.encode("utf-8")
    file_binary = bytearray(iptv_list)

    response = app.make_response(file_binary)
    response.headers.set('Content-type','audio/mpegurl')
    response.headers.set('Content-Disposition', 'attachment', filename=NAME_NEW_FILE)

    return response

if __name__ == "__main__":
    app.run()

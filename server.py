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
SECRET_KEY = os.environ['SECRET_KEY']
SEPARATOR = ';'
NAME_NEW_FILE = 'list.m3u'
NAME_FILE_COMPLEMENT = 'list_complement.m3u'
UPLOAD_LIST_COMPLEMENT_FOLDER = 'storage'
ALLOWED_EXTENSIONS = set(['m3u', 'm3u8'])

## Flask

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_LIST_COMPLEMENT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/list", methods = ["GET"])
def get_list():
    if API_KEY != request.args.get('api_key'):
        return Response('api_key unauthorized', status=403, mimetype='text/plain')

    iptv_filter = IPTVFilter(IPTV_M3U_URL, BLACKLIST_GROUPS, SEPARATOR)
    iptv_list = iptv_filter.generate_list()
    iptv_list = iptv_list.encode("utf-8")
    file_binary = bytearray(iptv_list)

    response = app.make_response(file_binary)
    response.headers.set('Content-type','plain/text')
    response.headers.set('Content-Disposition', 'attachment', filename=NAME_NEW_FILE)

    return response

@app.route("/uploadcomplementlist", methods = ["POST"])
def upload_complement_list():
    if API_KEY != request.args.get('api_key'):
        return Response('api_key unauthorized', status=403, mimetype='text/plain')

    if 'file' not in request.files:
        return Response('param "file" invalid', status=400, mimetype='text/plain')

    file = request.files['file']
    if file.filename == '':
        return Response('param "file" invalid', status=400, mimetype='text/plain')

    if file and allowed_file(file.filename):
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], NAME_FILE_COMPLEMENT))
        return Response(status=201)

    return Response('param "file" invalid', status=400, mimetype='text/plain')

if __name__ == "__main__":
    app.run()

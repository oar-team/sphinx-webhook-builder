# -*- coding: utf-8 -*-
from __future__ import with_statement, absolute_import, unicode_literals
import os
import pprint
import re
import json
import shutil
import subprocess
import requests
import ipaddress
import hmac
import contextlib
import tempfile
from hashlib import sha1

from flask import Flask, request, abort


__version__ = '0.1-dev'
VERSION = __version__


app = Flask(__name__)


if os.environ.get('USE_PROXYFIX', None):
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route("/", methods=['POST'])
def index():
    # Store the IP address blocks that github uses for hook requests.
    hook_blocks = requests.get('https://api.github.com/meta').json()['hooks']

    # Check if the POST request if from github.com
    for block in hook_blocks:
        ip = ipaddress.ip_address('%s' % request.remote_addr)
        if ip in ipaddress.ip_network(block):
            break  # the remote_addr is within the network range of github
    else:
        abort(403)

    if request.headers.get('X-GitHub-Event') == "ping":
        return json.dumps({'msg': 'Hi!'})
    if request.headers.get('X-GitHub-Event') != "push":
        return json.dumps({'msg': "wrong event type"})

    payload = json.loads(request.data)
    pprint.pprint(payload)
    # Check if POST request signature is valid
    if not app.config["SECRET_KEY"] == "":
        key = app.config["SECRET_KEY"]
        signature = request.headers.get('X-Hub-Signature').split('=')[1]
        if type(key) == unicode:
            key = key.encode()
        mac = hmac.new(key, msg=request.data, digestmod=sha1)
        if not compare_digest(mac.hexdigest(), signature):
            abort(403)

    # Try to get the branch name
    match = re.match(r"refs/heads/(?P<branch>.*)", payload['ref'])
    if match:
        branch = match.groupdict()['branch']
        if branch in app.config["BRANCHES"]:
            build_documentation(branch)
            return "Done!"
    return "Nothing to do"


def execute(*command, **kwargs):
    process = subprocess.Popen(command, cwd=kwargs.get("cwd", os.getcwd()))
    process.wait()


@contextlib.contextmanager
def make_temp_directory():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def build_documentation(branch):
    docs_src = os.path.join(app.config["REPO"], "docs")
    output = os.path.join(app.config["OUTPUT"], branch)
    with make_temp_directory() as temp_dir:
        execute("mkdir", "-p", output)
        execute("make", "html", "BUILDDIR=%s" % temp_dir, cwd=docs_src)
        execute("rsync", "-avh", "./html/", output, cwd=temp_dir)


def compare_digest(a, b):
    """
    ** From Django source **

    Run a constant time comparison against two strings
    """
    if len(a) != len(b):
        return False

    result = 0
    for ch_a, ch_b in zip(a, b):
        result |= ord(ch_a) ^ ord(ch_b)
    return result == 0

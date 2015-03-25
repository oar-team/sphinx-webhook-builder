#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, absolute_import, unicode_literals
import argparse
import os
from oar_docs_autobuilder import app


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run application ')
    parser.add_argument('-p', '--port', action="store", default=9090, type=int,
                        help='Set the listening port')
    parser.add_argument('-b', '--bind', action="store", default="0.0.0.0",
                        help='Set the binding address')
    parser.add_argument('-r', '--repo', action="store", required=True,
                        help='Set the local repository path')
    parser.add_argument('-o', '--output', action="store", required=True,
                        help='Set the local repository to save documentation')
    parser.add_argument('--branches', nargs='+', required=True,
                        help='List of branches to watch')
    parser.add_argument('--secret', action="store", default="",
                        help='Secret key')

    parser.add_argument('--debug', action="store_true", default=False,
                        help='Enable debugger')
    args = parser.parse_args()

    app.config["REPO"] = os.path.join(os.getcwd(), args.repo)
    app.config["OUTPUT"] = os.path.join(os.getcwd(), args.output)
    app.config["BRANCHES"] = args.branches
    app.config["SECRET_KEY"] = args.secret
    app.run(host=args.bind, port=args.port, processes=1, debug=args.debug)

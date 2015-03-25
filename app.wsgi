#!/usr/bin/env python
# -*- coding: utf-8 -*-
from oar_docs_autobuilder import app as application
application.config.from_envvar('SPHINX_WEBHOOK_CONFIG', silent=True)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sphinx_webhook_builder import app as application
application.config.from_envvar('SPHINX_WEBHOOK_CONFIG', silent=True)

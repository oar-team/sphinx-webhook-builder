#!/usr/bin/env python
# -*- coding: utf-8 -*-
from oar_docs_autobuilder import app as application
application.config.from_envvar('OAR_AUTODOC_CONFIG', silent=True)

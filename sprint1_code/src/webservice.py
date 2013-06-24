#!/bin/bash python
'''
Created on 19 Jun 2013

@author: evilclam
'''
import sys, os
sys.path.append('/var/www/webpy-app/')
import web
import json
import Gateway
urls = ("/gateway","Gateway.gateway")
app = web.application(urls, globals())
application = app.wsgifunc()
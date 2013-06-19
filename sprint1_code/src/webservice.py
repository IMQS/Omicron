'''
Created on 19 Jun 2013

@author: evilclam
'''
import web
import json
import Gateway

urls = ("/gateway","Gateway.gateway" )

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
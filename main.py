#!/usr/bin/env python

users = {
  'test': 'test'
}

import logging
import wsgiref.handlers
from google.appengine.api import mail
from google.appengine.ext import webapp
import os

from sys import version_info
if version_info >= (2, 5):
    from xml.etree import cElementTree as ElementTree
else:
    try:
        import cElementTree as ElementTree
    except ImportError:
        try:
            from elementtree import ElementTree
        except ImportError:
            raise Exception('ElementTree must be installed')

attributes = [
  'sender', 
  'to', 
  'cc', 
  'bcc', 
  'reply_to', 
  'subject', 
  'body', 
  'html'
]

class EmailHandler(webapp.RequestHandler):
  
  def forbidden(self):
    self.error(401)

  def post(self, *args):
    if 'HTTP_AUTHORIZATION' not in os.environ: 
      return self.forbidden()
    else: 
      auth_info = os.environ['HTTP_AUTHORIZATION'] 
      if auth_info.startswith('Basic '):
        basic_info = auth_info.lstrip('Basic ')
        u,p = basic_info.decode("base64").split(":")
        if u not in users or users[u] != p:
          return self.forbidden()
      else:
        return self.forbidden()
        
    result = {}
    
    for arg in self.request.arguments():
      name = arg[6:-1]
      if name in attributes:
        result[name] = self.request.get(arg)
    
    if 'to' not in result:
      doc = ElementTree.fromstring(self.request.body)
      for child in doc.getchildren():
        if child.tag in attributes:
          result[child.tag] = child.text
    
    mail.EmailMessage(**result).send()
    
    self.response.headers['Content-Type'] = 'application/xml'


def main():
  application = webapp.WSGIApplication([('/emails(\.xml)*', EmailHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
#!/usr/bin/env python

users = {
  'test': 'test'
}

from email_handler import EmailHandler
from email_template_handler import EmailTemplateHandler

import wsgiref.handlers
from google.appengine.ext import webapp


def main():
  application = webapp.WSGIApplication([
    ('/emails(\.xml)*', EmailHandler),
    ('/emails/template(\.xml)*', EmailTemplateHandler)
  ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
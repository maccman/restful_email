import os
from main import users
from google.appengine.ext import webapp

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

class Forbidden(Exception):
  def __init__(self):
    super(Forbidden, self).__init__()
    
class InvalidRequest(Exception):
  def __init__(self):
    super(InvalidRequest, self).__init__()

class Handler(webapp.RequestHandler):
  attributes    = []
  element_name  = None
  
  def initalize(self, *args):
    super(EmailHandler, self).__init__(*args)
    
  def handle_exception(exception, debug_mode):
    if exception.__class__ == Forbidden:
      self.error(401)
    elif exception.__class__ == InvalidRequest:
      self.error(406)
    else:
      super(self)
    
  def basicAuth(self):
    if 'HTTP_AUTHORIZATION' not in os.environ: 
      return self.forbidden()
    else: 
      auth_info = os.environ['HTTP_AUTHORIZATION'] 
      if auth_info.startswith('Basic '):
        basic_info = auth_info.lstrip('Basic ')
        u,p = basic_info.decode("base64").split(":")
        if u not in users or users[u] != p:
          raise Forbidden()
      else:
        raise Forbidden()
  
  # todo - refactor
  def paramsFromXML(self):
    result = {}
    doc = ElementTree.fromstring(self.request.body)
    for child in doc.getchildren():
      if child.tag in self.__class__.attributes:
        if child.getchildren():
          result[child.tag] = {}
          for c in child.getchildren():
            result[child.tag][c.tag] = c.text
        else:
          result[child.tag] = child.text
    return result
  
  # todo - refactor
  def paramsFromPost(self):
    result = {}
    for arg in self.request.arguments():
      name = arg[len(self.__class__.element_name):-1]
      if name in self.__class__.attributes:
        result[name] = self.request.get(arg)
    return result
  
  def params(self):
    return (self.paramsFromPost() or self.paramsFromXML())
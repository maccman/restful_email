from google.appengine.api import mail
from handler import Handler

class EmailHandler(Handler):
  element_name = 'email'
  
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
  
  def __init__(self):
    super(EmailHandler, self).__init__()

  def post(self, *args):
    self.basicAuth()
    
    result = self.params()
    mail.EmailMessage(**result).send()
    
    self.response.headers['Content-Type'] = 'application/xml'
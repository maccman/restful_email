from handler import Handler, InvalidRequest

class EmailTemplateHandler(Handler):
  element_name = 'email'
  
  attributes = [
    'dict',
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
    super(EmailTemplateHandler, self).__init__()
    
  def post(self, *args):
    self.basicAuth()
    
    result = self.params()
    
    if 'dict' not in result: 
      raise InvalidRequest()
    
    if result['body']:
      result['body'] = (result['body'] % result['dict'])
    elif result['html']:
      result['html'] = (result['html'] % result['dict'])    
    
    mail.EmailMessage(**result).send()
    
    self.response.headers['Content-Type'] = 'application/xml'
    
  
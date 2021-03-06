require 'rubygems'
require 'activeresource'

module RestfulEmail
  class Email < ActiveResource::Base
    # Attributes:
    # * sender
    # * to
    # * cc
    # * bcc
    # * reply_to
    # * subject
    # * body
    # * html
    # 
    # sender, to, subject and 
    # body/html are required
    # 
    # The sender address must be the email address of a 
    # registered administrator for the application
    
    def from=(d)
      self.sender = d
    end
  
    self.site = 'http://test:test@localhost:8080/'
  end
end
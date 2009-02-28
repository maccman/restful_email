# ActionMailer::Base.delivery_method = :restful

class ActionMailer::RestfulMailer < ActionMailer::Base
  @@email_class = RestfulEmail::Email

  def self.email_class
    @@email_class
  end

  def self.email_class=(klass)
    @@email_class = klass
  end

  def perform_delivery_restful(mail)
    mail.destinations.each do |destination|
      @@email_class.create :body => mail.encoded, :to => destination,
                           :from => mail.from.first
    end
  end
end
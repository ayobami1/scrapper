import smtplib

def send_alert1():
  
    # create an SMTP object
  s = smtplib.SMTP('smtp.gmail.com', 587)
  
  # start the TLS (Transport Layer Security) encryption
  s.starttls()
  
  # authenticate with the server
  s.login('akinloluojo1@gmail.com', 'hksaufwaboudeiob')
  
  # set the sender and recipient
  sender = 'akinloluojo1@gmail.com'
  recipient = ['akinloluojo1@gmail.com',' FabriqeLtd@hotmail.com']
  
  # create the email message
  msg = """\
  From: Python Bot !
  To: Shoab
  Subject: Stopped Please Restart Me !
  
  Hey Bro,\n this stuff have just stop now\nPlease Restsart Quickly
  """
  
  # send the email
  for i in recipient:
      s.sendmail(sender, i, msg)
  
  # close the SMTP connection
  s.quit()


def send_alert2():
  
    # create an SMTP object
  s = smtplib.SMTP('smtp.gmail.com', 587)
  
  # start the TLS (Transport Layer Security) encryption
  s.starttls()
  
  # authenticate with the server
  s.login('akinloluojo1@gmail.com', 'hksaufwaboudeiob')
  
  # set the sender and recipient
  sender = 'akinloluojo1@gmail.com'
  recipient = ['akinloluojo1@gmail.com',' FabriqeLtd@hotmail.com']
  
  # create the email message
  msg = """\
  From: Python Bot !
  To: Shoab
  Subject: Stopped Please Restart Me !
  
  Hey Bro,\nFinished !!
  """
  
  # send the email
  for i in recipient:
      s.sendmail(sender, i, msg)
  
  # close the SMTP connection
  s.quit()
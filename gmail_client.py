import smtplib
# for gmail only
from_a = "sender's id"
to_a = "receiver's id" # can be a list of ids; use for loop to send to every user
msg = "your message"

username = "sender's id"
password = "sender's password"

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(from_a,to_a,msg)
server.quit()

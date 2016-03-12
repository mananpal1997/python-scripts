from selenium import webdriver

browser = webdriver.Firefox()
browser.maximize_window()

#get any site you want
browser.get('http://mail.yahoo.com')

#inspect the login form and find ids for email and password boxes
login_id = browser.find_element_by_id('login-username')

#sends email id to the email-id box
login_id.send_keys('email-id')

pass_id = browser.find_element_by_id('login-passwd')

#sends password to the password box
pass_id.send_keys('password')

#clicks the login button
pass_id.submit()

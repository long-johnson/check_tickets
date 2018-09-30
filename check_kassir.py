# -*- coding: utf-8 -*-

"""
Checks kassir.ru every minute for fan-zone tickets availability
and sends email if they are available
"""

import selenium
import selenium.webdriver
import time
import datetime
import winsound
import smtplib
from settings import login, password, to_addr_list


def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems


def mail_myself():
    sendemail(from_addr=login,
              to_addr_list=to_addr_list,
              cc_addr_list=[],
              subject='Metallica',
              message='https://metallica.kassir.ru/koncert/metallica',
              login=login,
              password=password)


# %% MAIN

driver = selenium.webdriver.chrome.webdriver.WebDriver()

while True:
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    driver.get('https://metallica.kassir.ru/koncert/metallica')
    elements = driver.find_elements_by_class_name('col-sector')
    for element in elements:
        print(element.text.lower())
        if 'фан' in element.text.lower():
            print('FOUND!!!')
            mail_myself()
            for i in range(60):
                winsound.Beep(2000, 1000)
    print()
    time.sleep(60)
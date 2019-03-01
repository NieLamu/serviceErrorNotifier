#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 11:19
# @Author  : maxm
# @Email   : mxmxlty@gmail.com
# @File    : serviceErrorNotify.py
# @Description: init


import os
import json
import logging
import sys
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
# StreamHandler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level=logging.DEBUG)
logger.addHandler(stream_handler)


sendEmailConfig = os.path.join(os.path.dirname(__file__), 'sendEmailConfig.json')


def sendEmail(mail_content='测试', mail_title='辣鸡，又出错了...'):
    with open(sendEmailConfig, 'r') as f:
        config = json.load(f)
    #ssl登录
    smtp = SMTP_SSL(config["server"])
    #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(0)
    smtp.ehlo(config["server"])
    smtp.login(config["sender"], config["pwd"])

    msg = MIMEText(str(mail_content), "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = config["senderName"]+"<%s>"%config["sender"]
    for receiver in config["receiver"]:
        msg["To"] = receiver
        smtp.sendmail(config["sender"], receiver, msg.as_string())
    smtp.quit()


def notify(content, type=0):
    try:
        if type==1:
            sendEmail(content)
        elif type==2:
            # requests.get('http://sc.ftqq.com/SCKEY.send')
            pass
        else:
            sendEmail(content)
            # requests.get('http://sc.ftqq.com/SCKEY.send')
    except Exception as e:
        logger.info('notify error error %s', e)
        pass


if __name__ == '__main__':
    logger.info(sendEmail('hello world.'))
    pass
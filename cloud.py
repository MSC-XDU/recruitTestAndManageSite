# coding: utf-8

from leancloud import Engine,HttpsRedirectMiddleware
from app import app

app = HttpsRedirectMiddleware(app)
engine = Engine(app)


# @engine.define
# def sendemail(email,name,phone):
#     import smtplib
#     from email.mime.multipart import MIMEMultipart
#     from email.header import Header
#     me = 'noreply@dlmyb.com'
#     you = email
#     passwd = 'Rmbbkb12'
#     host = 'smtp.exmail.qq.com'
#     msg = MIMEMultipart()
#     msg['Subject'] = Header('有人过关了','utf-8')
#     msg['From'] = Header("【MSC Testing】<noreply@dlmyb.com>",'utf-8')
#     msg['To'] = Header(you,'utf-8')
#     data = "email:%s\nname:%s\nphone:%s"%(email,name,phone)
#     msg.attach(MIMEText(data,'plain','utf-8'))
#     s = smtplib.SMTP_SSL()
#     s.connect(host,465)
#     s.login(me,passwd)
#     s.sendmail(me,you,msg.as_string())
#     s.quit()
#     return 200

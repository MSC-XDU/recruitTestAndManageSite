# coding: utf-8

from __future__ import unicode_literals
from leancloud import Engine,HttpsRedirectMiddleware
import leancloud
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

@engine.after_save('SignUp')
def reindex():
    field = ['活动部','联络部','传媒部-平面设计组','传媒部-影像视讯组','技术部-ACM组','技术部-APP组','技术部-Game组','技术部-实用工具组','技术部-Web组']
    result = {}
    for i in field:
        maleNum = leancloud.Query.do_cloud_query(
            """select count(*) from SignUp where sex='男' and department='%s'"""%i
        ).count
        femaleNum = leancloud.Query.do_cloud_query(
            """select count(*) from SignUp where sex='女' and department='%s'"""%i
        ).count
        result[i] = [maleNum,femaleNum,maleNum+femaleNum]
    maleNum = femaleNum = all = 0
    for i in field:
        maleNum += result[i][0]
        femaleNum += result[i][1]
        all += result[i][2]
        result['all'] = [maleNum,femaleNum,all]
    # id is 57cd03472e958a0068e6d0a5
    I = leancloud.Query('index')
    i = I.get('57cd03472e958a0068e6d0a5')
    i.set('result',result)
    i.save()


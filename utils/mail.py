# coding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from config.configData import EMAIL_HOST, EMAIL_USER, EMAIL_PASSWD
# 第三方 SMTP 服务
mail_host = EMAIL_HOST  # 设置服务器
mail_user = EMAIL_USER  # 用户名
mail_pass = EMAIL_PASSWD  # 口令


def SendMail(From, To, Title, mail_msg):
    # @
    #    From：发件人
    #    To：收件人
    #    Title：邮件标题
    #    mail_msg：邮件内容（可以是html，或文本）

    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header(From, 'utf-8')
    message['To'] = Header(To, 'utf-8')

    #     subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(Title, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(From, To, message.as_string())
        print("邮件发送成功".encode('utf-8'))
    except smtplib.SMTPException:
        print("Error: 无法发送邮件".encode('utf-8'))


if __name__ == '__main__':
    mail_msg = \
        """
        <p>Python 邮件发送测试...</p>
        <p><a href="http://www.runoob.com">这是一个链接</a></p>
    """
    #     with open('sample.html', 'r') as newF:
    #         mail_msg = newF.read();
    #     newF.close();
    SendMail(EMAIL_HOST, "majunfeng@sogou-inc.com", "我来测试一下发邮件的方法", mail_msg)

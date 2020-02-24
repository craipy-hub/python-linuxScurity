import zmail
# 配置邮件服务器
server = zmail.server('Today_News@163.com','447621smtp')

mail_content = {
    'subject':'test'+'Report',
    'content_text':'',
    'attachments':[]
}

# server.send_mail(['cpy_3566@163.com'], mail_content)
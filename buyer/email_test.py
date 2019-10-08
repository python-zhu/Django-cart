import smtplib
from email.mime.text import MIMEText

msg = MIMEText('womenshimeinv', 'plain', 'utf-8')
msg['subject']='无名小子'
msg['to']='python_hh@163.com'
msg['from'] = 'gjmnaozibuhao@163.com'

# 3. 实例化服务器（登录）
smtp = smtplib.SMTP_SSL('smtp.163.com', 994)  # 设置url 和 端口号
smtp.login('gjmnaozibuhao@163.com', 'admin123')  # user:邮箱账号，passsword :授权码

# 4. 发送邮件
smtp.sendmail('gjmnaozibuhao@163.com', ['python_hh@163.com'], msg.as_string())

# 5. 关闭
smtp.close()

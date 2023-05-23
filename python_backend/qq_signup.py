import smtplib
from email.mime.text import MIMEText
import random

# 生成一个6位数的验证码
verification_code = str(random.randint(100000, 999999))

# QQ邮箱的SMTP服务器地址
smtp_server = 'smtp.qq.com'

# 你的QQ邮箱地址
from_addr = '1946605630@qq.com'

# 你的QQ邮箱SMTP授权码
password = 'fclwiymyqesrbebi'

# 收件人邮箱地址
to_addr = '3315288091@qq.com'

# 邮件内容
content = '''
Hello,

Thank you for registering at Word Journeyman.

Your verification code is: {}

Please enter this code on the Word Journeyman website to complete your registration.

If you did not request this code, please ignore this email.

Best regards,
The Word Journeyman Team
'''.format(verification_code)

# 创建MIMEText对象
msg = MIMEText(content, 'plain', 'utf-8')

# 设置邮件主题
msg['Subject'] = 'Word Journeyman Registration Verification Code'

# 设置发件人
msg['From'] = from_addr

# 设置收件人
msg['To'] = to_addr

# 创建SMTP服务器对象
server = smtplib.SMTP_SSL(smtp_server)

# 登录SMTP服务器
server.login(from_addr, password)

# 发送邮件
server.sendmail(from_addr, [to_addr], msg.as_string())

# 关闭服务器连接
server.quit()

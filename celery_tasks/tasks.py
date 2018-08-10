from django.conf import settings

# 这两行代码在启动worker进行的一端打开
# 设置django配置依赖的环境变量
import os
from fushentang.settings import app
from goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner
import logging


logger = logging.getLogger("task")
# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    # 组织邮件内容
    import smtplib
    from smtplib import SMTP_SSL
    from email.mime.text import MIMEText
    from email.header import Header

    mail_host = "smtp.qq.com"
    mail_user = "893177204@qq.com"
    mail_pass = "nyeuzvnpbfxwbbjg"  # nyeuzvnpbfxwbbjg
    receivers = to_email
    mail_msg = """
    <h1>%s, 欢迎您成为福参堂注册会员</h1>
        请点击以下链接激活您的账户(7个小时内有效)<br/>
        <a href="http://www.dongpouu.com/user/active/%s">http://www.dongpouu.com/user/active/%s</a>
                     """ % (username, token, token)
    logger.info("task正在发送激活邮件")

    message = MIMEText(mail_msg, 'html', 'utf-8')
    # message = MIMEText("welcome", 'plain', 'utf-8')
    subject = u'福参堂欢迎信息'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = SMTP_SSL(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())

        logger.info("邮件发送成功")
    except smtplib.SMTPException:

        logger.info("Error: 无法发送邮件")
    finally:
        smtpObj.quit()



@app.task
def generate_static_index_html():
    """使用celery生成静态首页文件"""
    # 获取商品的分类信息
    types = GoodsType.objects.all()

    # 获取首页的轮播商品的信息
    index_banner = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页的促销活动的信息
    promotion_banner = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品的展示信息
    for category in types:
        # 获取type种类在首页展示的图片商品的信息和文字商品的信息
        image_banner = IndexTypeGoodsBanner.objects.filter(type=category, display_type=1)
        title_banner = IndexTypeGoodsBanner.objects.filter(type=category, display_type=0)

        # 给category对象增加属性title_banner,image_banner
        # 分别保存category种类在首页展示的文字商品和图片商品的信息
        category.title_banner = title_banner
        category.image_banner = image_banner

    cart_count = 0

    # 组织模板上下文
    context = {
        'types': types,
        'index_banner': index_banner,
        'promotion_banner': promotion_banner,
        'cart_count': cart_count,
    }

    # 使用模板

    # 1.加载模板文件
    from django.template import loader
    temp = loader.get_template('static_index.html')
    # 2.模板渲染
    static_html = temp.render(context)
    # 3.生成静态首页文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w') as f:
        f.write(static_html)








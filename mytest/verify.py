from PIL import Image, ImageDraw, ImageFont
import random, string, io
from django.shortcuts import HttpResponse, render


# 返回随机色
def rndColor():
    c1 = random.randrange(0, 220)
    c2 = random.randrange(0, 220)
    c3 = random.randrange(0, 220)
    return (c1, c2, c3)


def verifycode(request):
    '''在django中用于生成随机验证码，返回验证码图片并将随机字符保存进session'''
    # 得到4位随机码
    base_str = string.ascii_letters + string.digits
    rnd_list = random.sample(base_str, 4)
    rnd_str = ''.join(rnd_list)

    # 保存验证码到session
    request.session['verifycode'] = rnd_str.lower()

    # 创建图片对象
    bgcolor = 'lightgray'
    width, height = 100, 25
    img = Image.new('RGB', (width, height), bgcolor)

    # 关联字体文件，设置字体大小
    font = ImageFont.truetype('/usr/share/fonts/truetype/fonts-japanese-gothic.ttf', 22)
    # 创建画笔对象并书写验证码
    draw = ImageDraw.Draw(img)
    font_color = rndColor()
    draw.text((20, 2), rnd_str, fill=font_color, font=font)

    # 随机生成100个散点
    for i in range(100):
        xy = (random.randint(0, width), random.randint(0, height))
        draw.point(xy, fill=rndColor())

    # 生成随机直线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line(xy=(x1, y1, x2, y2), fill=rndColor(), width=1)

    # 生成随机圆
    for i in range(5):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 5, y + 5), 0, 360, fill=rndColor())

    # 开辟二进制内存空间，存储图片
    buf = io.BytesIO()
    img.save(buf, 'png')

    return HttpResponse(buf.getvalue())
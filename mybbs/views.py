from django.shortcuts import render,HttpResponse

# Create your views here.

from django.contrib import auth
def login(request):

    if request.is_ajax():
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')
        code=request.POST.get('code')

        if code.upper()== request.session['code'].upper():
            user=auth.authenticate(request,username=name,password=pwd)
            if user:
                return HttpResponse('ok')
            else:
                return HttpResponse('用户名或密码错误')
        else:
            return HttpResponse('验证码错误')


    return render(request,'login.html')

def get_random_color():
    import random
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))


def get_code(request):
    import random
    # with open('static/img/lhf.jpg','rb') as f:
    #     data=f.read()
    # pip3 install pillow
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    import random
    img = Image.new("RGB", (270, 40), color=get_random_color())

    draw = ImageDraw.Draw(img)
    kumo_font = ImageFont.truetype("static/font/kumo.ttf", size=32)

    valid_code_str = ""
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(95, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((i * 50 + 20, 5), random_char, get_random_color(), font=kumo_font)

        # 保存验证码字符串
        valid_code_str += random_char

    print("valid_code_str", valid_code_str)
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    request.session['code']=valid_code_str

    return HttpResponse(data)
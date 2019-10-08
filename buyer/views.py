from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from seller import models as s1
from seller import views as s1_view
from buyer import models as b1


# Create your views here.
def index(request):
    queryset_obj = s1.Goods.objects.all()
    return render(request, 'buyer/index.html', locals())


def goods_detail(request):
    goods_id = request.GET.get('id')
    # 查询数据库
    goods_obj = s1.Goods.objects.get(id=goods_id)
    seller_id = goods_obj.seller_id
    queryset_obj = s1.Goods.objects.filter(seller_id=seller_id)
    return render(request, 'buyer/goods_details.html', {'goods_obj': goods_obj, 'queryset_obj': queryset_obj})

    # 查询数据库


def register_ajax(request):
    dic = {'status': 'false'}
    username = request.GET.get('username')
    queryset_obj = b1.Buyer.objects.filter(name=username)
    if queryset_obj:
        dic['status'] = 'true'

    return JsonResponse(dic)


def register(request):
    nickname = ''
    username = ''
    error_msg = ''
    if request.method == 'POST':
        # 1. 获取表单提交过来的内容
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        userpass = request.POST.get('userpass')
        buyer_obj = b1.Buyer.objects.filter(name=username).first()
        if not buyer_obj:
            # 2. 对密码加密
            pwd = s1_view.pwd_jm(userpass)
            # 3. 保存数据库
            b1.Buyer.objects.create(
                name=username,
                nickname=nickname,
                password=pwd
            )
            # 4. 重定向到登录界面
            return redirect('/buyer/login/')
        error_msg = '为啥不该呢'
    return render(request, 'buyer/register.html', locals())


# 登录
def login(request):
    if request.method == 'POST':
        # 1.获取表单提交过来的 内容
        username = request.POST.get('username')
        userpass = request.POST.get('userpass')
        # 2. 对密码进行加密
        password = s1_view.pwd_jm(userpass)
        # 3. 查询数据库
        buyer_obj = b1.Buyer.objects.filter(name=username, password=password).first()
        if buyer_obj:
            """登录成功"""
            # 将用户名保存到session中
            # request.session['buyer_name'] = buyer_obj.name
            # request.session['buyer_pwd'] = buyer_obj.password
            # # 4. 重定向到首页
            # return redirect('/buyer/index/')
            goods_id = request.COOKIES.get('goods_id')
            if goods_id:
                """如果goods_id 存在 表示 从购物车中间页跳转过来的"""
                response = redirect('/buyer/car_jump/')
                response.set_cookie('buyer_name', buyer_obj.name)
                response.set_cookie('buyer_id', buyer_obj.id)
                return response
            else:
                # 将用户名保存到cookie中
                response = redirect('/buyer/index/')
                response.set_cookie('buyer_name', buyer_obj.name)
                response.set_cookie('buyer_id', buyer_obj.id)
                return response
    else:
            return render(request, 'buyer/login.html', {'error_msg': '用户名或者密码错误'})
    return render(request, 'buyer/login.html')


# 登出
def logout(request):
    response = redirect('/buyer/login/')
    # 删除cookie
    # response.delete_cookie('buyer_name') # 将 max_age=0
    # 第二种方式：通过设置cooKie 的过期时间
    response.set_cookie('buyer_name', max_age=0)
    response.set_cookie('buyer_id', max_age=0)
    # 2. 重定向到登录界面
    return response


"""
使用session ：
1.将用户名和密码保存到session中
2.再次访问首页的时候，从session获取出来

"""
"""
需求：登录成功后，显示 用户名 并且将登录和注册按钮隐藏
 - 使用cookie 
    - 登录成功后，将用户名保存到cookie中。
    - 页面上使用cookie 进行判断。
 - 使用session
     - 登录成功后，将用户名保存到session中。
     - 页面上使用session 进行判断。

登出操作：
 - 使用session : del flush ,clear 
 - 使用cookie : 
    - response.delete_cookie(key)
    - response.set_cookie(key,max_age=0) 使用过期时间来删除cookie

15天免登陆（参考京东）：
 - 使用session 实现。
  用户登录成功后，将用户名和密码设置在session中。
  重新会话的时候，根据session 是否过期，来显示用户名。
"""


# 用户地址展示
def address_list(request):
    queryset_obj = b1.Address.objects.all()

    return render(request, 'buyer/address_list.html', locals())


# 地址新增
def address_add(request):
    if request.method == 'POST':
        buyer_name = request.POST.get('buyer_name')
        buyer_phone = request.POST.get('buyer_phone')
        buyer_address = request.POST.get('buyer_address')
        b1.Address.objects.create(
            receiver=buyer_name,
            phone=buyer_phone,
            address=buyer_address,
            buyer_id=request.COOKIES.get('buyer_id')
        )
        return redirect('/buyer/address_list/')
    return render(request, 'buyer/address_add.html')


# 用户地址删除
def address_delete(request):
    id = request.GET.get('id')
    b1.Address.objects.get(id=id).delete()
    return redirect('/buyer/address_list/')


# 用户地址修改
def address_update(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        address_obj = b1.Address.objects.get(id=id)
        return render(request, 'buyer/address_change.html', {'address_obj': address_obj})
    else:
        '''POST'''
    id = request.POST.get('id')
    buyer_name = request.POST.get('buyer_name')
    buyer_phone = request.POST.get('buyer_phone')
    buyer_address = request.POST.get('buyer_address')
    address_obj = b1.Address.objects.get(id=id)
    address_obj.receiver = buyer_name
    address_obj.phone = buyer_phone
    address_obj.address = buyer_address
    address_obj.save()
    return redirect('/buyer/address_list/')


# 购物车中间页
def car_jump(request):
    buyer_id = request.COOKIES.get('buyer_id')
    if buyer_id:

        if request.method == 'GET':
            # 1.从cookie 中获取 商品id 和数量
            goods_id = request.COOKIES.get('goods_id')
            count = request.COOKIES.get('count')
            # 2. 查询数据库（商品数据库）将信息返回给页面
            goods_obj = s1.Goods.objects.get(id=goods_id)
            goods_name = goods_obj.goods_name
            goods_img_path = goods_obj.goodsimage_set.first().image_address
            goods_price = goods_obj.goods_cprice  # 现价
            all_goods_price = int(goods_price) * int(count)  # 小计
            # 3.保存数据库
            buyer_car_obj = b1.BuyerCar.objects.filter(goods_id=goods_id, buyer_id=buyer_id).first()
            # 先判断数据库中购物车表中是否存在此商品，如果存在则修改数量，否则保存此商品到数据库
            if buyer_car_obj:
                """数据库中存在"""
                buyer_car_obj.goods_num += int(count)  # 修改数量
                buyer_car_obj.save()
            else:
                """数据库中没有"""
                b1.BuyerCar.objects.create(
                    goods_id=goods_id,
                    goods_name=goods_name,
                    goods_picture=goods_img_path,
                    goods_price=goods_price,
                    goods_num=count,
                    buyer_id=buyer_id
                )

            # 删除cookie
            response = render(request, 'buyer/car_jump.html', locals())
            response.delete_cookie('goods_id')
            response.delete_cookie('count')
            # 页面上展示
            return response
        else:
            """POST提交"""
            # 1.获取表单提交过来的内容
            goods_id = request.GET.get('id')  # 商品id
            count = request.POST.get('count')  # 商品数量
            goods_name = request.POST.get('goods_name')  # 商品名称
            goods_price = request.POST.get('goods_cprice')  # 商品现价
            goods_img_path = request.POST.get('goods_img_path')  # 商品图片路径
            all_goods_price = int(goods_price) * int(count)  # 小计
            # 2.查询此商品数据库，如果存在 则 修改数量，否则 保存此商品
            buyer_car_obj = b1.BuyerCar.objects.filter(goods_id=goods_id, buyer_id=buyer_id).first()
            if buyer_car_obj:
                """数据库中存在"""
                buyer_car_obj.goods_num += int(count)  # 修改数量
                buyer_car_obj.save()
            else:
                """数据库中没有"""
                b1.BuyerCar.objects.create(
                    goods_id=goods_id,
                    goods_name=goods_name,
                    goods_picture=goods_img_path,
                    goods_price=goods_price,
                    goods_num=count,
                    buyer_id=buyer_id
                )
            # 3.返回页面
            return render(request, 'buyer/car_jump.html', locals())
    else:
        # 用户没有登录--> 跳转登录界面，登录成功后再跳转到购物车中间页。
        # 1.先将表单提交过来的内容
        goods_id = request.GET.get('id')  # 注意获取id 我们通过 get 方式
        count = request.POST.get('count')  # 商品数量
        response = redirect('/buyer/login/')
        response.set_cookie('goods_id', goods_id)
        response.set_cookie('count', count)
        # 3.在跳转到登录界面
        return response


def car_list(request):
    # 获取当前用户id
    buyer_id = request.COOKIES.get('buyer_id')
    # 获取当前用户购物车全部数据
    buycar_obj_list = b1.BuyerCar.objects.filter(buyer_id=buyer_id)
    new_list = []
    total_price = 0
    for buycar_obj in buycar_obj_list:
        dic = {}
        dic['buycar_obj'] = buycar_obj
        xiaoji = int(buycar_obj.goods_price * buycar_obj.goods_num)
        dic['xiaoji'] = xiaoji
        new_list.append(dic)
        total_price += xiaoji
    # 查询用户地址
    address_obj_list = b1.Address.objects.filter(buyer_id=buyer_id)
    # 返回页面
    return render(request, 'buyer/car_list.html', locals())


# 清空购物车


def car_delete(request):
    # 1.查询当前用户
    buyer_id = request.COOKIES.get('buyer_id')
    # 2.删除数据库
    b1.BuyerCar.objects.filter(buyer_id=buyer_id).delete()
    # 3.重定向到购物车列表页面
    return redirect('/buyer/car_list/')


# 删除购物车中的某一件商品
def car_goods_delete(request):
    # 1. 获取 购物车id
    buycar_id = request.GET.get('id')
    # 2. 查询数据库并且删除
    b1.BuyerCar.objects.get(id=buycar_id).delete()
    # 3. 重定向到购物车列表页面
    return redirect('/buyer/car_list/')


# 立即下单
import datetime
import random


def get_random():
    return random.randint(100000, 999999)


def enter_order(request):
    # num = 1
    if request.method == 'POST':
        # 1. 获取地址
        address_id = request.POST.get('address')
        address_obj = b1.Address.objects.get(id=address_id)

        # 2.发货时间
        times = datetime.datetime.now()

        # ret = times.strftime('%Y%m%d%H%M%S')
        # print(ret) 20190827111601

        total_price = 0  # 商品总计
        new_goods_list = []  # 保存购物车 # [{buyercar_obj:'',xiaoji:''},{}]
        # 3. 获取 checkbox
        for key, value in request.POST.items():
            print(key, '--->>', value)
            if key.startswith('name'):
                dic = {}
                buyercar_obj = b1.BuyerCar.objects.get(id=value)
                # 计算商品小计
                xiaoji = int(buyercar_obj.goods_price) * int(buyercar_obj.goods_num)
                dic['buyercar_obj'] = buyercar_obj
                dic['xiaoji'] = xiaoji
                new_goods_list.append(dic)
                total_price += xiaoji

        # 4. 创建订单表
        order_obj = b1.Order.objects.create(
            order_num=str(times.strftime('%Y%m%d%H%M%S')) + str(get_random()),  # 订单号 日期+随机数
            order_time=times,
            order_status='1',  # 订单状态 0 表示未付款，1表示付款了
            order_total=total_price,  # 商品总价
            buyer_id=request.COOKIES.get('buyer_id'),
            address=address_obj
        )
        # 5. 创建订单商品详情表
        for goods_obj_dic in new_goods_list:
            buyercar_obj = goods_obj_dic.get('buyercar_obj')
            b1.OrderGoods.objects.create(
                goods_id=buyercar_obj.goods_id,
                goods_name=buyercar_obj.goods_name,
                goods_picture=buyercar_obj.goods_picture,
                goods_price=buyercar_obj.goods_price,
                goods_num=buyercar_obj.goods_num,
                order=order_obj
            )
    return render(request, 'buyer/enter_order.html', locals())


from alipay import AliPay


def alipay_method(request):
    order_num = request.GET.get('order_num')
    total = request.GET.get('total')
    # 商家的私钥
    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEogIBAAKCAQEAu2H8+A/zPsPJhd8NfO3TmSxHxxRTnTndtRZKvvBse/Tqic0RAN75kQZyiR3yCAoVSaGABcKsTBeaxBjw5DgLmYUCo2Z8bqR460Gqht44IsMBJtftTqJiO/X7FVQiI4cMFebeEeROi7DZ6z+oSs+USV99MGs2054w2MHRZMxqIQHYTYUkLFH3saEnKPaIxPfP+eAZruf+H6E/LmdkVIr/EWmk3UZ5txdA47S3eDbPuCylm6gG+0xWJfQj7F6chyqEUzQsFdGNrLmWsfYzCFYDxb3Jbq8LdeKFisZVGp2JUrZW+HVumeTdo/MFN4A6GbBx+t0gWpl+q3wkrbK4zOPj4wIDAQABAoIBAE/eXlLliYqxLQ5wmnErdcuOAjIqydD0PznWfJmSJMtZAzclPyAd6kYUd3FWYDlpAtXVjpnl9kagsQjwkIzWDquq9Artvg/y7s9nt+WwhkDa2XzTAIVJ1ZE1MYZPzBVUlKQpOXJq28fS46/P/E2W2N/FYbjnmgDtJmjdhADw2DOkt/ZKibjdvbrmQo4I4ybke9C1AzTcOpLFe/B/EkFyaiDsRMS7AV0VkkjEOTEX2PetRnW+SulIczV4c6IQ29fCncBE9goZNpKsKGmaCME/u5oSL5Negm/D6NuT9kT7wUQyhuUZ1Vg9yFHycbEjHcHp1LkyLjALF2LlJoXAYwhv8HECgYEA8t6RGzFXIi1WtY3RNpVArU7SYYIhkq5c3xhZUUPeAMEOJzVDLqlswmtGDowbPRyRF1AGcrqABGgz07KAB4hHPaQpXb/Wy1tmLzZbmI7gBDF8uzNtD8KQTTaEJePQIlQ0JLsZzSfCa4yYvdLa/9867zkD3ujkVkvMeBdkr5OGeD8CgYEAxYN1b+cZDY+LetKh7bDh8f51/lIidFKjkbiWKOiQ4XhiVJJxGdIyyyyCXSNzlmyzo4eBPavTl2RPKKrhjVjJdIQqEoJ9LnWXjz2OcrUP5gMXTjjIVgEpMbeTT0M/WdWeYEkLjCpPv+ZjnJJLm/LeuzNst6nkc5iE77xrr15Ai10CgYBrj9jSI0ME1vGdDMcIloeDefJAzyJRVTm6cI02KYmL6fR7tuIfK1gIrvvi+3gg06MKoR2J+EE0MnYpnteG/nsWuLq9U3YssDkMVdWxNi3OjaBBRGBb536DQ864/TEz0vkY/2hI7P/1I9qNz3HAerweMLEfKyPdeEqBMVMdU4ftfwKBgFDae5yPccYHWQWya+8tVZEGpa6yWMBdg/AHLBEbAxQJf9c3C22SipB5a/RMquiNHwx2UAW67ScwPOdc7HA8RFuaLs7c8/ms0ZoljMaQMC3sXgH7ZKcwWniruXXdBXX06JxpynxaZcMcwPI7QRBZ36uqZXrZ5VccvG6XJ03mu21RAoGAeaSqeWX0wA8yg/UIyeFazlgp5Gtnfp3JBCdxs0jAFk8qGOLb8N2toNCq5SjEyXC2o6Me2dTyQWDGAb+f20UrTvdwq+StzCltKMoEsJpQ2VzctzdCXaMNPZjdazkTWp5kj1gj2+kmE9grdogh3sIGyey++NRZ5rdNfeGATGmetKY=
    -----END RSA PRIVATE KEY-----"""
    # 支付宝的公钥
    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgQF31qv8cn5Kqhm7NTdnOpA3YSj8lwgy39eqlCQOF946WoAWXy0B0b1eaWH3dzGwh6rMl57HwproaOCnSg2wKrcL0jxrPKqAnUyVmewFdjUrP83+WSG0hW1TWeRwXY1rcU39xeLGm6HZN2KLfPPNENt5G9ha0OhGDYtolSZ0AXZAhx+9EGdRpNly960uw2hmo3E6H2EZabUDYM6oLdKzCTJ8tfd7nRlLiyvchCNA8rbnswB0gA1lM8FeV6AER12W+a+ksL+aqg4/4DMbymt5/eJj9r8Wr+Iwe/STQjMDq9pBoSnBeS2SkxQ3z36zkP7TRCNZsKEwSFropS+gHsHbpQIDAQAB
    -----END PUBLIC KEY-----"""
    # 初始化操作
    alipay = AliPay(
        appid="2016101300679714",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
        debug=True
    )

    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=str(order_num),  # 订单号
        total_amount=str(total),  # 总额  注意使用 字符串!!!
        subject="中公水果超市",
        return_url='/buyer/car_list/',
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    # https: // openapi.alipaydev.com / gateway.do? + order_string
    return redirect('https://openapi.alipaydev.com/gateway.do?' + order_string)


from django.core.mail import EmailMultiAlternatives


# 邮箱注册，点击获取验证码发送的ajax
def send_message(request):
    dic = {'status': 'error', 'data': ''}
    # 1.获取邮箱
    email = request.GET.get('email')
    print(email)
    try:
        # 2.生成验证码并发送邮件
        # (1).在settings.py中配置邮箱信息
        # (2).生成邮件并且发送
        subject = '中公水果商城'  # 主题
        body_yzm = str(get_random())  # 生成四位随机数验证码,并且转换成字符串类型
        print(body_yzm)
        msg = EmailMultiAlternatives(subject, body_yzm, 'gjmnaozibuhao@163.com', [email])
        msg.send()
        print(body_yzm)
    except Exception as e:
        print(e)
        dic['status'] = 'error'
        dic['data'] = 'error'
    else:
        dic['status'] = 'success'
        dic['data'] = 'success'
        b1.EmailValid.objects.create(
            email_name=email,
            value=body_yzm,
            time=datetime.datetime.now()
        )
    finally:
        return JsonResponse(dic)


def register_email(request):
    dic = {}
    if request.method=="POST":
        #获取表单提交过来的内容
        emailname=request.POST.get('emailname')
        code = request.POST.get('code')
        userpass = request.POST.get('userpass')
        email_obj = b1.EmailValid.objects.filter(email_name=enumerate).last()
        #判断邮箱是否存在
        if email_obj:
            db_code = email_obj.value
            #判断验证码是否正确


        #不存在
        else:
            pass


    return render(request, 'buyer/register_email.html')

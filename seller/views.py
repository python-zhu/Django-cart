from django.shortcuts import render, redirect, HttpResponse
from seller import models
from django import forms
import hashlib
import datetime
from django.forms import widgets


# Create your views here.
def pwd_jm(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


# def register(request):
#     if request.method == 'POST':
#         # 1.获取表单提交过来的信息
#         name = request.POST.get('username')
#         nickname = request.POST.get('nickname')
#         password = request.POST.get('password')
#         picture = request.FILES.get('picture')
#         password = pwd_jm(password)
#         # 2.保存图片
#         path = 'static/touxiang/' + picture.name
#         with open(path, mode='wb') as f:
#             for pic in picture.chunks():
#                 f.write(pic)
#         # 3.保存数据库
#         seller_obj = models.Seller()
#         seller_obj.name = name
#         seller_obj.nickname = nickname
#         seller_obj.password = password
#         seller_obj.picture = 'touxiang/' + picture.name
#         seller_obj.save()
#         # 4.重定向
#         return redirect('/seller/login/')
#     return render(request, 'seller/register.html')
# 登录装饰器
def login_decorator(func):
    def inner(request):
        username = request.session.get('username')
        if username:
            return func(request)
        else:
            return redirect('/seller/login')

    return inner


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3,
                               widget=widgets.TextInput(attrs={'placeholder': '用户名', 'class': 'layui-input'})
                               )
    nickname = forms.CharField(min_length=3,
                               widget=widgets.TextInput(attrs={'placeholder': '昵称', 'class': 'layui-input'})
                               )
    password = forms.CharField(min_length=6,
                               widget=widgets.PasswordInput(attrs={'placeholder': '密码', 'class': 'layui-input'})
                               )
    picture = forms.CharField(
        widget=widgets.FileInput(attrs={'placeholder': '头像', 'class': 'layui-input'})
    )


def register_ajax(request):
    dic = {'status': 'false'}
    name = request.GET.get('name')
    ret = models.Seller.objects.filter(name=name)
    if ret:
        dic['status'] = 'true'
    return JsonResponse(dic)


def register1(request):
    registerform = RegisterForm()
    if request.method == 'POST':
        registerform = RegisterForm(request.POST, request.FILES)
        if registerform.is_valid():
            data = registerform.cleaned_data
            username = data.get('username')
            nickname = data.get('nickname')
            password = data.get('password')
            picture = request.FILES.get('picture')
            password = pwd_jm(password)
            path = 'static/zixuantouxiang/' + picture.name
            with open(path, mode='wb') as f:
                for pic in picture.chunks():
                    f.write(pic)
            # 3.保存数据库
            seller_obj = models.Seller()
            seller_obj.name = username
            seller_obj.nickname = nickname
            seller_obj.password = password
            seller_obj.picture = 'touxiang/' + picture.name
            seller_obj.save()
            models.TouXiang.objects.create(name='zixuantouxiang/' + picture.name)  # 新建用户头像保存在自选头像相册中  可换头像
            # 4.重定向
            return redirect('/seller/login/')
    return render(request, 'seller/register1.html', {'registerform': registerform})


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3,
                               widget=widgets.TextInput(attrs={'placeholder': '用户名', 'class': 'layui-input'})
                               )
    password = forms.CharField(min_length=6,
                               widget=widgets.PasswordInput(attrs={'placeholder': '密码', 'class': 'layui-input'})
                               )


# 登录
def login(request):
    loginform = LoginForm()
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            data = loginform.cleaned_data
            username = data.get('username')
            password = data.get('password')
            password = pwd_jm(password)
            ret = models.Seller.objects.filter(name=username, password=password)
            if ret:
                # 登录后将用户名保存到session
                request.session['username'] = username
                request.session['seller_id'] = ret[0].id
                request.session['password'] = password
                return redirect('/seller/index/')
    return render(request, 'seller/login.html', locals())


from django.db.models.fields.files import ImageFieldFile


# 首页
# @login_decorator
def index(request):
    times = datetime.datetime.now()
    # 获取头像
    id = request.session.get('seller_id')
    seller_obj = models.Seller.objects.get(id=id)
    return render(request, 'seller/index.html', {'seller_obj': seller_obj, 'times': times})


# 退出
# @login_decorator
def logout(request):
    # 清除session
    request.session.clear()
    # 重定向到登录界面
    return redirect('/seller/login')


from django.http import JsonResponse
# def type_add_ajax(request):
#     dic = {'status':'false'}
#     name=request.GET.get('name')
#     ret = models.Goods_Type.objects.filter(name=name)
#     if ret:
#         dic['status']='true'
#     return JsonResponse(dic)
#
# def type_add(request):
#     msg=''
#     type_name=''
#     if request.method=='POST':
#         type_name= request.POST.get('type_name')
#         if type_name:
#             ret = models.Goods_Type.objects.filter(name=type_name)
#             if not ret:
#                 models.Goods_Type.objects.create(
#                     name=type_name
#                 )
#                 return HttpResponse('添加成功')
#             else:
#                 msg='该商品类型已存在！'
#
#     return render(request,'seller/type_add.html',{'msg':msg,'type_name':type_name})
from django.core.paginator import Paginator, EmptyPage


# 商品类型展示
def type_list(request):
    goods_type_obj_list = models.Goods_Type.objects.all()
    my_num = 5
    paginator = Paginator(goods_type_obj_list, my_num)
    num_pages = paginator.num_pages  # 总共页码数
    count = paginator.count  # 总记录数
    try:
        current_num = None
        current_num = int(request.GET.get('page', 1))
        page_obj = paginator.page(current_num)
    except Exception:
        if current_num:
            if num_pages < current_num:
                current_num = num_pages
                page_obj = paginator.page(current_num)
        else:
            current_num = 1
            page_obj = paginator.page(1)

    # 2. 返回
    return render(request, 'seller/type_list.html', locals())


# 商品类型修改
def type_change(request):
    if request.method == 'POST':
        # 1. 获取 商品id 和修改过的 商品类型名称
        id = request.POST.get('id')
        type_name = request.POST.get('type_name')
        qureset_obj = models.Goods_Type.objects.filter(name=type_name)
        if not qureset_obj:
            # 2. 根据id 查找 数据库中原来的商品
            goods_type_obj = models.Goods_Type.objects.get(id=id)
            # 3.修改商品，并保存数据库
            goods_type_obj.name = type_name
            goods_type_obj.save()
            # 4. 响应-->>重定向到商品类型列表
            return redirect('/seller/type_list/')
        goods_type_obj = qureset_obj[0]
        return render(request, 'seller/type_change.html', {'goods_type_obj': goods_type_obj, 'error': '该商品类型已存在！'})

    else:
        """get 请求"""
        # 1. 获取商品类型的id
        id = request.GET.get('id')
        # 2. 根据id查询数据库
        goods_type_obj = models.Goods_Type.objects.get(id=id)
        # 3. 响应 --> 将数据放到页面上
        return render(request, 'seller/type_change.html', {'goods_type_obj': goods_type_obj})


# 商品类型删除
def type_delete(request):
    id = request.GET.get('id')
    page_num = request.GET.get('page')
    models.Goods_Type.objects.get(id=id).delete()
    return redirect('/seller/type_list/?page=' + page_num)


# 第一次改进版商品类型增加.1
def type_add1(request):
    return render(request, 'seller/type_add1.html')


# 第一次改进版商品类型增加.2
def type_add_ajax1(request):
    dic = {'status': 'false'}
    if request.method == 'POST':
        type_name = request.POST.get('name')
        if type_name:
            ret = models.Goods_Type.objects.filter(name=type_name)
            if ret:
                dic['status'] = 'true'
            else:
                models.Goods_Type.objects.create(
                    name=type_name
                )
    return JsonResponse(dic)


import time


# 添加商品
def goods_add(request):
    if request.method == 'GET':
        # 1.查询数据库中的商品类型
        goods_type_obj_list = models.Goods_Type.objects.all()

        return render(request, 'seller/goods_add.html', {'goods_type_obj_list': goods_type_obj_list})

    else:
        """post 请求"""
        # 1. 获取表单提交过来的内容
        goods_num = request.POST.get('goods_num')  # 编号
        goods_name = request.POST.get('goods_name')  # 名称
        goods_oprice = request.POST.get('goods_oprice')  # 原价
        goods_xprice = request.POST.get('goods_xprice')  # 现价
        goods_count = request.POST.get('goods_count')  # 库存
        goods_type_id = request.POST.get('goods_type')  # 商品类型（获取的是id)
        goods_content = request.POST.get('goods_content')  # 详情
        goods_description = request.POST.get('goods_description')  # 描述

        userfiles = request.FILES.getlist('userfiles')  # 获取图片
        # 2. 保存数据库
        goods_obj = models.Goods.objects.create(
            goods_num=goods_num,
            goods_name=goods_name,
            goods_oprice=goods_oprice,
            goods_cprice=goods_xprice,
            goods_kucun=goods_count,
            type_id=goods_type_id,
            goods_detail=goods_content,
            goods_desc=goods_description,
            seller_id=request.session.get('seller_id')
        )

        # 3.保存图片
        for userfile in userfiles:
            time_temp = str(time.time())  # 时间戳
            path = 'static/goodsimage/' + time_temp + '_' + userfile.name
            with open(path, mode='wb') as f:
                for foo in userfile.chunks():
                    f.write(foo)
            models.GoodsImage.objects.create(
                image_address='goodsimage/' + time_temp + '_' + userfile.name,
                goods=goods_obj
            )
        # 4.重定向到商品列表
        return redirect('/seller/goods_list/')


def goods_list(request):
    seller_id = request.session.get('seller_id')
    goods_obj_list = models.Goods.objects.filter(seller_id=seller_id)
    my_num = 2
    paginator = Paginator(goods_obj_list, my_num)
    num_pages = paginator.num_pages  # 总共页码数
    count = paginator.count  # 总记录数
    try:
        current_num = None
        current_num = int(request.GET.get('page', 1))
        page_obj = paginator.page(current_num)
    except EmptyPage:
        if current_num:
            if num_pages < current_num:
                current_num = num_pages
                page_obj = paginator.page(current_num)
        else:
            current_num = 1
            page_obj = paginator.page(1)

    # 2. 返回
    return render(request, 'seller/goods_list.html', locals())


import os


def goods_delete(request):
    goods_id = request.GET.get('id')
    page_num = request.GET.get('page')
    goodsimage_obj = models.GoodsImage.objects.filter(goods_id=goods_id)
    for goodsimage in goodsimage_obj:
        path = goodsimage.image_address
        path = 'static/' + path
        os.remove(path)
    models.Goods.objects.get(id=goods_id).delete()
    return redirect('/seller/goods_list/?page=' + page_num)


# 商品修改
def goods_change(request):
    if request.method == 'GET':
        # 1.获取商品
        id = request.GET.get('id')
        # 2.查询数据库
        goods_obj = models.Goods.objects.get(id=id)  # 查询当前商品
        goods_type_obj_list = models.Goods_Type.objects.all()  # 查询所有商品类型
        # 3.返回
        return render(request, 'seller/goods_change.html', locals())
    else:
        print('ssss')
        # 1.获取表单内容
        id = request.POST.get('id')
        goods_num = request.POST.get('goods_num')  # 编号
        goods_name = request.POST.get('goods_name')  # 名称
        goods_oprice = request.POST.get('goods_oprice')  # 原价
        goods_xprice = request.POST.get('goods_xprice')  # 现价
        goods_count = request.POST.get('goods_count')  # 库存
        goods_type_id = request.POST.get('goods_type')  # 商品类型（获取的是id)
        goods_content = request.POST.get('goods_content')  # 详情
        goods_description = request.POST.get('goods_description')  # 描述
        userfiles = request.FILES.getlist('userfiles')  # 获取图片
        # 2.保存数据库
        goods_obj = models.Goods.objects.get(id=id)
        goods_obj.goods_num = goods_num
        goods_obj.goods_name = goods_name
        goods_obj.goods_oprice = goods_oprice
        goods_obj.goods_cprice = goods_xprice
        goods_obj.goods_kucun = goods_count
        goods_obj.type_id = goods_type_id
        goods_obj.goods_detail = goods_content
        goods_obj.goods_desc = goods_description
        goods_obj.save()
        # 3.删除图片
        goods_image_obj_list = models.GoodsImage.objects.filter(goods_id=id)
        for goods_image_obj in goods_image_obj_list:
            path = 'static/' + goods_image_obj.image_address
            os.remove(path)
        goods_image_obj_list.delete()
        # 4.保存图片
        for userfile in userfiles:
            time_temp = time.time()
            path = 'static/goodsimage/' + str(time_temp) + '_' + userfile.name
            with open(path, mode='wb') as f:
                for con in userfile:
                    f.write(con)
            models.GoodsImage.objects.create(
                image_address='goodsimage/' + str(time_temp) + '_' + userfile.name,
                goods=goods_obj
            )
        # 5.重定向
        return redirect('/seller/goods_list/')


# 头像自选
def touxiang(request):
    touxiang_obj = models.TouXiang.objects.all()
    my_num = 10
    paginator = Paginator(touxiang_obj, my_num)
    num_pages = paginator.num_pages  # 总共页码数
    count = paginator.count  # 总记录数
    try:
        current_num = int(request.GET.get('page', 1))
        page_obj = paginator.page(current_num)
    except EmptyPage:
        if num_pages < current_num:
            current_num = num_pages
            page_obj = paginator.page(current_num)
        else:
            page_obj = paginator.page(1)
    return render(request, 'seller/touxiang.html', locals())


def xuanze(request):
    id = request.GET.get('img_id')
    touxiang_obj = models.TouXiang.objects.get(id=id)
    seller_id = request.session.get('seller_id')
    seller_obj = models.Seller.objects.get(id=seller_id)
    seller_obj.picture = touxiang_obj.name
    seller_obj.save()
    return redirect('/seller/index/')

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

# 白名单
#  /: 表示访问商城的首页
white_list = ['/seller/login/', '/seller/register/', '/']


class AuthMD(MiddlewareMixin):

    def process_request(self, request):
        # 1. 获取url路径部分
        path_info = request.path_info
        print(path_info)
        # 2. 进行判断
        # 如果路径在白名单中就放行
        if path_info in white_list:
            return
        # 如果是买家访问，全部放行
        if path_info.find('/buyer/') != -1:
            print('放行...。。。。')
            return

            # 3. 判断是否登录了,如果登录了，则放行
        username = request.session.get('username')
        if username:
            return

        # 4. 如果不在白名单和没有登录则重定向到 登录页面。
        return redirect('/seller/login/')
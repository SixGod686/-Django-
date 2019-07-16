import hashlib
import uuid

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from design.models import User, Collect, Site


# Create your views here.
# 生成token值
def make_token():
    uid = str(uuid.uuid4())
    # 使用md5进行加密处理
    md = hashlib.md5()
    md.update(uid.encode('utf-8'))

    return uid


# 密码加密
# 将密码加密封装成一个函数，可以多次调用
def make_pwd(pwd):
    password = str(pwd)
    # 使用md5进行密码加密
    mdd = hashlib.md5()
    # 编码格式为‘utf-8’
    mdd.update(password.encode('utf-8'))

    return mdd.hexdigest()


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'login-register.html')
    elif request.method == 'POST':
        phone = request.POST.get('phone')
        pwd = request.POST.get('password')
        users = User.objects.filter(phone=phone)
        u = users.first()
        # 判断用户是否存在
        if not users.exists():
            data = {
                'num': 1
            }
            return render(request, 'login-register.html', context=data)
        if u.password == make_pwd(pwd):
            response = HttpResponseRedirect(reverse('design:index'))
            response.set_cookie('token', u.token)
            return response
        else:
            return HttpResponse('账号或密码错误')


# 注册功能
def register(request):
    if request.method == 'GET':
        return render(request, 'login-register.html')
    elif request.method == 'POST':
        u_icon = request.FILES['icon']
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        phone = request.POST.get('phone')
        birthday = request.POST.get('birthday')
        password = request.POST.get('password')
        users = User.objects.filter(phone=phone).count()
        if users == 1:
            data = {
                'count': 1
            }
            return render(request, 'login-register.html', context=data)
        else:
            user = User()
            user.icon = u_icon
            user.username = username
            user.nickname = nickname
            sex1 = request.POST.get("sex")
            if sex1 == '男':
                user.sex = True
            elif sex1 == '女':
                user.sex = False
            user.phone = phone
            user.birthday = birthday
            user.password = make_pwd(password)
            user.token = make_token()

            user.save()
            red = redirect(reverse('design:index'))
            red.set_cookie('token', user.token)

            return red


# 首页
def index(request):
    token = request.COOKIES.get('token')
    if not token:
        return render(request, 'index.html')
    user = User.objects.get(token=token)
    icon = '/static/headimages/' + user.icon.url
    dic = {
        'users': user,
        'url': icon,
        'token': token
    }
    return render(request, 'index.html', context=dic)


# 路线搜索
def search(request):
    token = request.COOKIES.get('token')
    if not token:
        return render(request, 'search.html')
    data = {
        'token': token
    }
    return render(request, 'search.html', context=data)


# 路线规划,及路线收藏
def drawing(request):
    token = request.COOKIES.get('token')
    start = request.POST.get('start')
    end = request.POST.get('end')
    if not token:
        dict = {
            'start': start,
            'end': end
        }
        return render(request, 'drawing-route.html', context=dict)
    else:
        user = User.objects.get(token=token)
        collect = Collect()
        collect.c_user_id = user.id
        collect.line_origin = start
        collect.line_destination = end
        collect.site = None
        collect.save()
        dict = {
            'start': start,
            'end': end
        }
        return render(request, 'drawing-route.html', context=dict)


# 点击头像的操作
def clickImg(request):
    token = request.COOKIES.get('token')
    if not token:
        return render(request, 'user/user.html')
    else:
        user = User.objects.get(token=token)
        icon = '/static/headimages/' + user.icon.url
        data = {
            'token': token,
            'user': user,
            'icon': icon
        }
        return render(request, 'user/user.html', context=data)


# 基本资料显示与修改
def user_base_info(request):
    token = request.COOKIES.get('token')
    if not token:
        return render(request, 'user/user_base_info.html')
    else:
        user = User.objects.get(token=token)
        if request.method == 'GET':
            data = {
                'username': user.username,
                'phone': user.phone,
                'nickname': user.nickname,
                'sex': user.sex
            }
            return render(request, 'user/user_base_info.html', context=data)
        elif request.method == 'POST':
            username = request.POST.get('username')
            nick_name = request.POST.get('nick_name')
            phone = request.POST.get('phone')
            user.username = username
            user.nickname = nick_name
            user.phone = phone
            user.save()
            data = {
                'username': user.username,
                'phone': user.phone,
                'nickname': user.nickname,
                'sex': user.sex
            }
            return render(request, 'user/user_base_info.html', context=data)


# 头像设置
def user_pic_info(request):
    token = request.COOKIES.get('token')
    if not token:
        return render(request, 'user/user_pic_info.html')
    else:
        user = User.objects.get(token=token)
        if request.method == 'GET':
            icon = '/static/headimages/' + user.icon.url
            data = {
                'url': icon
            }
            return render(request, 'user/user_pic_info.html', context=data)
        elif request.method == 'POST':
            u_icon = request.FILES.get('icon')
            with open(u_icon.name,'wb') as f:
                for line in u_icon:
                    f.write(line)
            if u_icon == None:
                return HttpResponse('数据错误')
            user.icon = u_icon
            user.save()
            url = '/static/headimages/' + user.icon.url
            data = {
                'url': url
            }
            return render(request, 'user/user_pic_info.html', context=data)


# 密码修改
def user_pass_info(request):
    token = request.COOKIES.get('token')
    if not token:
        return render(request, 'user/user_pass_info.html')
    else:
        if request.method == 'GET':
            data = {
                'token': token
            }
            return render(request, 'user/user_pass_info.html', context=data)
        elif request.method == 'POST':
            user = User.objects.get(token=token)
            old_psd = request.POST.get('old_password')
            new_psd = request.POST.get('new_password')
            if make_pwd(old_psd) == user.password:
                user.password = make_pwd(new_psd)
                user.save()
                response = render(request, 'user/user_pass_info.html')
                response.delete_cookie('token')
                return response
            else:
                return HttpResponse('原密码错误')


# 我的收藏
def user_collection(request):
    token = request.COOKIES.get('token')
    if not token:
        return render(request, 'user/user_collection.html')
    else:
        if Collect is None:
            return render(request, 'user/user_collection.html')
        else:
            user = User.objects.get(token=token)
            collections = Collect.objects.filter(c_user_id=user.id)
            sites = Site.objects.filter(s_user_id=user.id)
            data = {
                'collection': collections,
                'sites':sites,
                'token': token
            }
            return render(request, 'user/user_collection.html', context=data)


# 退出登录
def logout(request):
    response = HttpResponseRedirect(reverse('design:clickImg'))
    response.delete_cookie('token')
    return response


# 收藏地点
def collection(request):
    token = request.COOKIES.get('token')
    user = User.objects.get(token=token)
    s = Site()
    site = request.POST.get('site')
    print(site)
    s.s_user_id = user.id
    s.site = site
    s.save()
    return redirect(reverse('design:user_collection'))
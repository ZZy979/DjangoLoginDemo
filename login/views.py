from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from login.models import User


def index(request):
    return render(request, 'login/index.html', {'message': request.GET.get('message')})


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'login/register.html')
    username = request.POST['username']
    password = User.encrypt_password(request.POST['password'])
    if User.objects.filter(username=username).exists():
        return render(request, 'login/register.html', {'error_message': '用户名已存在'})
    User.objects.create(username=username, password=password)
    return HttpResponseRedirect(reverse('login:index') + '?message=注册成功')


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
    username = request.POST['username']
    password = User.encrypt_password(request.POST['password'])
    try:
        user = User.objects.get(username=username)
        if user.password == password:
            request.session['username'] = user.username
            return redirect('login:index')
        else:
            return render(request, 'login/login.html', {'error_message': '用户名或密码错误'})
    except User.DoesNotExist:
        return render(request, 'login/login.html', {'error_message': '用户名或密码错误'})


def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return HttpResponseRedirect(reverse('login:index') + '?message=注销成功')

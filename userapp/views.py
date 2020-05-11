from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def login(request):
    return HttpResponse('登录')

def regist(request):
    return HttpResponse('注册')

def login_logic(request):
    return HttpResponse('登录逻辑')
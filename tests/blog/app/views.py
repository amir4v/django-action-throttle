from django.shortcuts import render
from django.http import HttpResponse

from action_throttle.throttle import action_throttle


def home(request):
    action_throttle(user=request.user, limit_name='home-page', raise_exception=True)
    
    return HttpResponse('<h1>Home sweet home :)</h1>')

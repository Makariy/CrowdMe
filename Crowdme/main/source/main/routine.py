from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse_lazy
import json
import os
from django.contrib.auth import get_user



class PageBase:
    def __init__(self):
        pass

    def handle(self, request: HttpRequest, *params, **args):
        if request.method == 'POST':
            return self.post(request, *params, **args)
        else:
            return self.get(request, *params, **args)

    def post(self, request: HttpRequest, *params, **args) -> HttpResponse:
        return HttpResponse()

    def get(self, request: HttpRequest, *params, **args) -> HttpResponse:
        return HttpResponse()

    def set_cookies(self, response, cookies={}, **kwargs):
        if not cookies == {}:
            if not isinstance(cookies, type({})):
                raise TypeError('Parameter cookies was not the correct type: type(cookies) = ' + str(type(cookies)))
            else:
                for key in cookies:
                    response.set_cookie(key, cookies[key])
        else:
            for key in kwargs:
                response.set_cookie(key, cookies[key])



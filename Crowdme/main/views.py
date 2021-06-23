import datetime, json
import os

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from django.views.generic import edit
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from .models import Project
from .models import User
from .forms import UserForm

from .source.main.routine import *

from .models import MinValueValidator


# Create your views here.


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


class MainPage(PageBase):
    def __init__(self):
        self.times_called = 0
        self.clients_profiles = ClientsProfilingFile()

    def __is_time(self):
        if self.times_called > 100:
            self.times_called = 0
            return True
        self.times_called += 1
        return False

    def check_date(self, projects):
        today = datetime.date.today()
        for i in range(len(projects)):
            if (today - projects[i].published_date).days > 1:
                projects[i].is_new = False
            else:
                projects[i].is_new = True
            projects[i].save()

    def get(self, request, *params, **args):
        self.clients_profiles.add_client(request.environ["wsgi.input"].stream.raw._sock.getpeername())

        projects = Project.objects.all().order_by('funded')
        if self.__is_time():
            self.check_date(projects)
            self.clients_profiles.write()

        context = {'projects': projects}

        if Authorization.check_user(request):
            context['user_in'] = True
            context['user_name'] = request.COOKIES.get('user_name')
        else:
            context['user_in'] = False

        return HttpResponse(render(request, 'main/index.html', context))

    def post(self, request, *params, **args):
        self.clients_profiles.add_client(request.environ["wsgi.input"].stream.raw._sock.getpeername())

        projects = Project.objects.all().order_by('funded')

        context = {'projects': projects}
        ret = HttpResponse(render(request, 'main/index.html', context))
        self.set_cookies(ret, {'user_name': None, 'user_password': None})
        return ret


class Authorization(PageBase):
    @staticmethod
    def check_user(request):
        if request.COOKIES.get('user_name') and request.COOKIES.get('user_password'):
            db_user = User.objects.all().filter(name=request.COOKIES.get('user_name'))
            if len(db_user) > 0:
                if request.COOKIES.get('user_password') == StringHasher.get_hash(db_user[0].password):
                    return True

        return False

    def __check_user(self, user, db_user):
        if not db_user:
            return "User with this name doesn't exist"
        if not db_user[0].password == user['password']:
            return "Incorrect password"
        return ''

    def post(self, request: HttpRequest, *params, **args):
        user = UserForm(request.POST)
        db_user = User.objects.all().filter(name=user.data['name'])
        error = self.__check_user(user.data, db_user)
        if not error == '':
            return self.get(request, error)

        ret = redirect(reverse_lazy('main'))
        self.set_cookies(ret, {'user_name': user.data['name'], 'user_password': StringHasher.get_hash(db_user[0].password)})
        return ret

    def get(self, request: HttpRequest, *params, **args):
        context = {'form': UserForm}
        if not params == ():
            context['error'] = params[0]
        return HttpResponse(render(request, 'main/login.html', context))


class Registration(PageBase):
    def check_user(self, user):
        if (user['name'] == '') or (user['name'][0].isdigit()) or (len(user['name']) < 2):
            return "Your name is too short or starts with a digit"
        if (len(user['password']) < 6) or (not user['password'].lower().find(user['name'].lower()) == -1):
            return "Your password is too short or contains your name"
        if User.objects.all().filter(name=user['name']).count() > 0:
            return "This name is already used"
        if User.objects.all().filter(mail=user['mail']).count() > 0:
            return "This mail is already used"
        return ''

    def post(self, request, *params, **args):
        post = UserForm(request.POST)
        error = self.check_user(post.data)
        if not error == '':
            return self.get(request, error)
        print(post.data['name'], post.data['password'], post.data['mail'])
        user = post.save()
        user.save()
        ret = redirect(reverse_lazy('main'))
        self.set_cookies(ret, {'user_name': user.name, 'user_password': StringHasher.get_hash(user.password)})
        return ret

    def get(self, request, *params, **args):
        context = {'form': UserForm}
        if not params == ():
            context['error'] = params[0]
        return HttpResponse(render(request, 'main/signup.html', context))


class ClientsSettingsPage(PageBase):
    def post(self, request, *params, **args):
        return self.get(request, *params, **args)

    def get(self, request, *params, **args):
        name = args['user_name']
        if not name:
            return redirect(reverse_lazy('main'))
        user = User.objects.all().get(name=name)
        if not request.COOKIES.get('user_password'):
            return redirect(reverse_lazy('main'))
        elif not StringHasher.get_hash(user.password) == request.COOKIES['user_password']:
            return redirect(reverse_lazy('main'))
        context = {'user': user}
        return HttpResponse(render(request, 'main/settings.html', context))


class ProjectPage(PageBase):
    def get(self, request, *params, **args):
        id = args['project_id']
        try:
            project = Project.objects.all().get(pk=id)
            return HttpResponse(str(project))

        except ObjectDoesNotExist:
            return redirect(reverse_lazy('main'))



class PageTest(PageBase):
    def get(self, request, *p, **args):
        print(request.GET)
        return redirect(reverse_lazy('main'))

    def post(self, request, *params, **args):
        print(request.GET)
        return redirect(reverse_lazy('main'))

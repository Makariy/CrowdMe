import datetime, json
import os

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from django.contrib.auth import get_user, authenticate, login, logout
from django.contrib.auth.models import User, AnonymousUser


from django.views.generic import edit
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from .models import Project

from .source.main.routine import *

from .models import MinValueValidator


# Create your views here.
class MainPage(PageBase):
    def __init__(self):
        self.times_called = 0

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
        projects = Project.objects.all().order_by('funded')
        if self.__is_time():
            self.check_date(projects)
            self.clients_profiles.write()

        context = {'projects': projects}

        user = get_user(request)

        if not user.is_anonymous or not user:
            context['user_in'] = True
            context['user_name'] = user.username
        else:
            context['user_in'] = False

        return HttpResponse(render(request, 'main/index.html', context))

    def post(self, request, *params, **args):
        logout(request)
        return redirect(reverse_lazy('main'))


class Authorization(PageBase):
    def post(self, request: HttpRequest, *params, **args):
        user_data = request.POST
        user = authenticate(username=user_data['name'], password=user_data['password'])
        if user:
            login(request, user)
            return redirect(reverse_lazy('main'))
        else:
            return redirect(reverse_lazy('login'))

    def get(self, request: HttpRequest, *params, **args):
        return HttpResponse(render(request, 'main/login.html'))


class Registration(PageBase):
    def check_user(self, user):
        if (user['name'] == '') or (user['name'][0].isdigit()) or (len(user['name']) < 2):
            return "Your name is too short or starts with a digit"
        if (len(user['password']) < 6) or (not user['password'].lower().find(user['name'].lower()) == -1):
            return "Your password is too short or contains your name"
        if User.objects.all().filter(username=user['name']).count() > 0:
            return "This name is already used"
        if User.objects.all().filter(email=user['mail']).count() > 0:
            return "This mail is already used"
        return ''

    def post(self, request, *params, **args):
        user_form = request.POST
        error = self.check_user(user_form)
        if not error == '':
            return self.get(request, error)
        print(user_form)
        user = User.objects.create_user(username=user_form['name'], password=user_form['password'], email=user_form['mail'])
        user.save()
        login(request, user)
        return redirect(reverse_lazy('main'))

    def get(self, request, *params, **args):
        return HttpResponse(render(request, 'main/signup.html', {'error': params[0] if params else None}))


class ProjectPage(PageBase):
    def get(self, request, *params, **args):
        user = get_user(request)
        if user.is_anonymous or not user.has_perm('main.can_redact_project'):
            return redirect('main')
        id = args['project_id']
        try:
            project = Project.objects.all().get(pk=id)
            return HttpResponse(str(project))

        except ObjectDoesNotExist:
            return redirect(reverse_lazy('main'))


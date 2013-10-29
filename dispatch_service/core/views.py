from django.contrib.auth import logout, authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View


class IndexView(TemplateView):

    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(IndexView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))


class LoginFormView(TemplateView):
    template_name = 'core/login.html'


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


class AuthenticationView(View):

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['pass']

        auth_user = authenticate(username=username, password=password)
        if auth_user is not None:
            login(request, auth_user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('login'))


from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View, DetailView


class IndexView(DetailView):

    model = User
    template_name = 'core/index.html'
    context_object_name = 'auth_user'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            self.kwargs['pk'] = request.user.id
            return super(IndexView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))

    #def get_object(self, queryset=None):
    #    obj = super(IndexView, self).get_object(queryset)
    #    #obj.executors_set.all()
    #    messages.add_message(
    #        self.request,
    #        messages.INFO,
    #        'You have %s events' % obj.executors_set.filter(decision=None).count()
    #    )
    #    return obj



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


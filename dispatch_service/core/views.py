from tempfile import TemporaryFile, NamedTemporaryFile
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View, DetailView
from dispatch_service import settings
from utils.sftp import SFTP


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


class LoginFormView(TemplateView):
    template_name = 'core/login.html'


class FileFormView(TemplateView):
    template_name = 'core/fileform.html'


class FileLoadView(View):

    def post(self, request, *args, **kwargs):

        print True, request.FILES, request.POST

        f = request.FILES.get('file')
        if not f:
            messages.add_message(
                request,
                messages.INFO,
                'You do not choose a file'
            )
            return HttpResponseRedirect(reverse('fileform'))
        else:
            with NamedTemporaryFile(prefix='__', suffix='test') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
                with SFTP(
                    settings.REMOTE_HOST,
                    request.POST['login'],
                    request.POST['password'],
                    settings.PORT
                ) as sftp:

                    try:
                        sftp.connect()
                        sftp.put_file_to_remote_host(destination.name)
                        messages.add_message(
                            request,
                            messages.INFO,
                            'File was loaded successfully')
                    except Exception, e:
                        messages.add_message(
                            request,
                            messages.INFO,
                            'Error during loading a file: %s' % e.message
                        )

        return HttpResponseRedirect(reverse('home'))


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


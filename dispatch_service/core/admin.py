import os
from django import forms
from django.contrib import admin

from utils.sftp import SFTP
from core.models import Settings
from dispatch_service import settings


class SettingsForm(forms.ModelForm):
    path = os.path.realpath(os.path.join(settings.DJANGO_PROJECT_ROOT, 'conf.ini'))
    settings = forms.CharField(widget=forms.Textarea())

    def read_settings(self):
        with open(self.path, 'r') as conf_file:
            return conf_file.read()

    def write_settings(self, content):
        with open(self.path, 'w') as conf_file:
            return conf_file.write(content)

    class Meta:
        model = Settings

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        conf = self.read_settings()
        self.fields['settings'].initial = conf
        params = SFTP.get_params(conf.split('\n'))
        for p in params:
            setattr(settings, str(p[0]).upper(), p[1])

    def clean_settings(self):
        data = self.cleaned_data['settings']
        if not SFTP.validate_conf(data=data):
            raise forms.ValidationError("You conf is not valid!")
        return data

    def save(self, commit=True):
        instance = super(SettingsForm, self).save(commit=commit)
        if self.is_valid():
            conf = self.cleaned_data.get('settings')
            self.write_settings(self.cleaned_data.get('settings'))
            params = SFTP.get_params(conf.split('\n'))
            for p in params:
                setattr(settings, str(p[0]).upper(), p[1])
        return instance


class ServerSettingsAdmin(admin.ModelAdmin):
    form = SettingsForm
    fields = ('settings',)
admin.site.register(Settings, ServerSettingsAdmin)
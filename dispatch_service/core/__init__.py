import os
from dispatch_service import settings
from utils.sftp import SFTP

path = os.path.realpath(os.path.join(settings.DJANGO_PROJECT_ROOT, 'conf.ini'))

params = []
if SFTP.validate_conf(path):
    with open(path, 'r') as conf_file:
        params = SFTP.get_params(conf_file.read().split('\n'))
    for p in params:
        setattr(settings, str(p[0]).upper(), p[1])
import os
import pysftp


class SFTP():

    def __init__(self, host=None, username=None, password=None, port=22):
        self.valid = True

        if host and username and password:
            setattr(self, 'host', host)
            setattr(self, 'username', username)
            setattr(self, 'password', password)
            setattr(self, 'port', port)

        else:

            dir_name = os.path.dirname(__file__)
            project_dir = os.path.realpath(os.path.join(dir_name, '..'))

            with open(project_dir+'/conf.ini', 'r') as conf_file:
                values = self.get_params(conf_file.readlines())
                for value in values:
                    setattr(self, value[0], value[1].strip())

            for opt in ('host', 'port', 'username', 'password'):
                if opt not in [i[0] for i in values]:
                    self.valid = False

    def __enter__(self):
        return self

    def connect(self):
        if self.valid:
            connection = pysftp.Connection(
                host=self.host,
                port=int(self.port),
                username=self.username,
                password=self.password,
            )

            setattr(self, 'connection', connection)

    def put_file_to_remote_host(self, file_name):
        if hasattr(self, 'connection'):
            self.connection.put(file_name)

    def get_file_from_remote_host(self, file_name):
        if hasattr(self, 'connection'):
            self.connection.get(file_name)

    def __exit__(self, type, value, traceback):
        if hasattr(self, 'connection'):
            self.connection.close()

    @staticmethod
    def validate_conf(path=None, data=None):
        is_valid = True
        if path:
            with open(path, 'r') as conf_file:
                content = conf_file.read()
        else:
            if data:
                content = data
            else:
                is_valid = False

        if(not 'host' in content and
           not 'port' in content
           ):
            is_valid = False
        else:
            lines = str(content).split('\n')
            for line in lines:
                if str(line).count('=') > 1:
                    is_valid = False
        return is_valid

    @staticmethod
    def get_params(data):
        values = []
        for line in data:
            if str(line).startswith('#'):
                continue
            value = str(line).split('=')
            for i, v in enumerate(value):
                v = v.strip()
                value[i] = v

            if len(value) < 2:
                continue
            else:
                values.append(value)
        return values

if __name__ == "__main__":
    with SFTP() as sftp:
        sftp.connect()
        sftp.put_file_to_remote_host('__init__.py')
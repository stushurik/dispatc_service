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
                values = []
                for line in conf_file.readlines():
                    if str(line).startswith('#'):
                        continue
                    value = str(line).split('=')

                    if len(value) < 2:
                        continue
                    else:
                        param = value[0].strip()
                        setattr(self, param, value[1].strip())
                        values.append(param)

            print values, type(values)
            for opt in ('host', 'port', 'username', 'password'):
                print opt
                if opt not in values:
                    print 'its a trap!'
                    self.valid = False

    def __enter__(self):
        return self

    def connect(self):
        print self.valid

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

if __name__ == "__main__":
    with SFTP() as sftp:
        sftp.connect()
        sftp.put_file_to_remote_host('__init__.py')
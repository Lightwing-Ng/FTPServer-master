#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''
 * @author: Lightwing Ng
 * email: rodney_ng@iCloud.com
 * created on Mar 15, 2018, 10:20 PM
 * Software: PyCharm
 * Project Name: Tutorial
'''

'''
Client
'''

import socket, os, json, hashlib


class FtpClient(object):
    def __init__(self, ):
        self.client = socket.socket()

    def connect(self, ip, port):
        '''

        :param ip:
        :param port:
        :return:
        '''
        self.client.connect((ip, port))

    def login(self):
        '''
        For user to login
        :return:
        '''
        name = input('Please input your account: ').strip()
        password = input('Please input your password: ').strip()
        infos = {
            'action': 'login',
            'name': 'name',
            'password': password
        }
        self.client.send(json.dumps(infos).encode('UTF-8'))
        res = self.client.recv(1024).decode('UTF-8')
        if res == '0':
            print('Login...'.center(50, ' '))
            self.interactive()
        else:
            exit('Login Failed.'.center(50, ' '))

    def interactive(self):
        '''
        To interactive with users
        :return:
        '''
        while True:
            cmd = input('>>>: ')
            if len(cmd) == 0:
                continue
            action = cmd.split(' ')[0]
            if hasattr(self, '%s' % action):
                func = getattr(self, '%s' % action)
                func(cmd)
            else:
                print('Sorry that command does not exist!')
                self.help()

    def put(self, *args):
        '''
        Send files
        :param args:
        :return:
        '''
        cmd_splt = args[0].split(' ')
        if len(cmd_splt):
            filename = cmd_splt[1]
            if os.path.isfile(filename):
                size = os.stat(filename).st_size
                msg_dct = {
                    'action': 'put',
                    'filename': filename,
                    'size': size,
                    'override': True
                }
                self.client.send(json.dumps(msg_dct).encode('UTF-8'))
                server_response = self.client.recv(1024).decode('UTF-8')
                if server_response == '0':
                    print('Enough to store.'.center(50, ' '))
                else:
                    exit('No enough space to store'.center(50, ' '))
                m = hashlib.md5()
                f = open(filename, 'rb')
                send_len = 0
                for line in f:
                    self.client.send(line)
                    m.update(line)
                    send_len += len(line)
                f.close()

                # Check MD5
                self.client.send(m.hexdigest().encode('UTF-8'))
                res = self.client.recv(1024).decode('UTF-8')
                if res == '0':
                    print('File Tranmission Done'.center(50, ' '))
                else:
                    print('Falied!'.center(50, ' '))
            else:
                exit('File %s does not exist!' % filename)

    def get(self, *args):
        '''
        Receive file
        :param args:
        :return:
        '''
        cmd_split = args[0].split(' ')
        if len(cmd_split):
            filename = cmd_split[1]
            msg_dct = {
                'action': 'get',
                'filename': filename
            }
            self.client.send(json.dumps(msg_dct).encode('UTF-8'))
            server_response = self.client.recv(1024)
            server_dct = json.loads(server_response.decode('UTF-8'))

            if server_dct['isfile']:
                self.client.send(b"200 ok")
                m = hashlib.md5()
                f = open(filename, 'wb')
                data_size = server_dct['size']
                received_size = 0
                while received_size < data_size:
                    if data_size - received_size > 1024:
                        size = 1024
                    else:
                        size = data_size - received_size
                    data = self.client.recv(size)
                    f.write(data)
                    m.update(data)
                    received_size += len(data)
                else:
                    f.close()
                    received_md5 = self.client.recv(1024).decode('UTF-8')

                    if m.hexdigest() == received_md5:
                        print('File downloaded.'.center(50, ' '))
                        self.client.send('0'.encode('UTF-8'))
                    else:
                        print('File downloaded Error.'.center(50, ' '))
                        self.client.send('-1'.encode('UTF-8'))
            else:
                exit('File does not exist.'.center(50, ' '))

    def cd(self, *args):
        '''
        Change the current diretory
        :param args:
        :return:
        '''
        cmd_split = args[0].strip().split(' ')
        if len(cmd_split):
            dirname = cmd_split[1]
            msg_dct = {
                'action': 'cd',
                'dirname': dirname
            }

            self.client.send(json.dumps(msg_dct).encode('UTF-8'))
            server_response = self.client.recv(1024)
            server_dct = json.loads(server_response.decode('UTF-8'))
            print(server_dct['current: '])

    def ls(self, *args):
        '''
        List all the files below
        :param args:
        :return:
        '''
        msg_dct = {
            'action': 'ls'
        }
        self.client.send(json.dumps(msg_dct).encode('UTF-8'))
        server_response = self.client.recv(1024)
        server_dct = json.loads(server_response.decode('UTF-8'))
        print(server_dct['ls'])

    def pwd(self, *args):
        '''
        Show the current diretory
        :param args:
        :return:
        '''
        msg_dct = {'action': 'pwd'}
        self.client.send(json.dumps(msg_dct).encode('UTF-8'))
        server_response = self.client.recv(1024)
        server_dct = json.loads(server_response.decode('UTF-8'))
        print(server_dct['current'])

    def mkdir(self, *args):
        '''
        Make a new diretory
        :param args:
        :return:
        '''
        cmd_split = args[0].strip().split(' ')
        if len(cmd_split):
            dirname = cmd_split[1]
            msg_dct = {
                'action': 'mkdir',
                'dirname': dirname
            }
            self.client.send(json.dumps(msg_dct).encode('UTF-8'))
            server_response = self.client.recv(1024)
            server_dct = json.loads(server_response.decode('UTF-8'))
            print(server_dct['current'])

    def help(self):
        '''
        Help Menu
        :return:
        '''
        help_menu = '''
        ls              List all files
        pwd             Show the current directory
        cd [diretory]   Go to the diretory
        mkdir           Create a new diretory
        get [filename]  Dowonload file
        put [filename]  Upload file
        '''


def run():
    '''
    boot the client
    :return:
    '''
    myFTP = FtpClient()
    myFTP.connect('localhost', 6969)
    myFTP.login()


if __name__ == '__main__':
    run()

#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''
 * @author: Lightwing Ng
 * email: rodney_ng@iCloud.com
 * created on Mar 15, 2018, 10:20 PM
 * Software: PyCharm
 * Project Name: Tutorial
'''

import socketserver, json, hashlib, os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import user_manager as users

users_path = users.users_path
home = r'./files/'


class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        '''
        Server end, the entry of data
        :return:
        '''
        while True:
            try:
                self.data = self.request.recv(1024)
                print('Client Address: ', self.client_address)
                print("Client's Infos: ", self.data)
                cmd_dct = json.loads(self.data.decode('UTF-8'))
                action = cmd_dct['action']
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(cmd_dct)
            except ConnectionResetError as e:
                exit(e)

    def login(self, *args):
        '''
        Server end's login entry
        :param args:
        :return:
        '''
        cmd_dct = args[0]
        user_path = os.path.join(users_path, cmd_dct['name'] + '.json')
        print('User path: ', user_path)
        if os.path.isfile(user_path):
            user = json.load(open(user_path, 'r'))
            if cmd_dct['password'] == user['password']:
                self.request.send('0'.encode('UTF-8'))
                print('Authentication Pass.')

                self.current = user['name']
                self.username = user['name']
                current_path = os.path.join(home, self.current)

                if not os.path.exists(current_path):
                    os.mkdir(current_path)
                return
            else:
                print('Password is not correct.')
        else:
            print('Account does not exist.')
        self.request.send('-1'.encode('UTF-8'))

    def put(self, *args):
        '''
        Receive files
        :param args:
        :return:
        '''
        cmd_dct = args[0]
        current_path = os.path.join(home, self.current)
        filename = os.path.join(current_path, cmd_dct['filename'])
        filesize = cmd_dct['size']

        userinfo = users.getinfo(self.username)
        if userinfo['total_size'] - userinfo['used_size'] > filesize:
            self.request.send('0'.encode('UTF-8'))
            print('Enough to store.'.center(50, ' '))
        else:
            self.request.send("-1".encode('UTF-8'))
            print('No enough space to store'.center(50, ' '))
            return

        if os.path.isfile(filename):
            f = open('new_' + filename, 'wb')
        else:
            f = open(filename, 'wb')
        received_size = 0
        m = hashlib.md5()
        while received_size < filesize:
            if filesize - received_size > 1024:
                size = 1024
            else:
                size = filesize - received_size
            data = self.request.recv(size)

            f.write(data)
            m.update(data)
            received_size += len(data)
        else:
            f.close()
            users.add_used_size(self.username, received_size)

            # Check MD5
            received_md5 = self.request.recv(1024).decode('UTF-8')
            if m.hexdigest() == received_md5:
                print('Upload Successfully.')
                self.request.send("0".encode('UTF-8'))
            else:
                print('Upload failed.')
                self.request.send("-1".encode('UTF-8'))

    def get(self, *args):
        '''

        :param args:
        :return:
        '''
        cmd_dct = args[0]
        current_path = os.path.join(home, self.current)
        filename = os.path.join(current_path, cmd_dct['filename'])

        if os.path.isfile(filename):
            size = os.stat(filename).st_size
            msg_dct = {
                'isfile': True,
                'filename': filename,
                'size': size,
            }

            self.request.send(json.dumps(msg_dct).encode('UTF-8'))
            server_response = self.request.recv(1024)
            m = hashlib.md5()
            f = open(filename, 'rb')
            for line in f:
                self.request.send(line)
                m.update(line)
            f.close()

            self.request.send(m.hexdigest().encode('UTF-8'))
            res = self.request.recv(1024).decode('UTF-8')
            if res == '0':
                print('File Transmission Successed.')
            else:
                print('File Transmission Failed.')
        else:
            msg_dct = {
                'isfile': False,
                'filename': filename,
            }

            self.request.send(json.dumps(msg_dct).encode('UTF-8'))
            print('Fine %s does not exits.' % filename)

    def cd(self, *args):
        '''
        Server end, change the current diretory
        :param args:
        :return:
        '''
        cmd_dct = args[0]
        dirname = cmd_dct['dirname']
        current_path = os.path.join(home, self.current)
        if dirname == "..":
            if self.current != self.username:
                self.current = os.path.dirname(current_path).replace(home, '')
        else:
            cd_path = os.path.join(current_path, dirname)
            if os.path.isdir(cd_path):
                self.current = cd_path.replace(home, '')

        msg_dct = {'current': self.current}
        self.request.send(json.dumps(msg_dct).encode('UTF-8'))

    def ls(self, *args):
        '''
        Server end, list all files below
        :param args:
        :return:
        '''
        current_path = os.path.join(home, self.current)
        lst = os.listdir(current_path)
        msg_dct = {'list': lst}
        self.request.send(json.dumps(msg_dct).encode('UTF-8'))

    def pwd(self, *args):
        '''
        Server end, show the current diretory
        :param args:
        :return:
        '''
        msg_dct = {'current': self.current}
        self.request.send(json.dumps(msg_dct).encode('UTF-8'))

    def mkdir(self, *args):
        '''
        Server end, make a new diretory
        :param args:
        :return:
        '''
        cmd_dct = args[0]
        dirname = cmd_dct['dirname']
        current_path = os.path.join(home, self.current)
        dir_path = os.path.join(current_path, dirname)
        os.mkdir(dir_path)
        self.current = dir_path.replace(home, '')
        msg_dct = {'current': self.current}
        self.request.send(json.dumps(msg_dct).encode('UTF-8'))


def run():
    host, port = 'localhost', 6969
    server = socketserver.ThreadingTCPServer((host, port), MyHandler)
    print('The Server is ready.'.center(50, ' '))
    server.serve_forever()


if __name__ == '__main__':
    run()

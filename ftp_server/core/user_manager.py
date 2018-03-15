#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''
 * @author: Lightwing Ng
 * email: rodney_ng@iCloud.com
 * created on Mar 15, 2018, 10:21 PM
 * Software: PyCharm
 * Project Name: Tutorial
'''
import os, json

# User's path
users_path = r'..\users'


def add_user(name, password, total_size):
    '''
    Add a new user
    :param name:
    :param password:
    :param total_size:
    :return:
    '''
    filename = os.path.join(users_path, name + '.json')
    f = open(filename, 'w')
    info = {
        'name': name,
        'password': password,
        'total_size': int(total_size),
        'used_size': 0
    }
    json.dump(info, f, indent="\t")
    f.close()


def getinfo(name):
    '''
    Get the user's information
    :param name:
    :return: info
    '''
    filename = os.path.join(users_path, name + '.json')
    print('Reading Filename: ', filename)
    f = open(filename, 'r')
    info = json.load(f)
    f.close()
    return info


def add_used_size(name, size):
    '''
    Expand the usage
    :param name:
    :param size:
    :return: info
    '''
    filename = os.path.join(users_path, name + '.json')
    f = open(filename, 'r')
    info = json.load(f)
    f.close()
    f = open(filename, 'w')
    info['used_size'] += int(size)
    json.dump(info, f, indent='\t')
    f.close()
    return info


def create_user(num):
    '''
    Initialized the user's data automatically
    :param num:
    :return:
    '''
    for i in range(1, num):
        name = str(i).zfill(3)
        password = 'abcd1234'
        total_size = 1000
        add_user(name, password, total_size)
    print('Initialized Completed.'.center(50, ' '))


def run():
    name = input('name: ')
    # # password = input("password:")
    # # total_size = input("total_size(bytes):")
    # # add_user(name, password, total_size)
    size = input('size: ')
    add_used_size(name, size)


if __name__ == '__main__':
    create_user(6)

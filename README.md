# FTPServer-master

## File Directory

.
├── .git<br/>
├── README.md<br/>
├── __init__.py<br/>
├── ftp_client<br/>
│   ├── __init__.py<br/>
│   ├── bin<br/>
│   │   ├── __init__.py<br/>
│   │   └── main.py<br/>
│   └── core<br/>
│       ├── __init__.py<br/>
│       ├── __pycache__<br/>
│       │   ├── __init__.cpython-36.pyc<br/>
│       │   └── client.cpython-36.pyc<br/>
│       └── client.py<br/>
└── ftp_server<br/>
    ├── __init__.py<br/>
    ├── bin<br/>
    │   ├── __init__.py<br/>
    │   └── main.py<br/>
    ├── core<br/>
    │   ├── __init__.py<br/>
    │   ├── __pycache__<br/>
    │   │   ├── __init__.cpython-36.pyc<br/>
    │   │   ├── server.cpython-36.pyc<br/>
    │   │   └── user_manager.cpython-36.pyc<br/>
    │   ├── server.py<br/>
    │   └── user_manager.py<br/>
    ├── files<br/>
    │   └── __init__.py<br/>
    └── users<br/>
        ├── 001.json<br/>
        ├── 002.json<br/>
        ├── 003.json<br/>
        ├── 004.json<br/>
        ├── 005.json<br/>
        └── __init__.py<br/>

## Requirements
    1. 用户加密认证
    2. 允许同时多用户登录
    3. 每个用户有自己的家目录 ，且只能访问自己的家目录
    4. 对用户进行磁盘配额，每个用户的可用空间不同
    5. 允许用户在ftp server上随意切换目录
    6. 允许用户查看前目录下文件
    7. 允许上传和下载文件，保证文件一致性
    8. 文件传输过程中显示进度条（显示过多，已屏蔽）
    9. 附加功能：支持文件的断点续传（暂时没实现）

## Run
	Server
        $ python ftp_server/bin/main.py
    Client
        $ python ftp_server/bin/main.py
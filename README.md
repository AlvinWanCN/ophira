<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>



# ophira
Ophira 项目是一个django+html+css+js+jquery+iView结合运用的项目，目前正在开发中。


已开发的代码已部署在https://alv.pub 上。

## 安装部署ophira

### 依赖环境

ophira使用的python版本为python2.7，django版本是1.8.2.， 使用mysql数据库。

### 下载ophira
```
# cd /opt/
# git clone https://github.com/AlvinWanCN/ophira.git
# cd ophira

```

### 配置数据

#### 修改数据库地址或设置本地解析

源代码中设置的连接数据库的地址是maxsclae.alv.pub,配置在ophira/ophira/settings.py里面。
我们可以修改数据库地址，或设置一个本地解析将maxscale.alv.pub 解析为我们自己的数据库ip。
```
# vim ophira/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ophira',
        'HOST': 'maxscale.alv.pub',
        'USER': 'alvin',
        'PASSWORD': 'sophiroth',
        'PORT': 4006

    }
}
```
#### 创建数据库

这里的数据库账号，根据实际情况设置
```
CREATE DATABASE `ophira` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
grant all privileges on ophira.* to 'alvin'@'%' identified by 'sophiroth';
```

### 安装依赖包

sudo yum install mysql-devel
sudo yum install python-devel
sudo pip install django=1.8.2
sudo pip install django-cors-headers
sudo pip install pymysql
sudo pip install MySQL-python

### 同步数据库

```
python  manage.py  validate/check  #检测数据库配置是否有错 旧版本是vilidate,新新版是check

python  manage.py  makemigrations  #创建对应数据库的映射语句

python  manage.py  syncdb   同步或者映射数据库
```

### 启动服务

```
echo '
[Unit]
Description=The Sophiroth Service
After=syslog.target network.target salt-master.service

[Service]
Type=simple
User=alvin
WorkingDirectory=/opt/ophira
ExecStart=/usr/bin/python2 manage.py runserver 0.0.0.0:8001
KillMode=process
Restart=on-failure
RestartSec=3s

[Install]
WantedBy=multi-user.target graphic.target
' > /usr/lib/systemd/system/ophira.service

systemctl start ophira
systemctl enable ophira

```

### 访问
http://localhost
---
title: 搭建私有vpn
date: 2019-10-31 10:16:19
tags:
---

# 搭建私有vpn

## 申请vps服务器

vps服务器供应商有很多，更具性价比选择，常用的vultr，对低配置5$/month，可以满足vpn搭建需要，还可以跑个web应用

### vultr 账号申请申请

- 注册vultr账号

注册官网www.vultr.com，邮箱注册，要认证以后才能申请服务器实例。

- 充值支持支付宝，微信。

优惠政策看供应商营销策略

### 初始化服务器实列

- 选择机房，可以通过ping工具查看各个机房的延迟丢包情况，选择网络最好的就可以了
  
建议美国洛杉矶线路机房

- 建议选择centos-6系统，工具支持完善

不需要系统版本太高的，因为很多工具安装会有小问题，centos-6比较稳定，有成熟的错误解决方案

- 申请好服务器以后，可以在控制台查看服务器实例信息

IP地址，root密码等，通过ssh登陆服务器要用

- windows可以通过xshell、mac直接终端命令工具可登陆

### 升级python，安装pip

- 系统默认python版本过低，需要先升级python版本

centos-6 系统支持的python是2.6版本，需要升级，否则安装shadowsocks失败
```shell
# 安装之前需要，先安装相关依赖
yum install zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel
# 下载 最新版本
wget http://python.org/ftp/python/2.7.17/Python-2.7.17.tgz
# 解压
tar -xvf Python-2.7.17.tgz
cd Python-2.7.17
./configure --prefix=/usr/local/python2.7.17
make
make install
# 老版本要保留，修改链接路径
mv /usr/bin/python /usr/bin/python.old
ln -s /usr/local/python2.7.17/bin/python2.7 /usr/bin/python

# 查看python版本
python –V

# 修改yum配置，否者yum无法正常运行
vim /usr/bin/yum
# "#!/usr/bin/python" 修改为 "#!/usr/bin/python2.6"
```

- 安装pip
```shell
# 下载安装脚本
wget https://bootstrap.pypa.io/get-pip.py

# 执行安装
python get-pip.py

# 添加pyhon bin 到环境变量
vim /etc/profile
# 添加 "export PATH=$PATH:/usr/bin/python/bin"
```

## 安装shadowsocks

- 通过pip工具，安装python的shadowsocks，选择python版本是因为安装简单
  
```shell
pip install shadowsocks
```

- 配置shadowsocks配置文件，规划端口密码

```shell
vim /etc/shadowsocks.json
# 单用户配置
{
    "server":"0.0.0.0",
    "server_port":8989,
    "local_address":"127.0.0.1",
    "local_port":1080,
    "password":"123456",
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open":false
}
# 多用户配置
{
    "local_address":"127.0.0.1",
    "local_port":1080,
    "server":"0.0.0.0",
    "port_password":{      
      "8989":"password0",  
       "8990":"password1",  
     },
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open":false
}
```

- 服务器后台启动和停止shadowsocks
  
```shell
ssserver -c "/etc/shadowsocks.json" -d start
ssserver -c "/etc/shadowsocks.json" -d stop
```

- 服务器防火墙暴露服务
  
  初始的服务器是不对外暴露用户自定义端口的，这里需要配置一下防火墙，centos防火墙默认是iptables
  
  ```shell
  # 新增
  iptables -I INPUT -p tcp --dport 6666 -j ACCEPT
  # 保存修改
  service iptables save
  # 服务重启生效
  service iptables restart
  ```

## 安装serverspeeder 加速器

安装好shadowsocks，会发现下行速度很慢，不能忍受，可以尝试安装加速器，可以选择BBR，serverspeeder等

BBR是google的加速工具，这里选择serverspeeder，安装容易，提升速度明显

- 加速器对系统内核有限制

```shell
# 查看内核版本
cat /proc/version
# 下载内核版本
wget http://ftp.scientificlinux.org/linux/scientific/6.6/x86_64/updates/security/kernel-2.6.32-504.3.3.el6.x86_64.rpm
# 安装内核
rpm -ivh kernel-2.6.32-504.3.3.el6.x86_64.rpm -–force
# 重启
reboot
# 检查内核版本
cat /proc/version
# 下载安装脚本
wget -N –no-check-certificate https://github.com/91yun/serverspeeder/raw/master/serverspeeder.sh
# 执行安装
bash serverspeeder.sh
```

## 安装shadowsocks客户端

- windows客户端
  
```html
https://github.com/shadowsocks/shadowsocks-windows/releases?after=2.5.1
```

- linux客户端

```html
https://github.com/shadowsocks/shadowsocks-qt5/wiki/Installation
```

- android

```html
https://github.com/shadowsocks/shadowsocks-android/releases
```

- ios客户端

```html
# ios Appstore 搜索shadowsocks
# 应用被下架，可以切换到国外商店搜索试试
# 应用被下架可以通过pp助手
```

- mac客户端
  
```html
https://github.com/shadowsocks/ShadowsocksX-NG/releases
```
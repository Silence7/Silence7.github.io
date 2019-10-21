---
title: centos安装mysql相关
date: 2019-10-22 17:59:06
tags:
---

#### 下载rpm文件

地址：https://dev.mysql.com/downloads/repo/yum/。选择对应版本下载。

#### 安装

- 安装mysql源
```shell
yum -y localinstall mysql80-community-release-el7-1.noarch.rpm
```

- 在线安装mysql
```shell
yum -y install mysql-community-server
```

- 启动mysql服务
```shell
systemctl start mysqld
```
- 设置开机启动mysql
```shell
systemctl enable mysqld
systemctl daemon-reload
```
- 修改root本地登录密码
```shell
vim /var/log/mysqld.log
```
- 登录
```shell
mysql -u root -p
```
- 修改密码
```shell
ALTER USER 'root'@'localhost' IDENTIFIED BY 'JiangSu@2018';
```
- 查看密码策略规则
```shell
SHOW VARIABLES LIKE 'validate_password%';
```
- 修改密码策略
```shell
set global validate_password.check_user_name=OFF;
set global validate_password.policy=LOW;
set global validate_password.length=4;
flush privileges;
```

- 设置允许远程登录
```shell
update user set Host='%' where User='root';

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
```
- 更改密码加密方式
```shell
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root';
```
- 创建用户
```shell
create user zhangsan identified by 'zhangsan';
```
- 授权
```shell
grant all privileges on zhangsanDb.* to zhangsan@'%' identified by 'zhangsan';
flush privileges;
```
---
title: mysql相关
date: 2019-10-22 17:59:06
tags:
---

## 下载rpm文件

地址：https://dev.mysql.com/downloads/repo/yum/。选择对应版本下载。

## 安装

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

## mysql命令行操作相关

- 登录
  
  ```shell
  mysql -u root -p
  ```

- 数据库选择相关操作
  
  ```shell
  show databases;
  use database;
  show tables;
  desc table;
  show create table table_name;
  show create table table_name\G
  # 修改表字段
  alter table table_name add clume bigint(20) unsigned DEFAULT NULL COMMENT '商品销售码';
  ```

- 导入导出数据库表结构和数据

```shell
# 导出
mysqldump -h 127.0.0.1 -u iaas_nsd -p ddos_clean > ddos_clean.sql
# 导入
source /data/ddos_clean.sql
```

## Macos 安装mysql

- 下载

```shell
# 地址 https://dev.mysql.com/downloads/mysql/
# 选择对应os的版本
# Macos下载dmg格式
```

- 安装

```shell
# 双击 dmg工具包，默认安装
# 安装完成以后，会提示默认的root账号和随机密码，需要记下
```

- 系统配置

```shell
# 打开系统偏好设置，搜索mysql 设置 start mysql server 运行状态
```

- 终端登录mysql

```shell
# 添加环境变量：PATH="$PATH":/usr/local/mysql/bin
# mysql -u root -p
# 输入安装结束以后生成的随机的密码
# 设置新密码，否则会执行命令会报错
# set PASSWORD =PASSWORD('root');
```

- 忘记密码的解决方式

```shell
# 第一步
# 打开系统偏好设置，搜索mysql 设置 start mysql server 运行状态
# 第二步
# cd /usr/local/mysql/bin
# sudo su
# ./mysqld_safe --skip-grant-tables &  ---mysql会自动重启
# 第三步
# ./mysql -p
# FLUSH PRIVILEGES
# SET PASSWORD FOR 'root'@'localhost' = PASSWORD('你的新密码');
# 或者 update mysql.user set authentication_string=password('root') where user='root' and Host ='localhost';
```

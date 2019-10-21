---
title: centos-7防火墙设置
date: 2019-10-22 17:58:20
tags:
---

#### 虚拟机centos7默认防火墙

Centos7.0 默认使用firewall作为防火墙
```shell
systemctl stop firewalld.service  #停止firewall

systemctl disable firewalld.service #禁止Firewalls开机启动

firewall-cmd --list-ports

firewall-cmd --zone=public --add-port=80/tcp --permanent

–zone #作用域

–add-port=80/tcp #添加端口，格式为：端口/通讯协议

–permanent #永久生效，没有此参数重启后失效

firewall-cmd --reload #重启firewall

```
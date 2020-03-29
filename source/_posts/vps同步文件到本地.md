---
title: vps同步文件到本地
date: 2020-03-27 22:38:34
tags:
---

## vps下载到本地网速慢到问题

- lrzsz命令

> 速度限制，很慢

- ftp下载

> ftp 网络延迟影响比较大，速度慢

- Rsync 工具

> Rsync 底层是否也是依赖Sftp协议，传输文件会比较慢，还未尝试效果。参考： https://www.digitalocean.com/community/tutorials/how-to-use-rsync-to-sync-local-and-remote-directories-on-a-vps

- 选择近节点vps作为中转

> 同一家vps内网很快，但是延迟相差不大，速度改善不大
> 已经尝试日本节点, 速度慢，不可接受
> 备选一 tencent 香港节点转存
> 备选二 七牛云 七牛云方案： https://www.xiaoz.me/archives/3763

- 选择google网盘作为中转

> vps上传到google网盘速度很快，可以跑到2MB/s。网盘下载速度还可以，受本地带宽限制，和翻墙代理延迟到限制。速度可达到300kb/s，勉强可以接收

- 选择百度网盘作为中转

> 百度网盘同步工具，百度云下载也有限速，不可取。同步工具： https://github.com/houtianze/bypy

- HTTP服务器文件下载

> cloud-torrent 可以浏览器下载文件，这里直接访问vps下载文件，速度完全依赖，本地网络带宽资源

- BTSync 点对点的文件同步

> 需要下载安装客户端软件，要翻墙，下载地址： https://www.getnas.com/resilio-sync/
> 这种方式还未尝试效果

- HTTP服务多线程的方式

> 服务端尝试nginx搭建http服务： http://blog.bjdch.org/2015/05/2006
> 本地客户端可尝试百度云离线下载，迅雷离线下载
> python 多线程客户端下载

- 网络加速

> 装锐速、net-speeder

### vps上传同步到google网盘

> 详细介绍： https://www.moerats.com/archives/583/

```shell
# 同步google网盘，使用shicka工具
# 安装git
# 安装Go
# 安装shicha
go get github.com/google/skicka
mv /root/go/bin/skicka /usr/local/bin
skicka init # 初始化，生成/root/.skicka.config文件
# 配置google网盘授权
# google 应用配置授权地址 https://console.developers.google.com/apis
# 获取到clientID 与clientSecretKey
# 修改替换/root/.skicka.config 文件中到配置
skicka -no-browser-auth ls
# 浏览器访问，返回的链接，授权以后返回认证码，输入以后就完成设备应用的到授权
```

### shicka命令介绍

```shell
#列举文件
skicka ls

#查看网盘大小
skicka df

#查看文件夹文件及大小
skicka du ${文件夹名}

#上传文件至网盘
skicka upload ${本地文件} ${网盘路径}

#从网盘下载文件至本地
skicka download ${网盘文件} ${本地目录}

#创建文件夹
skicka mkdir ${文件夹名}

#删除文件夹
skicka rm -r ${文件名}

#删除文件
skicka rm ${文件名}

```

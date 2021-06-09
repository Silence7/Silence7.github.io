---
title: Go开发环境相关
date: 2020-02-22 17:03:09
tags:
---

## Go开发环境相关

### linux Go安装

```shell
#32位系统下载
wget -O go.tar.gz https://dl.google.com/go/go1.13.3.linux-386.tar.gz
#64位系统下载
wget -O go.tar.gz https://dl.google.com/go/go1.13.3.linux-amd64.tar.gz

#解压压缩包
tar -zxvf go.tar.gz -C /usr/local
#设置环境变量，将以下一起复制进ssh客户端运行
mkdir $HOME/go
echo 'export GOROOT=/usr/local/go
export GOPATH=$HOME/go
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin' >> /etc/profile
source /etc/profile
#查看go版本，有输出即为安装成功
go version
```

### Go依赖工具下载代理

```shell
# 设置镜像代理
go env -w GOPROXY=https://goproxy.cn,direct

# 七牛云
https://goproxy.cn

# 阿里云
https://mirrors.aliyun.com/goproxy/

# goproxy.io
https://goproxy.io
```

### Go各平台编译相关命令

```shell
# mac 系统编译linux、windows
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build test.go
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build test.go

# linux 系统编译mac、windows
CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build test.go
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build test.go

# Windows 系统编译mac、Windows
SET CGO_ENABLED=0SET GOOS=darwin3 SET GOARCH=amd64 go build test.go
SET CGO_ENABLED=0 SET GOOS=linux SET GOARCH=amd64 go build test.go
```

### Go开发工具安装

- Go版本安装

- vscode安装

- Go扩展插件安装

```shell
# go的扩展插件下载依赖到golang.org/x包，直接下载会超时
# 先手动下载 tools lint 包
cd $GOPATH
cd src
mkdir golang.org
cd golang.org
mkdir x
cd x
git clone https://go.googlesource.com/sys
git clone https://go.googlesource.com/tools
git clone https://go.googlesource.com/lint
git clone https://go.googlesource.com/mod
git clone https://go.googlesource.com/xerrors
git clone https://go.googlesource.com/text
# git clone git@github.com:golang/tools.git
# git clone git@github.com:golang/lint.git
# vscode 插件参考官方 https://github.com/Microsoft/vscode-go/wiki/Go-tools-that-the-Go-extension-depends-on
# vscode 执行 ctrl+shift+p 执行Go:install update tools 一键安装会失败
# 可以手动安装
cd $GOPATH
# windows 用户使用 go get -u -ldflags -H=windowsgui github.com/stamblerre/gocode
go get -u github.com/stamblerre/gocode
go get -u github.com/ramya-rao-a/go-outline
go get -u github.com/newhook/go-symbols
go get -u github.com/uudashr/gopkgs/cmd/gopkgs
go get -u -v golang.org/x/tools/cmd/guru
go get -u -v golang.org/x/tools/cmd/gorename
go get -u github.com/sqs/goreturns
go get -u -v github.com/rogpeppe/godef
go get -u -v golang.org/x/tools/cmd/godoc
go get -u -v golang.org/x/lint/golint
go get -u -v github.com/go-delve/delve/cmd/dlv
go get -u github.com/fatih/gomodifytags
go get -u github.com/haya14busa/goplay/cmd/goplay
go get -u github.com/josharian/impl
go get -u github.com/tylerb/gotype-live
go get -u github.com/cweill/gotests/...
go get -u github.com/sourcegraph/go-langserver
go get -u github.com/davidrjenni/reftools/cmd/fillstruct

# 如果出现git clone SSL 相关的错误，可以尝试登录 github
```

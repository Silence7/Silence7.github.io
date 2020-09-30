---
title: Go modules基本使用
date: 2020-08-25 19:13:11
tags:
---

## Golang官方包管理工具

### 依赖版本

```shell
# go version 1.11 以上
# 控制环境变量 GO111MODULE
# 查看
go env
```

### 开启使用

```shell
# windows
set GO111MODULE=on
set GO111MODULE=off
set GO111MODULE=auto

# mac、linux 开启
export GO111MODULE=on
export GO111MODULE=off
export GO111MODULE=auto

```

### 命令介绍

```shell
# 项目初始化
cd project
go mod init project
```

### 下载依赖

```shell
go mod download
```

### 导入依赖

```shell
go mod vendor
```

### 更新依赖

```shell
go mod tidy
go mod download
go mod vendor
```

### 查看依赖

```shell
go list -m all
```

### 格式化mod文件

```shell
go mod edit -fmt
```

### 查看依赖关系图

```shell
go mod graph
```

### 校验依赖

```shell
go mod verify
```

### 移除依赖

```shell
# 修改go mod文件
go mod edit --droprequire=golang.org/x/crypto

# 更新修改以后的依赖
go mod tidy
```

### 修改依赖

```shell
# 查看可以升级的依赖版本
go list -u -m all

# 升级
go get -u rsc.io/quote

# 升级到指定版本
go get -u=patch rscio/quote

# 升级控制版本
go get foo@'<v1.6.2'

# 新增某个依赖
go mod edit --require=rsc.io/quote@latest # 下载最新
go mod edit --require=rsc.io/quote@v3.1.0
```

### 修改引用源

```shell
go mod edit --replace=old[@v]=new[@v]
go mod edit --replace=golang.org/x/image@v0.0.0-20180708004352-c73c2afc3b81=github.com/golang/image@v0.0.0-20180708004352-c73c2afc3b81

replace (

golang.org/x/crypto => github.com/golang/crypto v0.0.0-20190313024323-a1f597ede03a

golang.org/x/sys => github.com/golang/sys v0.0.0-20190318195719-6c81ef8f67ca

golang.org/x/text => github.com/golang/text v0.3.0

golang.org/x/lint => github.com/golang/lint v0.0.0-20190409202823-959b441ac422

golang.org/x/time => github.com/golang/time v0.0.0-20190308202827-9d24e82272b4

golang.org/x/tools => github.com/golang/tools v0.0.0-20190529010454-aa71c3f32488

golang.org/x/oauth2 => github.com/golang/oauth2 v0.0.0-20190523182746-aaccbc9213b0

golang.org/x/net => github.com/golang/net v0.0.0-20190318221613-d196dffd7c2b

golang.org/x/exp => github.com/golang/exp master

cloud.google.com/go => github.com/googleapis/google-cloud-go master

google.golang.org/genproto => github.com/google/go-genproto v0.0.0-20190522204451-c2c4e71fbf69

google.golang.org/grpc => github.com/grpc/grpc-go v1.21.0

google.golang.org/appengine => github.com/golang/appengine v1.6.1-0.20190515044707-311d3c5cf937

golang.org/x/sync => github.com/golang/sync v0.0.0-20190227155943-e225da77a7e6

)
```

### 打包依赖

```shell
go mod vendor
```

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
go mod edit -replace=old[@v]=new[@v]
go mod edit -replace=golang.org/x/image@v0.0.0-20180708004352-c73c2afc3b81=github.com/golang/image@v0.0.0-20180708004352-c73c2afc3b81
```

### 打包依赖

```shell
go mod vendor
```

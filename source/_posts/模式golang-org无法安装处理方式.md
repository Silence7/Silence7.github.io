---
title: 模式golang.org无法安装处理方式'
date: 2019-06-15 12:56:46
tags:
---

## go mod 依赖无法识别

```go
golang.org/x/crypto@v0.0.0-20181127143415-eb0de9b17e85: unrecognized import path "golang.org/x/crypto"
golang.org/x/net@v0.0.0-20181114220301-adae6a3d119a: unrecognized import path "golang.org/x/net"
```

1. 手动加入被墙的包（原始包），一定要记住版本号，实在不知道的话，就试试v0.0.0；

```go
go mod edit -require=golang.org/x/net@v0.0.0
```

2. 用github上的镜像地址替换

```go
go mod edit -replace=golang.org/x/crypto@v0.0.0=github.com/golang/crypto@latest
```

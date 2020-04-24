---
title: Go语言编程规范
date: 2020-04-17 14:06:54
tags:
---

## 介绍

> 这篇Blog总结Go语言在使用中需要遵守的规则, 这些规定一定是在平时的项目中遇到过疑惑的问题点

在开始使用Go语言之前，需要选择一款比较合适的编辑器，推荐Goland，Vscode。设置保存运行goformat、goimports 优化代码排版和模块的管理，使用 golint 和 go vet 去做错误检测。

### 指针和值的区别

```go
type conn struct {
    value string
}

func (p *conn)Get() string {
    return value
}

func (p *conn)Set(v string) {
    p.value = v
}

func (p conn)Get() string {
    return value
}

func (p conn)Set(v string) {
    p.value = v
}
```

### slice和map的引用

```go
// slice 做参数

// slice 做返回值

// map 做参数

// map 做返回值

```

### mutex的使用

> mutex 对象尽量使用非指针对象，初始化0值的mutex也是合法的，而指针对象需要对nil做判断

```go
// good
var m sync.Mutex

// bad 
var m = new(sync.Mutex)
```

### 使用defer来清理资源

```go
// 文件的关闭
f, err := os.Open(filename)
if nil != err {
    return
}

// 1 没有错误处理
defer f.close()

// 2 重复的释放会报错
if nil != f {
    defer func () {
        if err:= f.close; nil != err {
            return
        }
    }()
}

// 第二个文件
f, err = os.Open(filename2)
if nil != err {
    return
}

if nil != f {
    defer func () {
        if err:= f.close; nil != err {
            return
        }
    }()
}

// 3 通过参数传递，区分对文件句柄做一次拷贝，而不是局部变量的方式
if nil != f {
    defer func (f io.Closer) {
        if err:= f.close; nil != err {
            return
        }
    }(f)
}

// 第二个文件
f, err = os.Open(filename2)
if nil != err {
    return
}

if nil != f {
    defer func (f io.Closer) {
        if err:= f.close; nil != err {
            return
        }
    }(f)
}

```

### 按需申请channel的size大小

```go
```

### 类型转换的问题

```go
```

### 尽量不要使用panic

```go
```

### string类型转换

> 尽量使用strconvt

## 编程风格类

### package的命名风格

> 全部小写，不包含大写字母下划线
> 不要使用复数
> 不要使用高频的常用词汇

### 函数的声明顺序按照被调用的顺序

```go
```

### slice的nil值是合法的

```go
```

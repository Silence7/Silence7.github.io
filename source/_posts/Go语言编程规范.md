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
// slice 引用是slice结构体的copy
// 是否需要对slice做全局修改
// 需要全局修改，则引用slice指针，append操作在同一个slice上
// 不需要全局修改，则引用slice时指定len、cap属性，在append操作时会扩展为其他内存，防止修改同一个内存区，最好的方式时从原始slice新copy出来

// s在函数内部的操作，并不能引起外部s的同步修改
func AddSlice1(s []string, value string) {
    s = append(s, value)
}

// 函数内存操作的s与外部的是同一个
func AddSlice2(s *[]string, value string) {
    s = append(s, value)
}

// 不需要传递指针，修改的是同一个内存区
func ModSlice(s []string, index int, value string) {
    s[index] = value
}

// map 引用
// map 引用传递的是指针
// 不需要传递map的指针，所有的修改都是全局的
func AddMap(m [string]string, key string, value string) {
    m[key] = key
}
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

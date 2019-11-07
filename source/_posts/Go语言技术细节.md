---
title: Go语言技术细节
date: 2019-11-08 14:22:09
tags:
---

# Go语言技术细节

## 数据结构

### string

- 底层数据结构

```go
type stringStruct struct {
	str unsafe.Pointer
	len int
}
```

- go语言中的string默认是utf-8编码，表示Unicode编码用rune类型。

- string比较，按照字节进行比较

- string的追加

```go
str := "hello"
str += " world" // str 底层空间不够，会生成一个新的字符串

// 更好的表示
var buff bytes.Buffer
buffer.WriteString("hello world.")
```

- string的迭代

```go
for index, str := range("hello") {
    fmt.Printf("index:%d str:%s", index, str)
}
```

### slice

- 数据结构

```go
type slice struct {
	array unsafe.Pointer
	len   int
	cap   int
}
```

- 常见用法
  
```go
// 初始化
var s []string  // 为初始化值为nil, len=0 cap=0
var s = []string{"hello", "world"}
var s = make([]string, 0) // var s = []string{}, len = 0 cap = 0
var s = make([]string, 1, 1) // cap 参数可以省略掉, 默认是len

// 区间表示
var s = []string{"hello", "world", "golang"}
s[1:3] // 表示s索引 1-2
s[1:]  // s索引 1-len 
s[:2]  // s索引 0-1
s[:]   // s索引 0-len

// append 操作
var s []int // == nil
s = append(s, 1) // 分配内存
```

- 使用注意点

```go
// 1. 有效数组的引用,需要copy
var s []bytes = make([]bytes, 1024)
var d []bytes = make([]bytes, 10)
// copy 在底层引用的原始数据地址不同, 避免了切片重叠
copy(s[0:10], d) // 引用s数组的 0-9, 并copy到d, s会被回收掉, 避免内存浪费
```
```go
// 2. 切片引用被同一个内存区域, 被同步修改
var a = make([]int, 0, 10)
b := append(a, 1) // b和a引用同一个内存区
a := append(a, 2) // _ := append(a, 2) append操作修改了a的内存, 而间接导致b也被修改
fmt.Println(b[0]) // 结果: 2
```
```go
// 3. 如何避免重新分配的切片不被修改, 分配切片,指定len=cap
var a = []int{1, 2, 3, 4, 5}
b := a[0:2]  // 这里 b 切片 len 2, cap 5, 在append 操作的时候, 引用的是同一个内存区
// b := a[0:2:2] // 这里指定b切片的cap, 在append 操作的时候, 会重新分配内存
b = append(b, 0)
fmt.Println(a)
```
```go
// 4. 重新分配的切片 len, cap
var a = make([]int, 5, 10) // a len = 5, cap = 10
b := a[0:2]  // b len = 2, cap = 10
c := a[2:]  // c len = 3, cap = 7
```
```go
// 5. 如何避免重新分配内存,导致性能低
// 预分配
// 共享ptr 和 cap
var cache = make([]int, 0, 100)
r = cache[0:0]  // 这里 r 每次调用 都将r ptr 指向 cache ptr, r cap = cache cap 
r = append(r, 1)
```

### map

- 数据结构

- 常见用法

- 使用注意点

### interface

- 数据结构

- 常见用法

- 使用注意点

### struct

- 数据结构

- 常见用法

- 使用注意点

### channel

- 数据结构

- 常见用法

- 使用注意点

### defer函数原理

### 错误处理

## 内存管理

- 数据结构

- 常见用法

- 使用注意点

### 内存模型

### 内存分配

### 内存回收

## Goruntine原理
---
title: Go语言技术细节
date: 2019-11-08 14:22:09
tags:
---

## Go语言技术细节

### 数据结构

#### string

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

#### slice

> 切片是对数组片段的引用，是引用类型

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
// 数组的申明
var a = [3]int{0,1,2} // 指定数组长度3
var b = [...]int{0,1,2,3} // 推断数组长度4

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

```go
// 6. 删除操作
// silce没有delete接口，实现删除操作，原理上是将删除元素的前后元素连接起来，可以使用append操作
```

#### map

- 数据结构

- 常见用法

- 使用注意点

#### interface

在Golang体系中，interface是实现多态的方式，它是一个静态类型，在运行时态动态转换。

- 数据结构

```go
// 底层数据结构对应 有接口函数的接口类型
type iface struct {
    tab  *itab           // 类型信息以及类型实现的方法集合信息
    data unsafe.Pointer  // 指向类型数据指针
}

// 底层数据结构对应 空接口类型
type eface struct {
    _type *_type         //指向类型信息
    data  unsafe.Pointer //指向类型数据指针
}
```

- 常见用法

```go
func Search(src interface{}) {
    // 1. 类型断言
    isrc, ok := src.(int) // 此处没有ok， 会有panic错误
    if ok {
        Printlin(isrc)
    }

    // 2. 多种类型断言
    switch src.(type) {
        case int:
        case string:
        default:
    }
}
// -----------分割线-------------
type Animal interface{
    Run()
}

type Cat struct{

}

func (o *Cat)Run(){
    Println("Cat Run")
}

type Dog struct{

}

func (o *Dog)Run(){
    Println("Dog Run")
}

func Run(animal Animal) {
    animal.Run()
}

// 3. 多态实现
var animal Animal
animal = &Cat{}
animal.Run() // Cat Run
animal = &Dog{}
animal.Run() // Dog Run
```

- 使用注意点

实现接口方法时，对象传递统一为指针，避免出错

```go
type Animal interface{
    Run()
}

type Cat struct{

}

// 这里传入是实体不是指针
func (o Cat)Run(){
    Println("Cat Run")
}

type Dog struct{

}

// 这里是指针
func (o *Dog)Run(){
    Println("Dog Run")
}

func Run(animal Animal) {
    animal.Run()
}

var cat Cat
var dog Dog
Run(cat)
Run(dog) // 编译报错
Run(&cat) // 这里指针传递给了实体，不会报错，go语言隐试转换。指针可以转换为实体，实体不能转换为指针
Run(&dog)
```

#### struct

- GO语言关键字，可以自定义类型

```go
// struct与stuct之间没有继承的概念，是通过组合完成对属性的继承。
// struct对interface采用隐式实现，这里要防止接口滥用的情况，应为只要实现接口的方法，就可以隐式转换，而接口与接口之间是不可以转换的
type Profile struct {
    Age string
    Sex string
}

type User struct {
    Profile  // 匿名组合的方式，User拥有Profile的属性
}
```

- 常见用法

```go
type Data struct {
    Name string `json: name`  // 首字母大写多外部可见 格式化字段约定 "name"
    age  int                  // 对外部不可见
}

type Func struct{

}

func (o *Func)Action(){
    Println("Action print")
}

type People struct{
    data Data   // 显示
    Func        // 匿名继承
}
```

- 使用注意点

```go
// 1. 初始化
var data = Data{Name: "tom"}
// 2. 空结构体
var data = Data{}
// 3. 结构体赋值
var data = Data {
    Name: "tom",   // ","不能省略
}
```

#### channel

- 数据结构

```go
type hchan struct {
    qcount   uint           // total data in the queue
    dataqsiz uint           // size of the circular queue
    buf      unsafe.Pointer // points to an array of dataqsiz elements
    elemsize uint16
    closed   uint32
    elemtype *_type // element type
    sendx    uint   // send index
    recvx    uint   // receive index
    recvq    waitq  // list of recv waiters
    sendq    waitq  // list of send waiters

    // lock protects all fields in hchan, as well as several
    // fields in sudogs blocked on this channel.
    //
    // Do not change another G's status while holding this lock
    // (in particular, do not ready a G), as this can deadlock
    // with stack shrinking.
    lock mutex
}

// 阻塞队列，双向链表
type waitq struct {
    first *sudog
    last  *sudog
}
```

- channel 发生数据流程

```shell
# 条件发送协程G1，接收协程G2，chan阻塞式
# G1开始发送数据，chan 此时不可写，G1被加入chan sendq队列，runtime调度G1阻塞
# 如果chan 此时可写，检查recvq队列是否有协程G2阻塞等待，如果有数据拷贝到G2协程数据缓存区
# 如果没有协程在recvq队列，则加锁chan，数据拷贝到chan buf，sendx++，解锁

# 如果协程是非阻塞的，chan 队列满时会阻塞
```

- channel 接受数据流程

```shell
# 条件发送协程G1，接收协程G2，chan阻塞式
# G2接收数据，chan此时不可读，G2被加入chan recvq队列，runtime调度G2阻塞
# 如果chan可读，加锁chan，数据拷贝到G2缓存区，recvx++，解锁
```

- 常见用法

- 使用注意点

#### defer函数原理

> defer延迟函数，defer后的函数语句延迟到当前函数返回时执行，多个defer语句的执行顺序是按照申明的逆序，类似栈的顺序。
> defer函数的执行过程

```shell
# defer机制分为deferproc和deferreturn
# deferproc是在函数执行流中调用，执行流程如下
# 申请defer对象结构体，把结构体挂载到当前goruntime的G对象defer链上
# 保存defer调用的函数地址和参数到defer结构体中
# 返回到调用deferproc的地方，执行后面的语句

# deferreturn是在函数return处理中调用，执行流程如下：
# 在当前goruntime的G对象defer链上找需要处理的defer函数，没有就返回
# 把defer对象中的defer执行函数和参数拷贝到当前栈上
# 释放defer对象
# 通过jmpdefer命令执行defer函数

```

> defer与return的执行顺序

```shell
# return开始，执行函数或者表达式
# 执行deferreturn
# 执行return，当前函数栈返回值整理
```

#### panic和recover

> revover 只在defer函数内使用有效，外部使用返回nil
> recover 会捕获到最近一次的panic错误，在此之前的panic会被覆盖掉，程序会正常执行

- 主动panic

```shell
# 1. panic发生以后, 程序会执行runtime.sigpanic
# 2. 开始执行在panic函数前注册的defer函数，直到某个defer函数内的recover函数被执行，执行完所有defer函数以后，继续正常流程执行。 如果没有recover函数，执行完defer以后退出程序
# 3. panic嵌套, panic发生以后，开始执行defer，如果在defer又发生panic，就是panic嵌套，panic会产生对应panic结构，在当前g对象的panic对象链表，最近产生的在链表前，最开始的在链表尾部
```

```go
package main

import "fmt"

func main() {
    f()
    fmt.Println("main")
}

func f() {
    defer catch("f")

    defer func() {
        panic("defer panic")
    }()

    fmt.Println("f call")
    panic("f panic")
    fmt.Println("f continue")
}

func catch(funcname string) {
    if r := recover(); r != nil {
        fmt.Println(funcname, "recover:", r)
    }
}
```

- 被动panic

```shell
# 1. 被动panic，在程序运行时，cpu执行发现错误，比如数组和切片访问越界。
# 2. cpu发生执行错误，陷入内核处理
# 3. 内核开始异常处理，保存发生错误的执行内存地址和寄存器值，给发生异常的线程发送SIGSEGV信号
# 4. 执行程序向内核注册异常处理函数
# 5. 执行完异常处理函数以后，内核异常处理返回
# 6. 返回用户态执行runtime.sigpanic函数，过程和主动panic一样
```

### 内存管理

- 数据结构

- 常见用法

- 使用注意点

#### 内存模型

#### 内存分配

#### 内存回收

### Goruntine原理

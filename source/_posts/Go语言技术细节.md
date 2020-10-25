---
title: Go语言技术细节
date: 2019-11-08 14:22:09
tags:
---

## Go语言技术细节

### 基本数据类型

#### string

##### 数据结构

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

##### 数据结构

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

##### 注意事项

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

##### 数据结构

```go
type hmap struct {
    count        int  //元素个数
    flags        uint8
    B            uint8 //扩容常量
    noverflow    uint16 //溢出 bucket 个数
    hash0        uint32 //hash 种子
    buckets      unsafe.Pointer //bucket 数组指针
    oldbuckets   unsafe.Pointer //扩容时旧的buckets 数组指针
    nevacuate    uintptr  //扩容搬迁进度
    extra        *mapextra //记录溢出相关
}
```

> 每个map底层对应一个hmap结构，key值保存在buckets 对象数组中，每个bucket默认保存8个key，溢出(溢出不是满了，是hash冲突以后积累的)以后extra会扩展链接新的bucket

- key的hash

1. tophash会计算key的hash值，依赖golang对每种类型实现的hash和equal

- key的查找

1. 如果有并发查找，就抛出异常
2. 计算hash值，取模找到对应的bucket
3. 如果还没有迁移，就在旧buckets中找
4. 如果迁移，就在新buckets中找，找到以后取value地址
5. 如果当前bucket没有，那么就在下一链的bucket中查找

- key的更新插入

1. 检查是否需要扩容操作
2. 如果当前bucket满，新声请一个bucket
3. 找到插入key的位置，写入

- key的删除

1. 在map中找key
2. 找到对应的key值对象以后，把tophash标记设置empty，并没有真实删除数据

- map的扩容

1. 缩短扩容花费的时间，只在插入和更新的时候检查是否需要扩容
2. 每次扩容都是上一次的2倍，需要重新计算旧对象的hash值
3. 通过空间换时间，map中有新旧两个buckets数组对象

- map的并发

1. map+sync.RWMutex 自定义实现，所粒度比较大
2. sync.Map 官方工具包提供，内部采用读写两个map和锁机制实现，缺点是当写数据场景多的时候，并不会有很大优势
3. ConcurrentMap 把大map对象hash成多个小map减少锁粒度，提升性能

- map的垃圾回收

1. map删除key，只是打上删除标记，并不回收内存，所以map大小是不停增加的
2. gc回收需要把map设置nil，否则也不会回收掉

##### 常见用法

- 初始化

```go
var m map[int]string    // 定义类型，初始化nil，未分配内存，写入数据会panic
var m = make(map[int]string) // 分配内存
var m = map[int]string{}   // 初始化
```

> map的Key值有限制，必须是可比较类型。不可不计较类型有 slice，map，func

- 增、删、改、查

```go
var m = make(map[int]string)

m[0] = "add"     // 增

delete(m, 0)     // 删

d, ok := m[0]    // 查
if !ok {
    fmt.Println("key is not exist")
}

d = "update"
m[0] = d         // 改，必须重新赋值


for k, v := range m {   // 遍历map，不能保证有序
    fmt.Println("key:" + k + " value:" + v)
}

// 有序遍历，先把keys取出来，做好排序，再按照key来取值

// 函数参数传递，map是引用类型
```

##### 注意事项

1. map是无序的
2. map不是线程安全的
3. map更新操作需要重新赋值，range遍历是值拷贝

#### interface

在Golang体系中，interface是实现多态的方式，它是一个静态类型，在运行时态动态转换。

##### 数据结构

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

##### 常见用法

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

##### 注意事项

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

> GO语言关键字，可以自定义类型

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

##### 常见用法

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

##### 注意事项

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

> https://www.jianshu.com/p/24ede9e90490

##### 数据结构

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

- channel make实现

```go
func makechan(t *chantype, size int64) *hchan {
    elem := t.elem

    // compiler checks this but be safe.
    if elem.size >= 1<<16 {
        throw("makechan: invalid channel element type")
    }
    if hchanSize%maxAlign != 0 || elem.align > maxAlign {
        throw("makechan: bad alignment")
    }
    if size < 0 || int64(uintptr(size)) != size || (elem.size > 0 && uintptr(size) > (_MaxMem-hchanSize)/elem.size) {
        panic(plainError("makechan: size out of range"))
    }

    var c *hchan

    if elem.kind&kindNoPointers != 0 || size == 0 {
        // case 1: channel 不含有指针
        // case 2: size == 0，即无缓冲 channel
        // Allocate memory in one call.
        // Hchan does not contain pointers interesting for GC in this case:
        // buf points into the same allocation, elemtype is persistent.
        // SudoG's are referenced from their owning thread so they can't be collected.
        // TODO(dvyukov,rlh): Rethink when collector can move allocated objects.

        // 在堆上分配连续的空间用作 channel
        c = (*hchan)(mallocgc(hchanSize+uintptr(size)*elem.size, nil, true))
        if size > 0 && elem.size != 0 {
            c.buf = add(unsafe.Pointer(c), hchanSize)
        } else {
            // race detector uses this location for synchronization
            // Also prevents us from pointing beyond the allocation (see issue 9401).
            c.buf = unsafe.Pointer(c)
        }
    } else {
        // 有缓冲 channel 初始化
        c = new(hchan)
        // 堆上分配 buf 内存
        c.buf = newarray(elem, int(size))
    }
    c.elemsize = uint16(elem.size)
    c.elemtype = elem
    c.dataqsiz = uint(size)

    if debugChan {
        print("makechan: chan=", c, "; elemsize=", elem.size, "; elemalg=", elem.alg, "; dataqsiz=", size, "\n")
    }
    return c
}
```

- channel 发生数据流程

1. 有读协程阻塞在recvq上，channel buf为空，数据直接拷贝到读协程
2. 无读协程队列阻塞，channel buf未满，数据拷贝到channel buf
3. channel buf已满，发送协程添加到sendq上阻塞

```go
// entry point for c <- x from compiled code
//go:nosplit
func chansend1(c *hchan, elem unsafe.Pointer) {
    chansend(c, elem, true, getcallerpc(unsafe.Pointer(&c)))
}

/*
 * generic single channel send/recv
 * If block is not nil,
 * then the protocol will not
 * sleep but return if it could
 * not complete.
 *
 * sleep can wake up with g.param == nil
 * when a channel involved in the sleep has
 * been closed.  it is easiest to loop and re-run
 * the operation; we'll see that it's now closed.
 */
func chansend(c *hchan, ep unsafe.Pointer, block bool, callerpc uintptr) bool {

    // 前面章节说道的，当 channel 未初始化或为 nil 时，向其中发送数据将会永久阻塞
    if c == nil {
        if !block {
            return false
        }

        // gopark 会使当前 goroutine 休眠，并通过 unlockf 唤醒，但是此时传入的 unlockf 为 nil, 因此，goroutine 会一直休眠
        gopark(nil, nil, "chan send (nil chan)", traceEvGoStop, 2)
        throw("unreachable")
    }

    if debugChan {
        print("chansend: chan=", c, "\n")
    }

    if raceenabled {
        racereadpc(unsafe.Pointer(c), callerpc, funcPC(chansend))
    }

    // Fast path: check for failed non-blocking operation without acquiring the lock.
    //
    // After observing that the channel is not closed, we observe that the channel is
    // not ready for sending. Each of these observations is a single word-sized read
    // (first c.closed and second c.recvq.first or c.qcount depending on kind of channel).
    // Because a closed channel cannot transition from 'ready for sending' to
    // 'not ready for sending', even if the channel is closed between the two observations,
    // they imply a moment between the two when the channel was both not yet closed
    // and not ready for sending. We behave as if we observed the channel at that moment,
    // and report that the send cannot proceed.
    //
    // It is okay if the reads are reordered here: if we observe that the channel is not
    // ready for sending and then observe that it is not closed, that implies that the
    // channel wasn't closed during the first observation.
    if !block && c.closed == 0 && ((c.dataqsiz == 0 && c.recvq.first == nil) ||
        (c.dataqsiz > 0 && c.qcount == c.dataqsiz)) {
        return false
    }

    var t0 int64
    if blockprofilerate > 0 {
        t0 = cputicks()
    }

    // 获取同步锁
    lock(&c.lock)

    // 之前章节提过，向已经关闭的 channel 发送消息会产生 panic
    if c.closed != 0 {
        unlock(&c.lock)
        panic(plainError("send on closed channel"))
    }

    // CASE1: 当有 goroutine 在 recv 队列上等待时，跳过缓存队列，将消息直接发给 reciever goroutine
    if sg := c.recvq.dequeue(); sg != nil {
        // Found a waiting receiver. We pass the value we want to send
        // directly to the receiver, bypassing the channel buffer (if any).
        send(c, sg, ep, func() { unlock(&c.lock) }, 3)
        return true
    }

    // CASE2: 缓存队列未满，则将消息复制到缓存队列上
    if c.qcount < c.dataqsiz {
        // Space is available in the channel buffer. Enqueue the element to send.
        qp := chanbuf(c, c.sendx)
        if raceenabled {
            raceacquire(qp)
            racerelease(qp)
        }
        typedmemmove(c.elemtype, qp, ep)
        c.sendx++
        if c.sendx == c.dataqsiz {
            c.sendx = 0
        }
        c.qcount++
        unlock(&c.lock)
        return true
    }

    if !block {
        unlock(&c.lock)
        return false
    }

    // CASE3: 缓存队列已满，将goroutine 加入 send 队列
    // 初始化 sudog
    // Block on the channel. Some receiver will complete our operation for us.
    gp := getg()
    mysg := acquireSudog()
    mysg.releasetime = 0
    if t0 != 0 {
        mysg.releasetime = -1
    }
    // No stack splits between assigning elem and enqueuing mysg
    // on gp.waiting where copystack can find it.
    mysg.elem = ep
    mysg.waitlink = nil
    mysg.g = gp
    mysg.selectdone = nil
    mysg.c = c
    gp.waiting = mysg
    gp.param = nil
    // 加入队列
    c.sendq.enqueue(mysg)
    // 休眠
    goparkunlock(&c.lock, "chan send", traceEvGoBlockSend, 3)

    // 唤醒 goroutine
    // someone woke us up.
    if mysg != gp.waiting {
        throw("G waiting list is corrupted")
    }
    gp.waiting = nil
    if gp.param == nil {
        if c.closed == 0 {
            throw("chansend: spurious wakeup")
        }
        panic(plainError("send on closed channel"))
    }
    gp.param = nil
    if mysg.releasetime > 0 {
        blockevent(mysg.releasetime-t0, 2)
    }
    mysg.c = nil
    releaseSudog(mysg)
    return true
}
```

- channel 接受数据流程

1. channel buf为空sendq上有协程阻塞，直接拷贝数据到队列
2. channel buf不为空，从channel buf 取队头数据，移动头索引
3. channel buf不为空，sendq上有协程阻塞，读取队列头数据，唤醒阻塞的写协程，拷贝数据到buf当前索引，移动头索引

```go
// entry points for <- c from compiled code
//go:nosplit
func chanrecv1(c *hchan, elem unsafe.Pointer) {
    chanrecv(c, elem, true)
}

//go:nosplit
func chanrecv2(c *hchan, elem unsafe.Pointer) (received bool) {
    _, received = chanrecv(c, elem, true)
    return
}

// chanrecv receives on channel c and writes the received data to ep.
// ep may be nil, in which case received data is ignored.
// If block == false and no elements are available, returns (false, false).
// Otherwise, if c is closed, zeros *ep and returns (true, false).
// Otherwise, fills in *ep with an element and returns (true, true).
// A non-nil ep must point to the heap or the caller's stack.
func chanrecv(c *hchan, ep unsafe.Pointer, block bool) (selected, received bool) {
    // raceenabled: don't need to check ep, as it is always on the stack
    // or is new memory allocated by reflect.

    if debugChan {
        print("chanrecv: chan=", c, "\n")
    }

    // 从 nil 的 channel 中接收消息，永久阻塞
    if c == nil {
        if !block {
            return
        }
        gopark(nil, nil, "chan receive (nil chan)", traceEvGoStop, 2)
        throw("unreachable")
    }

    // Fast path: check for failed non-blocking operation without acquiring the lock.
    //
    // After observing that the channel is not ready for receiving, we observe that the
    // channel is not closed. Each of these observations is a single word-sized read
    // (first c.sendq.first or c.qcount, and second c.closed).
    // Because a channel cannot be reopened, the later observation of the channel
    // being not closed implies that it was also not closed at the moment of the
    // first observation. We behave as if we observed the channel at that moment
    // and report that the receive cannot proceed.
    //
    // The order of operations is important here: reversing the operations can lead to
    // incorrect behavior when racing with a close.
    if !block && (c.dataqsiz == 0 && c.sendq.first == nil ||
        c.dataqsiz > 0 && atomic.Loaduint(&c.qcount) == 0) &&
        atomic.Load(&c.closed) == 0 {
        return
    }

    var t0 int64
    if blockprofilerate > 0 {
        t0 = cputicks()
    }

    lock(&c.lock)

    // CASE1: 从已经 close 且为空的 channel recv 数据，返回空值
    if c.closed != 0 && c.qcount == 0 {
        if raceenabled {
            raceacquire(unsafe.Pointer(c))
        }
        unlock(&c.lock)
        if ep != nil {
            typedmemclr(c.elemtype, ep)
        }
        return true, false
    }

    // CASE2: send 队列不为空
    // CASE2.1: 缓存队列为空，直接从 sender recv 元素
    // CASE2.2: 缓存队列不为空，此时只有可能是缓存队列已满，从队列头取出元素，并唤醒 sender 将元素写入缓存队列尾部。由于为环形队列，因此，队列满时只需要将队列头复制给 reciever，同时将 sender 元素复制到该位置，并移动队列头尾索引，不需要移动队列元素
    if sg := c.sendq.dequeue(); sg != nil {
        // Found a waiting sender. If buffer is size 0, receive value
        // directly from sender. Otherwise, receive from head of queue
        // and add sender's value to the tail of the queue (both map to
        // the same buffer slot because the queue is full).
        recv(c, sg, ep, func() { unlock(&c.lock) }, 3)
        return true, true
    }

    // CASE3: 缓存队列不为空，直接从队列取元素，移动头索引
    if c.qcount > 0 {
        // Receive directly from queue
        qp := chanbuf(c, c.recvx)
        if raceenabled {
            raceacquire(qp)
            racerelease(qp)
        }
        if ep != nil {
            typedmemmove(c.elemtype, ep, qp)
        }
        typedmemclr(c.elemtype, qp)
        c.recvx++
        if c.recvx == c.dataqsiz {
            c.recvx = 0
        }
        c.qcount--
        unlock(&c.lock)
        return true, true
    }

    if !block {
        unlock(&c.lock)
        return false, false
    }

    // CASE4: 缓存队列为空，将 goroutine 加入 recv 队列，并阻塞
    // no sender available: block on this channel.
    gp := getg()
    mysg := acquireSudog()
    mysg.releasetime = 0
    if t0 != 0 {
        mysg.releasetime = -1
    }
    // No stack splits between assigning elem and enqueuing mysg
    // on gp.waiting where copystack can find it.
    mysg.elem = ep
    mysg.waitlink = nil
    gp.waiting = mysg
    mysg.g = gp
    mysg.selectdone = nil
    mysg.c = c
    gp.param = nil
    c.recvq.enqueue(mysg)
    goparkunlock(&c.lock, "chan receive", traceEvGoBlockRecv, 3)

    // someone woke us up
    if mysg != gp.waiting {
        throw("G waiting list is corrupted")
    }
    gp.waiting = nil
    if mysg.releasetime > 0 {
        blockevent(mysg.releasetime-t0, 2)
    }
    closed := gp.param == nil
    gp.param = nil
    mysg.c = nil
    releaseSudog(mysg)
    return true, !closed
}
```

- channel关闭

```go
func closechan(c *hchan) {
    if c == nil {
        panic(plainError("close of nil channel"))
    }

    lock(&c.lock)

    // 重复 close，产生 panic
    if c.closed != 0 {
        unlock(&c.lock)
        panic(plainError("close of closed channel"))
    }

    if raceenabled {
        callerpc := getcallerpc(unsafe.Pointer(&c))
        racewritepc(unsafe.Pointer(c), callerpc, funcPC(closechan))
        racerelease(unsafe.Pointer(c))
    }

    c.closed = 1

    var glist *g

    // 唤醒所有 reciever
    // release all readers
    for {
        sg := c.recvq.dequeue()
        if sg == nil {
            break
        }
        if sg.elem != nil {
            typedmemclr(c.elemtype, sg.elem)
            sg.elem = nil
        }
        if sg.releasetime != 0 {
            sg.releasetime = cputicks()
        }
        gp := sg.g
        gp.param = nil
        if raceenabled {
            raceacquireg(gp, unsafe.Pointer(c))
        }
        gp.schedlink.set(glist)
        glist = gp
    }

    // 唤醒所有 sender，并产生 panic
    // release all writers (they will panic)
    for {
        sg := c.sendq.dequeue()
        if sg == nil {
            break
        }
        sg.elem = nil
        if sg.releasetime != 0 {
            sg.releasetime = cputicks()
        }
        gp := sg.g
        gp.param = nil
        if raceenabled {
            raceacquireg(gp, unsafe.Pointer(c))
        }
        gp.schedlink.set(glist)
        glist = gp
    }
    unlock(&c.lock)

    // Ready all Gs now that we've dropped the channel lock.
    for glist != nil {
        gp := glist
        glist = glist.schedlink.ptr()
        gp.schedlink = 0
        goready(gp, 3)
    }
}
```

##### 常见用法

> channel状态：nil,active(可读可写),关闭

1. 使用for-range读取channel, 不需要判断chan是否关闭，如果关闭会自动退出for循环

```go
for x := range ch{
    fmt.Println(x)
}
```

2. 使用ok断言判断读取channel是否成功

```go
if v, ok := <- ch; ok { // 如果chan关闭，不使用ok断言，会panic
    fmt.Println(v)
}
```

3. 使用select读取多个channel, 如果ch为nil值会阻塞，case永远为阻塞，无论读写。普通情况下写nil chan会panic

```go
var ch = make(chan int)
select {
case ch <- 1:
case <- ch:
}
```

4. 申明channel为只读或者只写，限定协程的权限

```go
c := make(chan int)
go send(c)
go recv(c)

func send(ch chan<- int) {
    ch <- 1
}

func recv(ch <-chan int) {
    i := <- ch
}
```

5. 使用非阻塞channel，增加数据的缓存和并发

```go
var ch = make(chan int, 10)

for i := 0; i < 5; i++ {
    go func(){
        ch <- i
    }()
}

for d := range ch {
    fmt.Println(d)
}

```

6. 为select操作加上超时限制

```go
var ch = make(chan int)
select{
    case <-ch:
    case time.After(2 * time.Second)
}
```

7. 使用time实现channel无阻塞读写

```govar ch = make(chan int)
select{
    case <-ch:
    default: // 如果ch阻塞则命中default分支
}
```

8. 使用close(ch)关闭所有下游协程

```go
var ch = make(chan struct{})

go func(){
    for {
        select {
            case <- ch: //可以在外部close(ch),或者写入struct{}
            return
        }
    }
}()

time.AfterFunc(2 * time.Second, func(){
    close(ch)
    // ch <- struct{}
}())
```

9. 使用channel传递结构体的指针而非结构体

```go
var ch = make(chan *Struct) // channel中的数据是值copy，如果是对象有性能开销，传递指针可以提高性能
```

##### 注意事项

1. 关闭一个未初始化(nil) 的 channel 会产生 panic
2. 重复关闭同一个 channel 会产生 panic
3. 向一个已关闭的 channel 中发送消息会产生 panic
4. 从已关闭的 channel 读取消息不会产生 panic，且能读出 channel 中还未被读取的消息，若消息均已读出，则会读到类型的零值。
5. 从一个已关闭的 channel 中读取消息永远不会阻塞，并且会返回一个为 false 的 ok-idiom，可以用它来判断 channel 是否关闭
6. 关闭 channel 会产生一个广播机制，所有向 channel 读取消息的 goroutine 都会收到消息

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

#### 内存模型

> Golang 采用TCMalloc算法，thread caching malloc

- golang内存管理单元单元

```shell
# |------|-------------------|-------------------------------|
# |-span-|-----bitmap--------|----------arena----------------|
# |-512M-|-----16G-----------|----------512G-----------------|
# span = 512G/8K/8B = 512M span存储指针对应一个页大小，64位系统下，指针8B，golang内部虚拟页大小8K
# bitmap = 512G/8B/4 = 16G bitmap一个指针对应arena区域4个指针，指针大小事8B。bitmap一个指针中，高4位标记是否有扫描，第四位表示是否是指针
```

- span存放的是mspan对象，glang里划分了67组大小的mspan对象，每一组有对应的页数。size为0表示是大对象，会直接在堆上分配

- 内存管理模块，mcache，mcentral，mheap

1. mcache：工作线程会绑定一个mcache对象，存放了2陪的spanCLass的mspan对象，一半用于非指针对象，一半用于指针对象，加速回收时的扫描
2. mcentral：全局mspan管理，多个线程共享。一个mcentral存放一组相同大小的mspan，empty链表存储已分配的mspan，noempty链表存储未分配的mspan
3. mheap：GO程序使用一个全局的mheap对象来管理堆，mheap拥有所有大小的mcentral对象，不同大小的mcentral申请分配，不相互影响

#### 内存分配

1. 小于16KB大小的对象在mcache上分配
2. 大于16KB小于32KB的对象现在mcache上找，如果没有合适的，在mcentral上找，如果没有合适的，再向mheap申请
3. 大于32KB的对象直接由mheap对象分配

#### 内存逃逸

> golang中特有的内存逃逸分析，通过编译器分析变量是在栈上分配还是在堆上分配

- 发送逃逸的情况

1. 返回局部的指针变量
2. 在channel中传递指针
3. 在切片上存储指针和包含指针的变量
4. slice重新分配
5. 在接口上调用方法

- 逃逸分析的作用

1. 减少gc
2. 减少在堆上分配内存，在栈上分配性能更好
3. 同步锁的消除，如果执行流程加了锁，而只有一个线程使用到，会消除锁同步

#### 内存回收

- 三色标记算法

1. 根对象是协程栈上的指针对象
2. 开始gc，开启写屏障，所有根对象都是白色，把所有可达的对象入栈，并标记为灰色。
3. 从栈中取出对象，把指向的子对象入栈，子对象标记为灰色，当前对象标记成黑色
4. 重复步骤3，直到栈为空
5. 扫描写屏障过程中新生成的对象
6. 清除白色对象
7. 分批次扫描，减少STW时间

- 屏障技术

1. 1.5 采用的写屏障，在开始标记和栈re-scan的过程中会STW
2. 1.8 采用的混合屏障，避免对栈的re-scan
3. 插入屏障
4. 删除屏障

### Goruntine原理

#### 协程栈状态

- golang 协程栈初始大小2KB
- golang 协程状态
  
1. Grunnable 创建协程以后的初始状态
2. Grunning 协程运行态
3. Gsyscall 系统调用态
4. Gwaiting 协程等待执行
5. Gdead    协程释放

```shell
# 协程栈创建完成以后，状态设置Grunnable，会加入P待执行G队列
# 开始执行协程，状态转换成Grunning
# 如果发生系统调用，会切换协程态为Gsyscall
# 系统调用完成，如果不满足执行条件，会切换为Grunnable，加入P待执行G队列
# 系统调用完成，满足执行条件，会切换回Grunning
# 协程有阻塞调用，如channel，io，定时器，协程切换Gwaiting
# 协程解除阻塞以后，切换回Grunning
# 协程执行完毕，切换回Gdead，协程会存到P上的空闲G队列
```

#### 协程调度

- 协程重系统调用返回的时候
- 协程发生阻塞调用的时候
- 协程长时间执行，会发生抢占式调度，由sysmon检查系统状态的协程发起调度
- 协程调度相关的函数

1. getg() // 获取当前G信息到TLS-线程本地存储 thread local storage
2. mcall() // 切换G
3. gogo()  // 恢复执行G

- 协程调度对象

1. G: 描述协程栈信息，包括寄存器，计数器，对应的M,协程上下文缓存
2. P: 本地可执行G队列，mcache，对应的M信息，当前的G，下一个G
3. M: 线程栈信息，当前执行的G，绑定的P，当前的mcache，调度器等信息
4. 全局G队列，均衡每个P本地队列的G个数，均衡公式：min(len(GQ)/GOMAXPROCS + 1, len(GQ/2))
5. sysmon协程，检查每个P状态，GC，可回收内存，回去fd事件，抢占式调度

- 协程调度过程

1. 空闲的M分配一个P取本地G队列执行
2. G发生系统调用或者阻塞，M和P解绑，P获取空闲的M，继续执行P当前G

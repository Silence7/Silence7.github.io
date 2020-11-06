---
title: Go工具包的基本用法
date: 2019-11-18 17:27:21
tags:
---

## Go工具包的基本用法

### strconv

```go
strconv.Itoa(0)
strconv.FormatInt(0)
_, err := strconv.Atoi("0")
_, err := strconv.ParseInt("0", 10, 0)
```

### context

- context接口
  
```go
// 控制协程树
// 顶级context
ctx := context.Background()
// 传递未知context，也可以做为顶级context
ctx := context.TODO()
// 派生子context
// 派生传递值的context。context 传递key, value是线程安全，不建议隐试使用，应该显示通过函数参数传递
ctx := context.WithValue(context.Background(), key, value)
// 派生返回带有cancel函数的context
// 1. 取消函数应该当前调用函数中执行，不应该传递cancel，cancel 函数执行，会取消掉所有派生的context
ctx, cancel := context.WithCancel(context.Background())
// 派生接收deadline参数
ctx, cancel := context.WithDeadline(context.Background(), time.Now().Add(2 * time.Second))
// 派生接收超时参数
ctx, cancel := context.WithTimeout(context.Background(), 2 * time.Second)
```

- 示例用法
  
```go
func sleepRandom(fromFunction string, ch chan int) {
    defer func() {
        fmt.Println(fromFunction, "sleepRandom complete")
    }()

    seed := time.Now().UnixNano()
    r := rand.New(rand.NewSource(seed))
    randomNumber := r.Intn(100)
    sleeptime := randomNumber + 100
    fmt.Println(fromFunction, "Starting sleep for", sleeptime, "ms")
    time.Sleep(time.Duration(sleeptime) * time.Millisecond)
    fmt.Println(fromFunction, "Waking up, slept for ", sleeptime, "ms")
    if ch != nil {
        ch <- sleeptime
    }
}

func sleepRandomContext(ctx context.Context, ch chan bool) {
    defer func() {
        fmt.Println("sleepRandomContext complete")
        ch <- true
    }()

    sleeptimeChan := make(chan int)
    go sleepRandom("sleepRandomContext", sleeptimeChan)
    select {
    case <-ctx.Done():
        fmt.Println("sleepRandomContext: Time to return")
    case sleeptime := <-sleeptimeChan:
        fmt.Println("Slept for ", sleeptime, "ms")
    }
}

func doWorkContext(ctx context.Context) {
    ctxWithTimeout, cancelFunction := context.WithTimeout(ctx, time.Duration(150)*time.Millisecond)
    defer func() {
        fmt.Println("doWorkContext complete")
        cancelFunction()
    }()

    ch := make(chan bool)
    go sleepRandomContext(ctxWithTimeout, ch)

    select {
    case <-ctx.Done():
        // main call cancel(), match the case
        fmt.Println("doWorkContext: Time to return")
    case <-ch:
        //This case is selected when processing finishes before the context is cancelled
        fmt.Println("sleepRandomContext returned")
    }
}

func main() {
    ctx := context.Background()
    ctx, cancel := context.WithCancel(ctx)
    defer func() {
        cancel()
    }()
    go func() {
        sleepRandom("Main", nil)
        cancel()
        fmt.Println("Main Sleep complete. canceling context")
    }()
    //Do work
    doWorkContext(ctx)
}
```

### sync

- WaitGroup

```go
// 协程并发控制作用
// 协程间无层次关系，不够灵活
// 使用context会更好
func main() {
    wg := sync.WaitGroup{} // 不是引用类型，在函数传参时，需要使用指针
    wg.Add(100) // 这里不能设置为负值
    for i := 0; i < 100; i++ {
        go func(i int) {
            fmt.Println(i)
            wg.Done()
        }(i)
    }
    wg.Wait() // 阻塞到协程结束
}
```

- Mutex & RWMutex

```go
// Mutex 互斥锁
// 1. 在未Unlock前，再次调用Lock会死锁
// 2. 在未Lock前，调用Unlock会panic
func main() {
    var lock sync.Mutex

    lock.Lock()
    defer lock.Unlock()

    fmt.Println("Lock")
}

// RWMutex 读写锁
// 单写多读，写与读互斥，读读可共存，读写互斥
// RUnlock多于RLock会panic

func main() {
    var lock sync.RWMutex

    lock.Lock()
    fmt.Println("Lock")
    lock.Unlock()

    lock.RLock()
    lock.RLock()
    lock.RUlock()
    lock.RUlock()
    lock.RUlock() // panic
}
```

- Once

```go
// init：包初始化的时候调用
// Once：标识函数只能被执行一次, 抢占式，先到先得

func main() {
    var once sync.Once
    onceFunc := func() {
        fmt.Println("exc once")
    }

    done := make(chan bool)
    for i := 0; i < 10; i++ {
        go func() {
            once.Do(onceFunc)
            done <- true
        }()
    }
    for i := 0; i < 10; i++ {
        <-done
    }
}
```

- Cond

```go
// 完成协程间的协作
// 初始化
var lock sync.Mutex
var cond = sync.NewCond(&lock)

func main() {
    for i := 0; i < 10; i++ {
        go func(x int) {
            cond.L.Lock()         //获取锁
            defer cond.L.Unlock() //释放锁
            cond.Wait()           //等待通知，阻塞当前 goroutine

            // do something. 这里仅打印
            fmt.Println(x)
        }(i)
    }
    time.Sleep(time.Second * 1)	// 睡眠 1 秒，等待所有 goroutine 进入 Wait 阻塞状态
    fmt.Println("Signal...")
    cond.Signal()               // 1 秒后下发一个通知给已经获取锁的 goroutine
    time.Sleep(time.Second * 1)
    fmt.Println("Signal...")
    cond.Signal()               // 1 秒后下发下一个通知给已经获取锁的 goroutine
    time.Sleep(time.Second * 1)
    cond.Broadcast()            // 1 秒后下发广播给所有等待的goroutine
    fmt.Println("Broadcast...")
    time.Sleep(time.Second * 1)	// 睡眠 1 秒，等待所有 goroutine 执行完毕
}
```

- pool

```go

```

- Map

```go
// 详细原理参考，go语言技术细节
func main() {
    var sm sync.Map
    //store 方法,添加元素
    sm.Store(1,"a")
    sm.Store("1","a")
    // delete 方法，删除元素
    sm.Delete(1)
    // LoadOrStore 方法，找到了更新， 没有就添加
    if v, ok := sm.LoadOrStore(1, "b"); ok {
        fmt.Println(v)
    }
    //Load 方法，查询value
    if v, ok := sm.Load(1); ok {
        fmt.Println(v)
    }

    // 遍历
    sm.Range(func(key, value interface{}) bool {
        fmt.Println(fmt.Sprintf("key:%v value:%v", key, value))
        return true
    })
}
```

### time

#### 定时器

- time.NewTimer

```go
go func() {
    t := time.NewTimer(time.Second * 2)
    defer t.Stop()
    for {
        select {
        case <-t.C:
            fmt.Println("timer running....")
            // 需要重置Reset 使 t 重新开始计时
            t.Reset(time.Second * 2)
        case stop := <-ch:
            if stop {
                fmt.Println("timer Stop")
                return
            }
        }
    }
}()
```

- time.NewTicker

```go
go func(ticker *time.Ticker) {
    ticker := time.NewTicker(2 * time.Second)
    defer ticker.Stop()
    for {
        select {
        case <-ticker.C:
            fmt.Println("Ticker running...")
        case stop := <-ch:
        if stop {
                fmt.Println("Ticker Stop")
                return
            }
        }
    }
}()
```

### crypto

### hash

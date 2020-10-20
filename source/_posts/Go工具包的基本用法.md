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

- Mutex

- Once

- Cond

- pool

- Map

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

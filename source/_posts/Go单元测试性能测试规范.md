---
title: Go单元测试性能测试规范
date: 2019-09-20 11:08:58
tags:
---

## Go单元测试&性能测试

### 测试工具

- Go语言自带测试框架和工具。一般测试代码放在*_test.go文件中，与被测代码放于同一个包中。文件需要import testing

- 单元测试的自动生成工具 gotests
       
1. 安装
   
   代码地址： https://github.com/cweill/gotests

   安装命令：go get -u github.com/cweill/gotests

2. 使用
        
    命令行：
    
    ```go
        -all
        // 为目录下的所有文件生成测试方法

        -only string
        // 为string匹配的函数和方法生成测试方法

        -w
        // 将输出写到测试文件而不是stdout

        示例：
        gotests -only "函数名称" 文件名称.go
        gotests -all 文件名称.go
        ```

        IDE：
        ```go
        Goland:
        Code->Generate-> Empty test file
                         Test for selection
                         Test for function
                         Test for file
                         Test for package

        VsCode:
        右键 -> Go: Generate Unit Test For Function
                Go: Toggle Test Coverage In Current Package
                Go: Toggle Test File
    ```

### Go单元测试

- 单元测试编写规则

    以Test开头，跟上非小写字母开头的字符串。测试函数都接受一个*testing.T类型参数，用于输出信息或中断测试。

    示例：

    ```go

        func add(i int) int {
            return i + 1
        }

        func Test_add(t *testing.T) {
            type args struct {
                i int
        }

        tests := []struct {
            name string
            args args
            want int
        }{
            // TODO: Add test cases.
            {
                name : "",
                args : args{
                    i: 1,
                },
                want: 2
            },
        }
        for _, tt := range tests {
            t.Run(tt.name, func(t *testing.T) {
                if got := add(tt.args.i); got != tt.want {
                    t.Errorf("add() = %v, want %v", got, tt.want)
                }
            })
        }
    ```

- 单元测试命令介绍

    进入测试代码所在的目录，执行go test命令：
    -v: 显示所有测试函数运行细节
    -cover: 输出单元测试覆盖率报告
    -run regex: 指定测试的具体函数

    示例：

    ```go
    go test ./ -v -cover

    === RUN   Test_add
    === RUN   Test_add/add_success
    --- PASS: Test_add (0.00s)
    --- PASS: Test_add/add_success (0.00s)
    PASS
    coverage: 9.1% of statements
    ok      _/F_/test/simple        0.191s  coverage: 9.1% of statements
    ```

### Go性能测试

- 性能测试编写规则
  
    性能测试函数以Benchmark 开头，参数类型是 *testing.B，可与Test函数放在同个文件中。默认情况下，go test不执行Benchmark测试，必须用“-bench <pattern>”指定性能测试函数。

    示例：

    ```go
        func add(i int) int {
            return i + 1
        }

        func Benchmark_add(b *testing.B) {
            for i := 0; i < b.N; i++ { // b.N，测试循环次数
                Add(1)
            }
        }
     ```

- 性能测试命令介绍

    ```go
    go test -v -bench=.

    // 指定参数 -N=1000000
    go test -v -bench=. -cpu=8 -benchtime="3s" -timeout="5s" -benchmem

    // 指定输出cpu信息到文件
    go test -bench=. -cpuprofile cpu.out

    // 通过工具分析输出结果
    go tool pprof -text cpu.out
    ```

### Go程序设计可测试接口的一些技巧

- 有外部组件依赖的情况下，如何设计可测试的函数和方法

   1. 函数和方法内部有对外部系统的调用，如建立一个外部连接

    示例：

    ```go
    func GatherTCP(host string, port int) error {
        addr, err := net.ResolveTCPAddr("tcp", fmt.Sprintf("%s:%d",host, port))
        if err != nil {
            return err
        }
        // 此处有建立外部连接，需要mock server。不方便测试
        conn, er := net.DialTCP("tcp", nil, addr)
        if err != nil {
            return err
        }
        defer conn.Close()
        data, err := ioutil.ReadAll(conn)
        if err != nil {
            return err
        }

        return strings.EqualFold(string(data), excepted), nil
    }
    ```

    解决思路：用全局对象保存函数，可以提供外部修改

    ```go
    var DialTCP = func(network string, laddr, raddr *net.TCPAddr)(net.Conn, error) {
        return net.DialTCP(network, laddr, raddr)
    }

    func GatherTCP(host string, port int) error {
        addr, err := net.ResolveTCPAddr("tcp", fmt.Sprintf("%s:%d",host, port))
        if err != nil {
            return err
        }
        // 全局变量可以被外部修改
        conn, er := DialTCP("tcp", nil, addr)
        if err != nil {
            return err
        }
        defer conn.Close()
        data, err := ioutil.ReadAll(conn)
        if err != nil {
            return err
        }

        return strings.EqualFold(string(data), excepted), nil
    }

    ```

    2. 函数和方法需要访问外部组件，如数据库

    示例：

    ```go
    func ReadDb(db, table string, result interface) (num int, err error) {
        cond := orm.NewCondition()

        //  这里有对数据库的操作，不可测试
        err := base_opt.ReadObj(condition, db, table, result)
        if nil != err {
            return 0, err
        }

        return len(result), nil
    }
    ```

    解决思路：抽象出一层接口层，对数据库的操作可以外部实现， 这种方式扩展性会更好

    ```go
    type DBDao interface {
        ReadObj(*orm.Condition, string, string, interface{}) error
    }

    type DbService struct {

    }

    func (o *DbService)ReadObj(condition *orm.Condition, db, table string, result interface{})(err error) {
        // 这里调用数据库的访问， 外部可以实现为 return nil
        return base_opt.ReadObj(condition, db, table, result)
    }

    // 通过接口传入参数，外部可以有不同的接口实现
    func ReadDb(service DBDao, db, table string, result interface) (num int, err error) {
        cond := orm.NewCondition()

        err := service.ReadObj(condition, db, table, result)
        if nil != err {
            return 0, err
        }

        return len(result), nil
    }
    ```

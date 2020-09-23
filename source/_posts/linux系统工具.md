---
title: linux系统工具
date: 2020-09-23 11:46:35
tags:
---

## Linux系统工具集盘点

盘点linux系统工具和命令，帮助快速了解机器性能和进程相关状态，方便分析查找问题

### 系统信息

- 系统版本

```shell
cat /etc/redhat-release
```

- 内核版本

```shell
cat /proc/version
uname -a
```

- 系统事件消息

```shell
dmesg
```

### CPU信息

```shell
# 查看CPU的详细信息
cat /proc/cpuinfo

# 查看逻bai辑CPU个数
cat /proc/cpuinfo |grep "processor"|sort -u|wc -l

# 查看物理CPU个数
grep "physical id" /proc/cpuinfo|sort -u|wc -l
grep "physical id" /proc/cpuinfo|sort -u

# 查看每个物理CPU内核个数
grep "cpu cores" /proc/cpuinfo|uniq

# 每个物理CPU上逻bai辑CPU个数
grep "siblings" /proc/cpuinfo|uniq

# 判断是否开启了抄超线程
#如果多个逻辑CPU的"physical id"和"core id"均相同，说明开启了超线程，或者换句话说
# 逻辑CPU个数 > 物理CPU个数 * CPU内核数   开启了超线程
# 逻辑CPU个数 = 物理CPU个数 * CPU内核数   没有开启超线程

```

### 进程

- top 命令

```shell
# 实时查看进程资源占用情况
top -p 10101

# top进程列表信息
# PID：进程的ID
# USER：进程所有者
# PR：进程的优先级别，越小越优先被执行
# NInice：值
# VIRT：进程占用的虚拟内存
# RES：进程占用的物理内存
# SHR：进程使用的共享内存
# S：进程的状态。S表示休眠，R表示正在运行，Z表示僵死状态，N表示该进程优先值为负数
# %CPU：进程占用CPU的使用率
# %MEM：进程使用的物理内存和总内存的百分比
# TIME+：该进程启动后占用的总的CPU时间，即占用CPU使用时间的累加值。
# COMMAND：进程启动命令名称
```

- ps 命令

```shell
# 查看进程的状态执行情况
ps -ef

# F 代表这个程序的旗标 (flag)， 4 代表使用者为 super user
# S 代表这个程序的状态 (STAT)
# PID 程序的 ID
# C CPU 使用的资源百分比
# PRI 这个是 Priority (优先执行序) 的缩写；
# NI 这个是 Nice 值。
# ADDR 这个是 kernel function，指出该程序在内存的那个部分。如果是个 running # 的程序，一般就是『 - 』
# SZ 使用掉的内存大小；
# WCHAN 目前这个程序是否正在运作当中，若为 - 表示正在运作；
# TTY 登入者的终端机位置；
# TIME 使用掉的 CPU 时间。
# CMD 所下达的指令
```

- strace 命令

```shell
# 查看进程的系统调用
strace -o output.txt -T -tt -e trace=all -p 28979

# -c 统计每一系统调用的所执行的时间,次数和出错的次数等.
# -d 输出strace关于标准错误的调试信息.
# -f 跟踪由fork调用所产生的子进程.
# -ff 如果提供-o filename,则所有进程的跟踪结果输出到相应的filename.pid中,pid是各进程的进程号.
# -F 尝试跟踪vfork调用.在-f时,vfork不被跟踪.
# -h 输出简要的帮助信息.
# -i 输出系统调用的入口指针.
# -q 禁止输出关于脱离的消息.
# -r 打印出相对时间关于,,每一个系统调用.
# -t 在输出中的每一行前加上时间信息.
# -tt 在输出中的每一行前加上时间信息,微秒级.
# -ttt 微秒级输出,以秒了表示时间.
# -T 显示每一调用所耗的时间.
# -v 输出所有的系统调用.一些调用关于环境变量,状态,输入输出等调用由于使用频繁,默认不输出.
# -V 输出strace的版本信息.
# -x 以十六进制形式输出非标准字符串
# -xx 所有字符串以十六进制形式输出.
# -a column 设置返回值的输出位置.默认 为40.
# -e expr 指定一个表达式,用来控制如何跟踪.格式如下: [qualifier=][!]value1[,value2]... qualifier只能是 trace,abbrev,verbose,raw,signal,read,write其中之一.value是用来限定的符号或数字.默认的 qualifier是 trace.感叹号是否定符号.例如: -eopen 等价于 -e trace=open,表示只跟踪open调用.而-etrace!=open表示跟踪除了open以外的其他调用.有两个特殊的符号 all 和 none. 注意有些shell使用!来执行历史记录里的命令,所以要使用\\.
# -e trace=set 只跟踪指定的系统 调用.例如:-e trace=open,close,rean,write表示只跟踪这四个系统调用.默认的为set=all.
# -e trace=file 只跟踪有关文件操作的系统调用.
# -e trace=process 只跟踪有关进程控制的系统调用.
# -e trace=network 跟踪与网络有关的所有系统调用.
# -e strace=signal 跟踪所有与系统信号有关的 系统调用
# -e trace=ipc 跟踪所有与进程通讯有关的系统调用
# -e abbrev=set 设定 strace输出的系统调用的结果集.-v 等与 abbrev=none.默认为abbrev=all.
# -e raw=set 将指 定的系统调用的参数以十六进制显示.
# -e signal=set 指定跟踪的系统信号.默认为all.如 signal=!SIGIO(或者signal=!io),表示不跟踪SIGIO信号.
# -e read=set 输出从指定文件中读出 的数据.例如:
# -e read=3,5  
# -e write=set 输出写入到指定文件中的数据.
# -o filename 将strace的输出写入文件filename
# -p pid 跟踪指定的进程pid.
# -s strsize 指定输出的字符串的最大长度.默认为32.文件名一直全部输出.
# -u username 以username 的UID和GID执行被跟踪的命令
```

- pstack

```shell
# 查看进程堆栈信息
pstack -p
```

- pmap

```shell
# 查看进程内存映射使用情况
pmap
```

### 内存

```shell
# 查看系统内存大小，和使用情况
cat /proc/meminfo

# 查看系统内存，交换区使用情况
free
# total:总计物理内存的大小。
# used:已使用多大。
# free:可用有多少。
# Shared:多个进程共享的内存总额。
# Buffers/cached:磁盘缓存的大小。

# 实时查看系统cpu，内存，io等信息
vmstat -s
```

### 磁盘

```shell
# 查看磁盘分区使用情况
df -h
```

### 网络

- 常用工具

```shell
# 系统网卡统计信息
cat /proc/net/dev

# 查看系统网络统计信息，包括端口，状态信息
netstat
```

- lsof 命令

```shell
# 安装
yum install lsof

lsof -i # 查看所有连接
lsof -i 6
lsof -i TCP # 查看tcp连接
lsof -i:80 # 查看端口连接
lsof -i @localhost # 查看指定主机的连接
lsof -i @192.168.1.222:22 # 查看基于主机和端口的连接
lsof  -i -sTCP:LISTEN # 查看指定状态的连接
lsof -p 78569 # 查看指定进程ID已打开的内容
# lsof 实用命令集
lsof `which httpd` # 那个进程在使用apache的可执行文件
lsof /etc/passwd  #那个进程在占用/etc/passwd
lsof /dev/hda6 # 那个进程在占用hda6
lsof /dev/cdrom # 那个进程在占用光驱
lsof -c sendmail # 查看sendmail进程的文件使用情况
lsof -c courier -u ^zahn # 显示出那些文件被以courier打头的进程打开，但是并不属于用户zahn
lsof -p 30297 # 显示那些文件被pid为30297的进程打开
lsof -D /tmp # 显示所有在/tmp文件夹中打开的instance和文件的进程。但是symbol文件并不在列
lsof -u1000 # 查看uid是100的用户的进程的文件使用情况
lsof -utony # 查看用户tony的进程的文件使用情况
lsof -u^tony # 查看不是用户tony的进程的文件使用情况(^是取反的意思)
lsof -i # 显示所有打开的端口
lsof -i:80 # 显示所有打开80端口的进程
lsof -i -U # 显示所有打开的端口和UNIX domain文件
lsof -i UDP@[url]www.akadia.com:123 # 显示那些进程打开了到www.akadia.com的UDP的123(ntp)端口的链接
lsof -i tcp@ohaha.ks.edu.tw:ftp -r # 不断查看目前ftp连接的情况(-r，lsof会永远不断的执行，直到收到中断信号,+r，lsof会一直执行，直到没有档案被显示,缺省是15s刷新)
lsof -i tcp@ohaha.ks.edu.tw:ftp -n # lsof -n 不将IP转换为hostname，缺省是不加上-n参数
lsof -P -n | wc -l # 统计系统打开的文件总数
lsof -a -c sshd -U # 查看被打开的 UNIX domain socket 文件
```

- sar 命令

```shell
# 查看网卡流量信息
sar -n DEV 1 2

# DEV显示网络接口信息。
# EDEV显示关于网络错误的统计数据。
# NFS统计活动的NFS客户端的信息。
# NFSD统计NFS服务器的信息
# SOCK显示套接字信息
# ALL显示所有5个开关
```

- watch 命令

```shell
# 周期性监控网卡流量信息
watch -n 1 "ifconfig eth0"
```

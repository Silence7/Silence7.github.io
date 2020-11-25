---
title: redis安装配置
date: 2020-11-25 16:08:19
tags:
---

## 下载

```shell
# 下载
wget http://download.redis.io/releases/redis-5.0.10.tar.gz
# 解压
tar xzvf redis-5.0.10.tar.gz
# 编译
cd redis-5.0.10
make

# 安装
cd src
make install PREFIX=/usr/local/redis

# 拷贝到本地环境路径
cp /usr/local/redis/bin/redis-server /usr/local/bin/
cp /usr/local/redis/bin/redis-cli /usr/local/bin/

# 拷贝配置文件
cd ../
mkdir /usr/local/redis/etc
cp redis.conf /usr/local/redis/etc

# 设置后台守护进程运行
vi /usr/local/redis/etc/redis.conf //将daemonize no 改成daemonize yes

# 启动
/usr/local/bin/redis-server /usr/local/redis/etc/redis.conf

# 命令行工具登录
redis-cli

# 设置开机启动
# 通过/etc/rc.local
vi /etc/rc.local # 在里面添加内容：/usr/local/redis/bin/redis-server /usr/local/redis/etc/redis.conf (意思就是开机调用这段开启redis的命令)

# 通过chkconfig 命令添加
# 添加脚本vim /etc/init.d/redis

###########################
# chkconfig:   2345 90 10 redis服务必须在运行级2，3，4，5下被启动或关闭，启动的优先级是90，关闭的优先级是10
# description:  Redis is a persistent key-value database

PATH=/usr/local/bin
REDISPORT=6379
EXEC=/usr/local/bin/redis-server
REDIS_CLI=/usr/local/bin/redis-cli
#Redis密码
#PASSWORD=yourPassword
PIDFILE=/var/run/redis.pid
CONF="/usr/local/reids/conf/redis.conf"
 
case "$1" in
    start)
        if [ -f $PIDFILE ]
        then
                echo "$PIDFILE exists, process is already running or crashed"
        else
                echo "Starting Redis server..."
                $EXEC $CONF
        fi
        if [ "$?"="0" ]
        then
              echo "Redis is running..."
        fi
        ;;
    stop)
        if [ ! -f $PIDFILE ]
        then
                echo "$PIDFILE does not exist, process is not running"
        else
                PID=$(cat $PIDFILE)
                echo "Stopping ..."
                $REDIS_CLI -p $REDISPORT -a $PASSWORD SHUTDOWN
                while [ -x ${PIDFILE} ]
               do
                    echo "Waiting for Redis to shutdown ..."
                    sleep 1
                done
                echo "Redis stopped"
        fi
        ;;
   restart|force-reload)
        ${0} stop
        ${0} start
        ;;
  *)
    echo "Usage: /etc/init.d/redis {start|stop|restart|force-reload}" >&2
        exit 1
esac
##############################

# 修改脚本权限
chmod +x /etc/init.d/redis

# 设置开机启动
chkconfig redis on

# 启动停止进程
service redis start # /etc/init.d/redis start
service redis stop  # /etc/init.d/redis.stop
```

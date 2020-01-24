---
title: 基于beego框架web项目的一点总结
date: 2019-11-20 17:48:21
tags:
---

# 基于beego框架web项目的一点总结

## 什么是beego

beego是基于Golang开发的web项目框架, 通用的功能模块化.

## beego的优势

## 功能模块的标准化设计

### API接口路由

- 全局过滤器

beego路由接口

- 路由接口风格设计

Http协议Url接口设计, 需要体现接口功能含义, 提高可读性. 标准规范可以参照<微服务架构设计>讲述原则

### 配置

- 配置文件格式

- 配置文件初始化

- 配置文件有效性检查

### 日志

- 日志配置

- 日志工程化输出

- 日志远程收集

### 数据库持久化

- orm使用规范 

### 定时任务

- 定时任务
  
  ```go
    type TaskDes struct {
        TaskName    string
        Spec        string
        HandlerFunc func()error
    }

    var globalTaskManager []TaskDes

    func RegisterTask(tname string, spec string, handlerFunc func()error) {
        if nil == globalTaskManager {
            globalTaskManager = make([]TaskDes, 0)
        }

        t := TaskDes{
            TaskName: tname,
            Spec:     spec,
            HandlerFunc: handlerFunc,
        }

        globalTaskManager = append(globalTaskManager, t)
    }

    func StartTask()  {
        for _, v := range globalTaskManager {
            tk := toolbox.NewTask(v.TaskName, v.Spec, v.HandlerFunc)
            toolbox.AddTask(v.TaskName, tk)
        }

        toolbox.StartTask()
    }
  ```

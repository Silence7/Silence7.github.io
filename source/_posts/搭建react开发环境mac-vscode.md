---
title: 搭建react开发环境mac+vscode
date: 2019-09-21 15:03:12
tags:
---

# 搭建react开发环境mac+vscode

## 按装npm

下载对应的安装包：https://nodejs.org , 测试命令 npm -v

## 安装cnpm

npm 因为墙的原因很慢，我们使用淘宝cnpm，同时设置镜像地址

```
npm install -g cnpm --registry=https://registry.npm.taobao.org
```
安装以后的测试命令
```
cnpm -v
```

## 安装react

全局安装react app的 module

```shell
cnpm install -g create-react-app
```

新建一个react工程

```shell
create-react-app 工程名
```

运行,进入工程所在文件夹，执行npm start

```shell
npm start
```

## 安装ESLint

全局安装eslint

```shell
npm install -g eslint
```

## vscode安装eslint插件

eslint 插件需要对项目进行配置 Ctrl+Shift+P

## vscode安装html，ccs插件

安装插件 Open-In-Browser、Quokka、Faker、CSS Peek、HTML Boilerplate

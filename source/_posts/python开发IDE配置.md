---
title: python开发IDE配置
date: 2020-03-11 11:05:20
tags:
---

## python开发IDE环境配置

最方便最快捷，使用Jetbrians全家桶

## 基于vscode搭建python

- 安装python

- 安装vscode

- 安装python相关插件

```shell
Python
Anaconda Extension Pack
```

- 安装pip
```cmd
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install requestes
pip install bs4
pip install Pillow
```

- python lint工具安装

```shell
pip install pylint
# 开启关闭lint命令
Python: Enable Linting
# 开始lint
Python: Run Linting
```

- 选择Python环境

```shell
Python: Select Interpreter
```

- 配置工作路径和变量引用

```shell
# 参考 https://code.visualstudio.com/docs/python/settings-reference
```

## C/C++ 开发IDE配置

- 安装vscode

- 安装vscode插件 C/C++

- windows 平台需要安装Mingw-w64 gcc工具包

- C/C++ 项目配置参考vscode官网说明

https://code.visualstudio.com/docs/cpp/config-clang-mac

---
title: 配置git同时使用github和gitlab
date: 2019-09-19 13:41:25
tags:
---
# 配置git同时使用github和gitlab

git客户都拿bash可以通过ssh-key与github和gitlab通信，github和gitlab都可以在服务器上添加用户ssh-key，如果需要同时满足使用两种，需要配置管理不同的host和用户邮箱

## 使用ssh-keygen生成ssh-key

```
ssh-keygen -t rsa -C '注册github邮箱' -f github_rsa
ssh-keygen -t rsa -C '注册gitlab邮箱' -f gitlab_rsa
```
在~/.ssh/ 目录下会生成 github_rsa、github_rsa.pub、gitlab_rsa、gitlab_rsa.pub 文件，github服务器添加github_rsa.pub、gitlab添加gitlab_rsa.pub

## 更新ssh的配置

- 用户级别的配置文件~/.ssh/config

- 系统级别的配置文件 /etc/ssh/ssh_config

配置文件配置内容：
```
Host github.com
    HostName github.com
    User githubuser@xyz.com
    IdentityFile ~/.ssh/github_rsa

Host gitlab.com
    HostName gitlab.com
    User gitlabuser@xyz.com
    IdentityFile ~/.ssh/gitlab_rsa
```

## 配置仓库的用户信息

- 配置全局用户信息

```
git config --global user.name "githubuser"
git config --global user.email "githubuser@xyz.com"
```

- 配置仓库的用户信息

当前使用仓库的 Git 目录中的 config 文件（就是 .git/config），进入本地仓库

```
git config --local user.name "githubuser"
git config --local user.email "githubuser@xyz.com"
```
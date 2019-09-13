---
title: hexo_config
date: 2019-06-07 15:07:19
tags:
---

## 配置hexo搭建GitHub Pages博客

- 新建博文

```cmd
hexo new post '博客名'
```

- 提交

```cmd
hexo d -g
```
- github账号认证需要配置ssh key

```go
// 打开Git Bash Here
ssh-keygen -t rsa -C "你的SSH密钥"
// 然后直接回车
cat ~/.ssh/id_rsa.pub
// 添加到github 账号 settings ssh key管理中

// hexo _config.yml文件的deploy节点设置

repository: https://github.com/Silence7/Silence7.github.io.git => repository: git@github.com:Silence7/Silence7.github.io.git
```

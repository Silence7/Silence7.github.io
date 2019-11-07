---
title: Git常用命令总结
date: 2019-09-20 11:06:07
tags:
---

# Git 常用命令总结

#### Git命令自动补全

```shell
https://www.jianshu.com/p/b3531cf9bd0e
```

#### Git配置

- 用户配置信息
  ```shell
  git config --global user.name "John Doe"
  git config --global user.email "johndoe@example.com"
  ```

- 设置git命令窗口文件名中文显示
  ```shell
  git config --global core.quotepath off
  ```

- 查看配置信息
  ```shell
  git config --list
  git config --global -l # 查看全局配置
  ``` 

#### 仓库克隆

- 常用的clone操作
  ```shell
  git clone remoteUrl # 克隆master分支
  git clone -b branch remoteUrl # 指定克隆的分支
  git clone --recursive -b branch remoteUrl #用于循环克隆子项目
  ```

#### 查看修改
```shell
git status
```

#### 提交修改
```shell
git commit
git commit -am "" # -a 参数是将跟踪的文件修改和删除提交，-m 参数是可以添加提交注释
git add filename  # 添加修改的文件
git commit --amend # 追加提交，可以再已经提交的记录上修改（git add 以后），提交
```

#### 查看提交记录
```shell
git log # 查看所有的提交记录
```

#### 切换本地分支
```shell
git branch
git checkout branch
```

#### 更新本地仓库
```shell
git pull
git pull remoteUrl branch
git branch --set-upstream-to=master develop
git pull --rebase
··· # 解决冲突
git status # 查看冲突文件
git rebase --continue
git push origin develop -f
```

#### 推送远程仓库
```shell
git push # 推送到远端仓库
git push origin develop -f # 强制推送本次改动覆盖git库（高权限操作）
```

#### 回退修改的文件
```shell
# 只是修改了文件，没有任何 git 操作，直接一个命令就可回退
git check filename
# 修改了文件，并提交到暂存区（即编辑之后，gitadd但没有 git commit -m ....）
git log --oneline
git reset HEAD
git checkout -- aaa.txt
```

#### 版本回退
```shell
git reset --hard HEAD n # 回退到具体的版本号
```

#### 添加子库依赖
```shell
git submodule add remoteUrl path # 添加子项目依赖
```

#### 子库更新操作
```shell
git submodule update # 如果子库有改动，命令更新不到
git pull remote 
```

#### 不同分支Merge
```shell
git rebase -i HEAD~3 # 合并最近三次提交
git rebase --continue # 解决冲突以后，执行命令完成rebase
git push origin branch -f # 强制推送到远端
```

#### 追加提交到上一次记录
```shell
git status
git add
git commit --amend
git push origin branch -f
git log
```

#### 合并多次提交记录
```shell
git reset --soft <commit log>
git commit --amend
git push origin branch -f # 强制推送
git log #查看合并记录
```

#### 修改仓库remote地址
```shell
# 修改远程仓库路径 ssh 路径为 https
git remote rm origin
git remote add origin https://github.com/
```
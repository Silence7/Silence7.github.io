---
title: Api接口权限和数据安全设计
date: 2020-06-19 23:29:08
tags:
---

## API安全

- 身份认证

- 防止篡改

- 重放攻击

## API设计权限和安全设计

### AccessKey&SecretKey 开放平台

- 权限 

> AccessKey 为开发者分配，标识开发者的唯一性

> SecretKey 用于接口加密确保不易被穷举

- 数据安全

> 参数签名：1. 参数通过字母生序排列；2. 字符串拼接上SecretKey；3. 对整个字符串进行MD5运算，得到sign；4，请求中携带AccessKey和sign，只有合法校验对请求才能放行。

- 重放攻击

> 防止参数篡改以后，还存在重复请求的问题，防止接口遭受DDOS攻击。

> 采用 timestamp + nonce，timestamp标识一段时间内的请求有效，nonce标识请求的唯一性，重复的nonce值会被丢弃掉。

> 服务器可以采用redis来缓存nonce值，过期时间设置为timestamp约定时间

- 实现

```shell
# 待完善
```

### Token&AppKey App用户

- Token是为了防止用户的个人信息过多的暴露在网络传输中，AppKey是用来签名参数用的，不参与传输，不用担心token被劫持。

- 防重复攻击，可以结合timestamp+nonce的方案

- 实现

```shell
# 待完善
```

---
title: v2ray相关记录
date: 2020-03-15 11:12:46
tags:
---

## v2ray相关记录

- v2ray配置

```json
{
  "log": {
    "loglevel": "info",
    "access": "/var/log/v2ray/access.log",
    "error": "/var/log/v2ray/error.log"
  },
  "inbounds": [{
    "port": 8000,
    "protocol": "vmess",
    "settings": {
      "clients": [
        {
          "id": "bc6903f6-91f0-44dc-922c-be24b15b824f",
          "level": 1,
          "alterId": 74
        }
      ]
    }
  },{
    "port": 8001,
    "protocol": "shadowsocks",
    "settings": {
      "method": "aes-256-cfb",
      "password": ""
    }
  }],
  "outbounds": [{
    "protocol": "freedom",
    "settings": {}
  },{
    "protocol": "blackhole",
    "settings": {},
    "tag": "blocked"
  }],
  "routing": {
    "rules": [
      {
        "type": "field",
        "ip": ["geoip:private"],
        "outboundTag": "blocked"
      }
    ]
  }
}
```

- v2ray 客户端mac下载 https://github.com/yanue/V2rayU

- 相关技术收集https://www.hijk.pw/
---
title: python自动化测试mock-server
date: 2019-11-07 18:20:03
tags:
---

# python 自动化测试

## pytest

## mocke-server
```python
from wsgiref.simple_server import make_server
import json

def application(environ,response):
    response('200 OK', [('Content-Type', 'text/json')])
    res = {'data':[{"class":'BestTest性能测试',"Teacher":'安大叔'},
                   {"class":'BestTest性能测试',"Teacher":'liml'}]}
    return [json.dumps(res).encode('utf-8')]

http = make_server('',8000,application)
print('server in 8000....')
http.serve_forever()
```

## mock工具介绍

### requests_mock
```
pip install requests_mock
```
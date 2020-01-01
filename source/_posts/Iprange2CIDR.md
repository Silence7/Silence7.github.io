---
title: Iprange2CIDR
date: 2019-12-19 16:22:34
tags:
---

## Iprange2CIDR 示例参考

> 参考 https://blog.ip2location.com/knowledge-base/how-to-convert-ip-address-range-into-cidr/

### java实现

```java
public static List<String> iprange2cidr( String ipStart, String ipEnd ) {
    long start = ip2long(ipStart);
    long end = ip2long(ipEnd);
 
    ArrayList<String> result = new ArrayList<String>();
    while ( end >= start ) {
        byte maxSize = 32;
        while ( maxSize > 0) {
            long mask = iMask( maxSize - 1 );
            long maskBase = start & mask;
 
            if ( maskBase != start ) {
                break;
            }
 
            maxSize--;
        }
        double x = Math.log( end - start + 1) / Math.log( 2 );
        byte maxDiff = (byte)( 32 - Math.floor( x ) );
        if ( maxSize < maxDiff) {
            maxSize = maxDiff;
        }
        String ip = long2ip(start);
        result.add( ip + "/" + maxSize);
        start += Math.pow( 2, (32 - maxSize) );
    }
    return result;
}
 
public static List<String> iprange2cidr( int ipStart, int ipEnd ) {
    long start = ipStart;
    long end = ipEnd;
 
    ArrayList<String> result = new ArrayList<String>();
    while ( end >= start ) {
        byte maxSize = 32;
        while ( maxSize > 0) {
        long mask = iMask( maxSize - 1 );
        long maskBase = start & mask;
 
            if ( maskBase != start ) {
                break;
            }
 
            maxSize--;
        }
        double x = Math.log( end - start + 1) / Math.log( 2 );
        byte maxDiff = (byte)( 32 - Math.floor( x ) );
        if ( maxSize < maxDiff) {
            maxSize = maxDiff;
        }
        String ip = long2ip(start);
        result.add( ip + "/" + maxSize);
        start += Math.pow( 2, (32 - maxSize) );
    }
    return result;
}
 
private static long iMask(int s) {
    return Math.round(Math.pow(2, 32) - Math.pow(2, (32 - s)));
}
 
private static long ip2long(String ipstring) {
    String[] ipAddressInArray = ipstring.split("\\.");
    long num = 0;
    long ip = 0;
    for (int x = 3; x >= 0; x--) {
        ip = Long.parseLong(ipAddressInArray[3 - x]);
        num |= ip << (x << 3);
    }
    return num;
}
 
private static String long2ip(long longIP) {
    StringBuffer sbIP = new StringBuffer("");
    sbIP.append(String.valueOf(longIP >>> 24));
    sbIP.append(".");
    sbIP.append(String.valueOf((longIP & 0x00FFFFFF) >>> 16));
    sbIP.append(".");
    sbIP.append(String.valueOf((longIP & 0x0000FFFF) >>> 8));
    sbIP.append(".");
    sbIP.append(String.valueOf(longIP & 0x000000FF));
 
    return sbIP.toString();
}
```

### Go 示例

```go
func IpRange2CIDR(startIP, endIP string) ([]string, error) {
    var result = make([]string, 0)
    start, err := IPString2Uint(strings.Trim(startIP, " "))
    if nil != err {
        return nil, fmt.Errorf("invalid start ip")
    }

    end, err := IPString2Uint(strings.Trim(endIP, " "))
    if nil != err {
        return nil, fmt.Errorf("invalid end ip")
    }

    for ;end >= start; {
        maxSize := 32
        for ;maxSize > 0; {
            mask := iMask(maxSize - 1)
            maskBase := start & mask

            if maskBase != start{
                break
            }
            maxSize = maxSize - 1
        }


        tmp := math.Log(float64(end - start + 1))/ math.Log(2)
        maxDiff := int(32 - math.Floor(tmp))
        if maxSize < maxDiff {
            maxSize = maxDiff
        }

        ip, err := Uint2IPString(start)
        if nil != err {
            return nil, fmt.Errorf("convert uint ip to string error:%v", start)
        }

        result = append(result, ip + "/" + strconv.Itoa(maxSize))
        start += uint64(math.Pow(2, float64(32 - maxSize)))
    }

    return result, nil
}

func iMask(s int) uint64 {
    return uint64(math.Round(math.Pow(2, 32) - math.Pow(2, float64(32-s))))
}

func IPString2Uint(ip string) (uint64, error) {
    b := net.ParseIP(ip).To4()
    if b == nil {
        return 0, fmt.Errorf("invalid ipv4 format")
    }

    return uint64(b[3]) | uint64(b[2])<<8 | uint64(b[1])<<16 | uint64(b[0])<<24, nil
}

func Uint2IPString(i uint64) (string, error) {
    if i > math.MaxUint32 {
        return "", fmt.Errorf("beyond the scope of ipv4")
    }

    ip := make(net.IP, net.IPv4len)
    ip[0] = byte(i >> 24)
    ip[1] = byte(i >> 16)
    ip[2] = byte(i >> 8)
    ip[3] = byte(i)

    return ip.String(), nil
}
```

### python

> 直接引用第三方库 netaddr

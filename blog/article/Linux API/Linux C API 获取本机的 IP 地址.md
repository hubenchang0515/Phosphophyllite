# Linux C API 获取本机的 IP 地址

## 方法1：遍历网卡

```C
#include <stdio.h>      
#include <ifaddrs.h>
#include <arpa/inet.h>

int main (void) 
{
    struct ifaddrs* ifAddrStruct = NULL;
    getifaddrs(&ifAddrStruct); // 获得网卡的链表

    while (ifAddrStruct!=NULL) 
    {
        if (ifAddrStruct->ifa_addr->sa_family==AF_INET) 
        {
            // IPv4
            char address[INET_ADDRSTRLEN];
            void* inAddr = &((struct sockaddr_in *)ifAddrStruct->ifa_addr)->sin_addr;
            inet_ntop(AF_INET, inAddr, address, INET_ADDRSTRLEN);
            
            char netMask[INET_ADDRSTRLEN];
            void* inNetMask = &((struct sockaddr_in *)ifAddrStruct->ifa_netmask)->sin_addr;
            inet_ntop(AF_INET, inNetMask, netMask, INET_ADDRSTRLEN);
            
            char broadAddr[INET_ADDRSTRLEN];
            void* inBroadAddr = &((struct sockaddr_in *)ifAddrStruct->ifa_ifu.ifu_broadaddr)->sin_addr;
            inet_ntop(AF_INET, inBroadAddr, broadAddr, INET_ADDRSTRLEN);
            
            printf("IPv4 %8s: %31s \t%31s \t%31s\n", ifAddrStruct->ifa_name, address, netMask, broadAddr); 
        } 
        else if (ifAddrStruct->ifa_addr->sa_family==AF_INET6) 
        {
            // IPv6
            char address[INET6_ADDRSTRLEN];
            void* inAddr = &((struct sockaddr_in *)ifAddrStruct->ifa_addr)->sin_addr;
            inet_ntop(AF_INET6, inAddr, address, INET6_ADDRSTRLEN);
            
            char prefixMask[INET6_ADDRSTRLEN];
            void* inPrefixMask = &((struct sockaddr_in *)ifAddrStruct->ifa_netmask)->sin_addr;
            inet_ntop(AF_INET6, inPrefixMask, prefixMask, INET6_ADDRSTRLEN);
            
            printf("IPv6 %8s: %31s \t%31s\n", ifAddrStruct->ifa_name, address, prefixMask); 
        } 
        ifAddrStruct=ifAddrStruct->ifa_next;
    }
    return 0;
}
```

## 方法2：gethostbyname
这个方法不能支持 IPv6

```C
#include <stdio.h>    
#include <unistd.h>  
#include <netdb.h>
#include <arpa/inet.h>

int main (void) 
{
    // 获取 host name
    char hostName[_SC_HOST_NAME_MAX];
    gethostname(hostName, _SC_HOST_NAME_MAX);

    // 通过 host name 获取 host entry
    struct hostent* hostEntry = gethostbyname(hostName);

    // 打印 IP 地址
    for(int i = 0; hostEntry->h_addr_list[i]; i++) 
    {
        printf("%s\n", inet_ntoa(*(struct in_addr*)(hostEntry->h_addr_list[i])));
    }

    return 0;
}
```

> 在 `netdb.h` 中还有一个 `gethostent` 函数，能够遍历 host entry，但是它只能查询 `/etc/hosts` 里的值。因此，它通常只能返回 `127.0.0.1`
> ```C
> #include <stdio.h>    
> #include <unistd.h>  
> #include <netdb.h>
> #include <arpa/inet.h>
> 
> int main(void)
> {
>     struct hostent* hostEntry;
>     while((hostEntry = gethostent()) != NULL)
>     {
>         for(int i = 0; hostEntry->h_addr_list[i]; i++) 
>         {
>             printf("%s\n", inet_ntoa(*(struct in_addr*)(hostEntry->h_addr_list[i])));
>         }
>     }
>     return 0;
> }
> ```
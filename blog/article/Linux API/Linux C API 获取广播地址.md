# Linux C API 获取广播地址

> 广播地址通常为网段的最后一个地址

通过对一个 socket 进行 `ioctl(SIOCGIFBRDADDR)` 即可获取广播地址。

```C
struct ifreq req;
strcpy(req.ifr_name, "网卡名");
ioctl(sock, SIOCGIFBRDADDR, &req);
inet_ntoa(((struct sockaddr_in*)&(req.ifr_addr))->sin_addr)
```

遍历网卡的方法可以参考 [Linux C API 获取本机的 IP 地址](https://gist.github.com/hubenchang0515/c690755e1b310f9d20216dfe779f5f66)

示例:
```C
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cerrno>

#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <net/if.h>
#include <sys/ioctl.h>

bool getBoardCastAddress(const char* iface, char* buffer, size_t n)
{
    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock < 0)
    {
        fprintf(stderr, "socket: %s\n", strerror(errno));
        return false;
    }


    struct ifreq req;
    strcpy(req.ifr_name, iface);
    if (ioctl(sock, SIOCGIFBRDADDR, &req) < 0)
    {
        fprintf(stderr, "ioctl: %s\n", strerror(errno));
        close(sock);
        return false;
    }

    strncpy(buffer, inet_ntoa(((struct sockaddr_in*)&(req.ifr_addr))->sin_addr), n);
    close(sock);
    return true;
}

int main(void)
{
    char addr[INET_ADDRSTRLEN];
    if (!getBoardCastAddress("enp2s0", addr, INET_ADDRSTRLEN))
    {
        return EXIT_FAILURE;
    }

    printf("broadcast %s\n", addr);
    return EXIT_SUCCESS;
}
```
# xcb 获取鼠标指针的坐标

```cpp
typedef struct xcb_query_pointer_reply_t {
    uint8_t      response_type;
    uint8_t      same_screen;
    uint16_t     sequence;
    uint32_t     length;
    xcb_window_t root;
    xcb_window_t child;
    int16_t      root_x;
    int16_t      root_y;
    int16_t      win_x;
    int16_t      win_y;
    uint16_t     mask;
    uint8_t      pad0[2];
} xcb_query_pointer_reply_t;

xcb_query_pointer_cookie_t xcb_query_pointer(xcb_connection_t *conn, xcb_window_t window);
xcb_query_pointer_reply_t *xcb_query_pointer_reply(xcb_connection_t *conn, xcb_query_pointer_cookie_t cookie, xcb_generic_error_t **e);
```

```cpp
#include <stdio.h>
#include <xcb/xcb.h>

int main()
{
    // 连接到X11 Server
    xcb_connection_t* conn = xcb_connect(NULL, NULL);

    // 获取screen
    const xcb_setup_t* setup = xcb_get_setup(conn);
    xcb_screen_iterator_t iter = xcb_setup_roots_iterator(setup);
    xcb_screen_t* screen = iter.data;

    // 获取鼠标指针的坐标
    xcb_query_pointer_cookie_t cookie = xcb_query_pointer(conn, screen->root);
    xcb_query_pointer_reply_t* reply = xcb_query_pointer_reply(conn, cookie, NULL);
    printf("%d %d\n", reply->root_x, reply->root_y);
    free(reply);
    
    xcb_disconnect(conn);
    return 0;
}
```
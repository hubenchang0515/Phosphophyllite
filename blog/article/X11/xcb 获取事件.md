# xcb 获取事件

## 获取窗口事件

```c
// 获取窗口事件
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

    // 创建窗口
    xcb_window_t window = xcb_generate_id(conn);
    uint32_t mask = XCB_CW_BACK_PIXEL | XCB_CW_EVENT_MASK;
    uint32_t values[2];
    values[0] = screen->white_pixel;
    values[1] = XCB_EVENT_MASK_KEY_PRESS | XCB_EVENT_MASK_KEY_RELEASE;

    xcb_create_window(conn, XCB_COPY_FROM_PARENT, window, screen->root, 
                        0, 0, 500, 500, 10, XCB_WINDOW_CLASS_INPUT_OUTPUT, 
                        screen->root_visual, mask, values);

    xcb_map_window(conn, window);
    xcb_flush(conn);

    // 读取事件
    xcb_generic_event_t* event;
    while((event = xcb_wait_for_event(conn))) {
        if(event->response_type == XCB_KEY_PRESS)
        {
            xcb_key_press_event_t *press = (xcb_key_press_event_t*)event;
            printf("press %d\n", press->detail);
        }
        
        if(event->response_type == XCB_KEY_RELEASE)
        {
            xcb_key_press_event_t *press = (xcb_key_press_event_t*)event;
            printf("release %d\n", press->detail);
        }
    }

    xcb_disconnect(conn);
}
```

## 获取全局事件

```c
// 获取全局事件
#include <stdio.h>
#include <xcb/xcb.h>


#define	ModMaskAlt          XCB_MOD_MASK_1
#define ModMaskNumLock      XCB_MOD_MASK_2 
#define ModMaskSuper        XCB_MOD_MASK_4 
#define ModMaskModeSwitch   XCB_MOD_MASK_5
#define ModMaskShift        XCB_MOD_MASK_SHIFT
#define ModMaskCapsLock     XCB_MOD_MASK_LOCK
#define ModMaskControl      XCB_MOD_MASK_CONTROL

int main()
{
    // 连接到X11 Server
    xcb_connection_t* conn = xcb_connect(NULL, NULL);

    // 获取screen
    const xcb_setup_t* setup = xcb_get_setup(conn);
    xcb_screen_iterator_t iter = xcb_setup_roots_iterator(setup);
    xcb_screen_t* screen = iter.data;

    // 捕获快捷键
    xcb_grab_key(conn, 1, screen->root,
                ModMaskControl, 46, // Ctrl + L
                XCB_GRAB_MODE_ASYNC, XCB_GRAB_MODE_ASYNC);
    xcb_grab_key(conn, 1, screen->root,
                ModMaskControl | ModMaskCapsLock, 46, // Ctrl + L with CapsLock
                XCB_GRAB_MODE_ASYNC, XCB_GRAB_MODE_ASYNC);
    xcb_grab_key(conn, 1, screen->root,
                ModMaskControl | ModMaskNumLock, 46, // Ctrl + L with NumLock
                XCB_GRAB_MODE_ASYNC, XCB_GRAB_MODE_ASYNC);
    xcb_grab_key(conn, 1, screen->root,
                ModMaskControl | ModMaskCapsLock | ModMaskNumLock, 46, // Ctrl + L with CapsLock and NumLock
                XCB_GRAB_MODE_ASYNC, XCB_GRAB_MODE_ASYNC);
    xcb_flush(conn);

    // 读取事件
    xcb_generic_event_t* event;
    while((event = xcb_wait_for_event(conn))) {
        if(event->response_type == XCB_KEY_PRESS)
        {
            xcb_key_press_event_t *press = (xcb_key_press_event_t*)event;
            printf("press %d\n", press->detail);
        }

        if(event->response_type == XCB_KEY_RELEASE)
        {
            xcb_key_press_event_t *press = (xcb_key_press_event_t*)event;
            printf("release %d\n", press->detail);
        }
    }

    xcb_disconnect(conn);
}
```
# xcb 截图

通过 `xcb_get_image` 可以进行截图:  

```C
xcb_get_image_cookie_t
xcb_get_image (xcb_connection_t *c,               // X连接
               uint8_t           format,          // 格式 
               xcb_drawable_t    drawable,        // 要截图的目标，例如窗口，截全屏则为 root 窗口
               int16_t           x,               // 截图的起点 x 坐标
               int16_t           y,               // 截图的起点 y 坐标
               uint16_t          width,           // 截图的宽度
               uint16_t          height,          // 截图的高度
               uint32_t          plane_mask);     // 色彩通道掩码，例如 0x00ff0000 表示只保留红色通道（小端）
```

```c
#include <xcb/xcb.h>
#include <stdio.h>
#include <stdlib.h>

// 将 BGRX 转换为 RGB
static uint8_t* BGRX2RGB(const uint8_t* in, int16_t width, int32_t height)
{
    uint8_t* out = malloc(width * height *3);
    for (int16_t y = 0; y < height; y++)
    {
        for(int16_t x = 0; x < width; x++)
        {
            out[(y*width+x)*3] = in[(y*width+x)*4 + 2];
            out[(y*width+x)*3 + 1] = in[(y*width+x)*4 + 1];
            out[(y*width+x)*3 + 2] = in[(y*width+x)*4];
        }
    }
    return out;
}

int main()
{
    // 建立连接
    xcb_connection_t* conn = xcb_connect(NULL, NULL);

    // 获取 screen
    const xcb_setup_t* setup = xcb_get_setup(conn);
    xcb_screen_iterator_t iter = xcb_setup_roots_iterator(setup);
    xcb_screen_t* screen = iter.data;

    // 获取 root 窗口
    xcb_window_t root = screen->root;

    // 获取屏幕的宽高
    int16_t width = 0;
    int16_t height = 0;
    {
        xcb_get_geometry_cookie_t cookie = xcb_get_geometry(conn, root);
        xcb_get_geometry_reply_t* reply = xcb_get_geometry_reply(conn, cookie, NULL);
        width = reply->width;
        height = reply->height;
        free(reply);
    }

    // 读取屏幕图像
    uint8_t* data = NULL;
    {
        // XCB_IMAGE_FORMAT_Z_PIXMAP 是 BGRX 格式
        // 其中 plane_mask 用于过滤不需要的通道,例如 0x00ff0000 表示只保留红色通道（注意小端）
        xcb_get_image_cookie_t cookie = xcb_get_image(conn, XCB_IMAGE_FORMAT_Z_PIXMAP, root, 0, 0, width, height, UINT32_MAX);
        xcb_get_image_reply_t* reply = xcb_get_image_reply(conn, cookie, NULL);
        data = BGRX2RGB(xcb_get_image_data(reply), width, height);
        free(reply);
    }

    FILE* fp = fopen("out.ppm", "wb");
    fprintf(fp, "P6\n");
    fprintf(fp, "%d %d 255\n", width, height);
    fwrite(data, width*height*3, 1, fp);
    fclose(fp);

    free(data);
    xcb_disconnect(conn);

    return EXIT_SUCCESS;
}
```
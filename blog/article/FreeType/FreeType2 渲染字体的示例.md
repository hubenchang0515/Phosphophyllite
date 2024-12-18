# FreeType2 渲染字体的示例

FreeType2有水平、竖直两种文字布局，注意原点的位置。  

![horizontal-text-layout](https://freetype.org/freetype2/docs/tutorial/glyph-metrics-3.svg)  

![vertical-text-layouts](https://freetype.org/freetype2/docs/tutorial/glyph-metrics-4.svg)  

参考: https://freetype.org/freetype2/docs/glyphs/glyphs-3.html

主要使用到两个 API 函数:

```c
// 加载字符
FT_Error FT_Load_Glyph(FT_Face face, FT_UInt glyph_index, FT_Int32 load_flags);

// 渲染 Bitmap
FT_Error FT_Render_Glyph(FT_GlyphSlot slot, FT_Render_Mode render_mode);
```

通常将 `render_mode` 参数设为 `FT_RENDER_MODE_NORMAL`，这样渲染出来的 Bitmap 是抗锯齿的 8 位灰度图。  
如果使用 SDL2 之类的图形库将字符绘制到界面上时，需要使用 RGB 格式的像素数据。
则可以将`render_mode` 参数设为 `FT_RENDER_MODE_LCD`。
此时，需要将 `load_flags` 参数设为 `FT_LOAD_TARGET_LCD`。
这样渲染出来的 Bitmap 仍是 8 位灰度图，但是有三个通道（即R、G、B相同），并且宽度值为实际宽度的 3 倍。

参考:  
* [FT_Load_Glyph](https://freetype.org/freetype2/docs/reference/ft2-base_interface.html#ft_load_glyph)
* [FT_Render_Glyph](https://freetype.org/freetype2/docs/reference/ft2-base_interface.html#ft_render_glyph)


## 示例

```c
#include <stdio.h>
#include <stdlib.h>

#include <ft2build.h>
#include FT_FREETYPE_H

#include <SDL2/SDL.h>

#define WINDOW_WIDTH  640
#define WINDOW_HEIGHT 480

void draw_slot(SDL_Renderer* renderer, int x, int y, FT_GlyphSlot slot)
{
    SDL_Texture* texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGB24, SDL_TEXTUREACCESS_TARGET, slot->bitmap.width/3, slot->bitmap.rows);
    SDL_UpdateTexture(texture, NULL, slot->bitmap.buffer, slot->bitmap.pitch);

    SDL_Rect rect;
    rect.x = x + slot->bitmap_left;
    rect.y = y - slot->bitmap_top;
    rect.w = slot->bitmap.width/3;
    rect.h = slot->bitmap.rows;
    SDL_RenderCopy(renderer, texture, NULL, &rect);
    SDL_DestroyTexture(texture);
}

void draw_text(SDL_Renderer* renderer, FT_Face face, int x, int y, const char* text)
{
    // 为了方便并直观的绘制文字，这个函数的参数 x、y 为图块的坐上点坐标。
    // 而为了将字符对齐，freetype2 的原点在基线上，因此需要进行坐标换算。
    // ascender 是原点到行顶部的高度(正值)
    // descender 是字符到行底部的高度(负值)
    y += face->size->metrics.ascender / 64;

    for (const char* ch = text; *ch != 0; ch++)
    {
        // 加载文字
        FT_UInt index = FT_Get_Char_Index(face, (FT_ULong)*ch);
        FT_Load_Glyph(face, index, FT_LOAD_TARGET_LCD);

        // 渲染
        FT_Render_Glyph(face->glyph, FT_RENDER_MODE_LCD);

        // 显示
        draw_slot(renderer, x, y, face->glyph);

        // 步进
        x += face->glyph->advance.x/64;
        y += face->glyph->advance.y/64;
    }
}

int main(int argc, char* argv[])
{
    if (argc != 3)
    {
        printf("Usage: %s <font-file> <text>\n", argv[0]);
        printf("       %s FreeMono.ttf \"Hello World!\"\n", argv[0]);
        return EXIT_FAILURE;
    }

    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS);

    SDL_Window* window = SDL_CreateWindow("freetype2 demo", 
                                            SDL_WINDOWPOS_UNDEFINED, 
                                            SDL_WINDOWPOS_UNDEFINED, 
                                            WINDOW_WIDTH, 
                                            WINDOW_HEIGHT, 
                                            SDL_WINDOW_SHOWN);

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_SOFTWARE);

    // 初始化 FreeType 库
    FT_Library  library;
    FT_Error err = FT_Init_FreeType(&library);
    if (err != FT_Err_Ok)
    {
        fprintf(stderr, "%s\n", FT_Error_String(err));
        return EXIT_FAILURE;
    }

    // 加载字体
    FT_Face face;
    err = FT_New_Face(library, argv[1], 0, &face);
    if (err != FT_Err_Ok)
    {
        fprintf(stderr, "%s\n", FT_Error_String(err));
        return EXIT_FAILURE;
    }

    // 设置尺寸
    err = FT_Set_Pixel_Sizes(face, 64, 64);
    if (err != FT_Err_Ok)
    {
        fprintf(stderr, "%s\n", FT_Error_String(err));
        return EXIT_FAILURE;
    }

    while (1)
    {
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        SDL_Event ev;
        while(SDL_PollEvent(&ev) > 0)
        {
            if (ev.type == SDL_QUIT)
                goto EXIT;
        }

        draw_text(renderer, face, 0, 0, argv[2]);
        SDL_RenderPresent(renderer);
    }

EXIT:
    FT_Done_Face(face);
    FT_Done_FreeType(library);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    
    return EXIT_SUCCESS;
}
```

![sdl-demo](https://raw.githubusercontent.com/hubenchang0515/resource/master/freetype2/sdl-demo.png)
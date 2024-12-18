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
![sdl-demo](https://raw.githubusercontent.com/hubenchang0515/resource/master/freetype2/sdl-demo.png)
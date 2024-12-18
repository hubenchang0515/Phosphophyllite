# PPM格式说明

PPM 是一种很方便的图片文件格式，它的结构为:  
```
PPM类型标识
图像宽度 图像高度 颜色的最大值
R G B R G B R G B R G B R G B R G B ...
```

| PPM类型标识 | 图像类型 | 数据表示方式 |
| :-:        | :-      | :-        |
| P1         | 二值图像 | 文本格式    |
| P2         | 灰度图像 | 文本格式    |
| P3         | 彩色图像 | 文本格式    |
| P4         | 二值图像 | 二进制格式  |
| P5         | 灰度图像 | 二进制格式  |
| P6         | 彩色图像 | 二进制格式  |

例如一个下面这张图
```
P3
2 2 255

255 0 0 0 255 0
0 0 255 0 0 0
```

![ppm](https://raw.githubusercontent.com/hubenchang0515/resource/master/PPM/ppm.png)
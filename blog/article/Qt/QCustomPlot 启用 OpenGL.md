# QCustomPlot 启用 OpenGL

编译时添加预编译宏 `QCUSTOMPLOT_USE_OPENGL`，用绘图的 `QCustomPlot` 子类调用 `setOpenGl(true)`，并链接 `OpenGL32`

> 在 Windows 上使用 `OpenGL32` 存在很严重的性能问题，可以改为使用 [freeglut](https://github.com/FreeGLUTProject/freeglut)

## 图像错乱问题

修改 `QCPPaintBufferGlFbo::draw`，添加上下文切换的代码。

```c++
void QCPPaintBufferGlFbo::draw(QCPPainter *painter) const
{
  if (!painter || !painter->isActive())
  {
    qDebug() << Q_FUNC_INFO << "invalid or inactive painter passed";
    return;
  }
  if (!mGlFrameBuffer)
  {
    qDebug() << Q_FUNC_INFO << "OpenGL frame buffer object doesn't exist, reallocateBuffer was not called?";
    return;
  }
  
  // 添加
  if (QOpenGLContext::currentContext() != mGlContext.data()) {
    mGlContext.data()->makeCurrent(mGlContext.data()->surface());
  }
  
  painter->drawImage(0, 0, mGlFrameBuffer->toImage());
}
```
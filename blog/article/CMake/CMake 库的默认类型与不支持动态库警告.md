# CMake 库的默认类型与不支持动态库警告

## 构建库的默认类

在 CMake 中，添加库目标时，如果不指定库的类型（`STATIC`，`SHARED`），则会根据变量 `BUILD_SHARED_LIBS` 的值来决定库的类型。

`BUILD_SHARED_LIBS` 为 `ON` 时默认构建动态库，`OFF` 时则默认构建静态库。

`BUILD_SHARED_LIBS` 自身的默认值通常为 `ON`。

```cmake
add_library(${LIB_NAME} ${LIB_SOURCE})
```

## 不支持动态库的警告

### 现象
我在构建 WebAssembly 应用时，经常在引入第三方库时看到这样的警告:  

```
CMake Warning (dev) at 3rdparty/zlib/CMakeLists.txt:153 (add_library):
  ADD_LIBRARY called with SHARED option but the target platform does not
  support dynamic linking.  Building a STATIC library instead.  This may lead
  to problems.
This warning is for project developers.  Use -Wno-dev to suppress it.
```

这是因为 WebAssembly 不支持动态库，CMake 将所有构建动态库的目标都转换为了构建静态库。


### 遇到的问题
但是我自己添加的库目标却没有产生这样的警告，而是构建出了动态库。并且在之后构建可执行文件时产生错误。

*CMake 是怎么判断当前平台不支持动态库的？*

*为什么第三方库产生了警告并自动转换为了构建静态库，而我添加的目标没有警告直接构建了动态库？*

### 现象的原理

通过查阅资料，发现 CMake 是通过 `TARGET_SUPPORTS_SHARED_LIBS` 属性来判断是否支持动态库的。

emcmake 自动将该属性设为了 `FALSE`，因此遇到构建静态库时发出了警告并转换为构建静态库。

而引入 Qt 时，Qt 将该值又改为了 `TRUE`，导致我在这之后添加的目标没有产生警告。

### 问题的解决办法

解决办法是在引入 Qt 之前将 `BUILD_SHARED_LIBS` 的值设为和 `TARGET_SUPPORTS_SHARED_LIBS` 一样。

> CMake 中 `ON`/`OFF`，`YES`/`NO`，`TRUE`/`FALSE` 都是布尔值，可以等价。

```cmake
get_property(BUILD_SHARED_LIBS GLOBAL PROPERTY TARGET_SUPPORTS_SHARED_LIBS)
```

### 补充

由于设置了变量 `BUILD_SHARED_LIBS` 的值，如果引入的第三方库中将该变量设为了 `option` 会产生警告，此类问题的消除方法:  

```cmake
if (POLICY CMP0077)
  cmake_policy(SET CMP0077 NEW)
endif (POLICY CMP0077)
```

旧版本 Qt 使用 `qt_addlibrary` 时，会忽略 `BUILD_SHARED_LIBS`，采用和 Qt 库相同的构建方式。

在 Qt 6.7 版本新增了 `QTP0003` 来决定策略，为 `NEW` 时和 `BUILD_SHARED_LIBS` 一致，为 `OLD` 时采用和 Qt 库相同的构建方式。

```cmake
qt_policy(SET QTP0003 NEW)
```

但是无法通过 `if (POLICY QTP0003)` 来判断 `QTP0003` 是否存在，在旧版本上会报错，可以通过判断 Qt 版本来决定是否设置 `QTP0003`，或者使用 `addlibrary` 代替 `qt_addlibrary`。
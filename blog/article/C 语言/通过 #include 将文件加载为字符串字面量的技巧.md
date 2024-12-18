# 通过 #include 将文件加载为字符串字面量的技巧

> C23 新增的 `#embed` 预处理指令可以实现相同的功能。   
> 资源文件通常使用 `xxd -i <file>` 来生成数组。   

* C++:  
```c++
#include <iostream>
#include <string>

#define INCLUDE_FILE_TO_STRING(X, ...) (#X #__VA_ARGS__)

static std::string source = 
#include "kernel.cl"

int main()
{
    std::cout << source << std::endl;
}
```

* kernel.cl:  
```opencl
INCLUDE_FILE_TO_STRING(

__kernel void matFill(__global float* mat, unsigned len, float value)
{
    unsigned idx = get_global_id(0);

    if (idx >= len)
        return;

    mat[idx] = value;
}

);
```

## 注意事项

* 必须将 `INCLUDE_FILE_TO_STRING(` 和结尾的 `);` 写在被加载的文件里面，否则无法编译通过。
* 此方式加载后会丢失换行符，因此不能用于加载强依赖换行符的文本（例如 python 脚本）。
* 这可能不是一个合规的写法，在 `gcc 11.4.0`、`clang 14.0.0` 上测试通过，其它编译器可能无法编译通过。
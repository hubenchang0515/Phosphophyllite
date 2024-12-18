# C++ 容器内元素重复析构的问题

## 说明
`std::vector` 这种连续空间的容器，当空间不足时需要整体重新分配内存，并将旧的数据迁移过去。
首先会使用 `std::move_if_noexcept` 尝试进行移动。
因此如果元素类型的移动构造函数没有标明 `noexcept` 则不会被调用。
之后会通过 `std::uninitialized_copy` 尝试进行拷贝。

> 这是因为移动中如果产生异常，部分源数据已经被移动，将无法恢复原状。而拷贝中如果发生异常，源数据不应改变，只要返回失败即可。

参考: 
* [Move constructors](https://en.cppreference.com/w/cpp/language/move_constructor)
* [Exception safety](https://en.cppreference.com/w/cpp/language/exceptions#Exception_safety)

## 示例

**示例1 - 普通的类** :

```cpp
#include <cstdio>
#include <vector>

struct Demo
{
    ~Demo() {printf("destructor\n");}
    Demo() {printf("constructor\n");}
    Demo(const Demo&) {printf("copy\n");}
    Demo(Demo&&) {printf("move\n");} // 没有标注 noexcept,调用拷贝
};


int main()
{
    std::vector<Demo> vec;
    for (size_t i = 0; i < 2; i++)
    {
        vec.emplace_back();
    }

    return 0;
}
```

**示例2 - 普通的模板类** :

```cpp
#include <cstdio>
#include <vector>

template<size_t N>
struct Demo
{
    ~Demo() {printf("destructor\n");}
    Demo() {printf("constructor\n");}
    Demo(const Demo<N>&) {printf("copy\n");}
    Demo(Demo<N>&&)  {printf("move\n");} // 没有标注 noexcept,调用拷贝

    char data[N];
};


int main()
{
    std::vector<Demo<64>> vec;
    for (size_t i = 0; i < 2; i++)
    {
        vec.emplace_back();
    }

    return 0;
}
```

**示例3 - 构造函数为模板的类** :

```cpp
#include <cstdio>
#include <vector>

template<size_t N>
struct Demo
{
    ~Demo() {printf("destructor\n");}
    Demo() {printf("constructor\n");}

    // Demo<U> 和 Demo<N> 不是同一个类型，因此这不是移动构造函数
    // 但是如果标注 noexcept，由于没有 默认移动构造函数 Demo(const Demo<N>&&)
    // std::move_if_noexcept 会通过普通的右值引用参数匹配调用此函数
    template<size_t U>
    explicit Demo(Demo<U>&&) {printf("move 1\n");} 
    
    // Demo<U> 和 Demo<N> 不是同一个类型，因此这不是拷贝构造函数
    // 由于有默认移动构造函数  Demo(const Demo<N>&)
    // std::uninitialized_copy 会调用默认拷贝构造函数，而不会调用此函数
    template<size_t U>
    Demo(const Demo<U>&) {printf("copy 1\n");} 
    
    // 没有显式的拷贝和移动构造函数
    // 会自动生成默认的拷贝构造函数  Demo(const Demo<N>&);
    // std::uninitialized_copy 会调用 它进行浅拷贝
    // 如果管理指针，析构函数会产生二次释放
    
    
    // 如果删除默认拷贝构造函数：Demo(const Demo<N>&) = delete;
    // template<size_t U> Demo(const Demo<U>&); 则也不会产生该实例
    // std::uninitialized_copy 将无法在 U == T 时调用，只能在不同时调用

    char data[N];
};


int main()
{
    std::vector<Demo<64>> vec;
    for (size_t i = 0; i < 2; i++)
    {
        vec.emplace_back();
    }

    return 0;
}
```

## 解决方案

当需要实现类似上述 **示例3** 的场景（存在类似拷贝构造函数或移动构造函数的模板函数）时，应当对**真正的拷贝构造函数**和**真正的移动构造函数**进行显式特例化。

```c++
#include <cstdio>
#include <vector>

template<size_t N>
struct Demo
{
    ~Demo()
    {
        printf("destructor %p\n", this );
        delete[] data;
    }
    Demo() 
    {
        printf("constructor  %p\n", this);
        data = new float[N];
    }

    // Demo<U> 和 Demo<N> 不是同一个类型，因此这不是真正的移动构造函数
    template<size_t U>
    explicit Demo(Demo<U>&& src) noexcept
    {
        printf("fake move %p\n", this);
        
        if (U >= N)
        {
            data = src.data;
            src.data = nullptr;
        }
        else
        {
            data = new float[N]{0};
            std::copy(data, data + U, src.data);
        }
    } 
    
    // Demo<U> 和 Demo<N> 不是同一个类型，因此这不是真正的拷贝构造函数
    template<size_t U>
    explicit Demo(const Demo<U>& src) 
    {
        printf("fake copy %p\n", this);
        data = new float[N]{0};
        if (U >= N)
        {
            std::copy(data, data + N, src.data);
        }
        else
        {
            std::copy(data, data + U, src.data);
        }
    }
    
    // 显式特化真正的移动构造函数
    explicit Demo(Demo<N>&& src) noexcept
    {
        printf("true move %p\n", this);
        data = src.data;
        src.data = nullptr;
    }
    
    // 显式特化真正的拷贝构造函数
    explicit Demo(const Demo<N>& src) noexcept
    {
        printf("true copy %p\n", this);
        data = new float[N]{0};
        std::copy(data, data + N, src.data);
    }

    float* data;
};

int main()
{
    // 相同类型调用真正的移动构造函数和真正的拷贝构造函数
    {
        Demo<64> demo1;
        Demo<64> demo2{std::move_if_noexcept(demo1)};
        Demo<64> demo3{demo2};
    }
    
    // 不同类型调用模板函数
    {
        Demo<64> demo1;
        Demo<32> demo2{std::move_if_noexcept(demo1)};
        Demo<128> demo3{demo2};
    }
    return 0;
}
```

```
==16139== Memcheck, a memory error detector
==16139== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==16139== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==16139== Command: ./a.out
==16139== 
constructor  0x1ffefffbb0
true move 0x1ffefffbb8
true copy 0x1ffefffbc0
destructor 0x1ffefffbc0
destructor 0x1ffefffbb8
destructor 0x1ffefffbb0
constructor  0x1ffefffbb0
fake move 0x1ffefffbb8
fake copy 0x1ffefffbc0
destructor 0x1ffefffbc0
destructor 0x1ffefffbb8
destructor 0x1ffefffbb0
==16139== 
==16139== HEAP SUMMARY:
==16139==     in use at exit: 0 bytes in 0 blocks
==16139==   total heap usage: 6 allocs, 6 frees, 75,008 bytes allocated
==16139== 
==16139== All heap blocks were freed -- no leaks are possible
==16139== 
==16139== For lists of detected and suppressed errors, rerun with: -s
==16139== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
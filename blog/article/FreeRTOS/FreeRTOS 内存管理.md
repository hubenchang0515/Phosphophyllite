# FreeRTOS 内存管理  
FreeRTOS的内存管理API定义在`heep_1.c`、`heep_2.c`、`heep_3.c`、`heep_4.c`和`heep_5.c`中，这五个文件中的内存管理API有所不同。  
* `heep_1.c`只能分配内存而不能释放内存。  
* `heep_2.c`可以分配和释放内存但不能合并空闲内存块。  
* `heep_3.c`简单的封装了线程安全版的标准C语言malloc和free函数。  
* `heep_4.c`可以合并相邻的空闲内存块。  
* `heep_5.c`可以合并相邻的空闲内存块，且可以管理地址不连续的物理内存。  

分配内存的API是`pvPortMalloc`，释放内存的`API是vPortFree`。  
```C
#include <portable.h>
 
void* pvPortMalloc(size_t xWantedSize);
//分配指定大小的内存
 
void vPortFree(void *pv);
//释放内存，使用heep_1.c的话，这个函数不工作
```

如果使用`heep_5.c`则需要使用`vPortDefineHeapRegions`进行初始化。
```C
#include <portable.h>
void vPortDefineHeapRegions(const HeapRegion_t * const pxHeapRegions);
```
# FreeRTOS 事件标志组  
FreeRTOS可以使用事件标志组进行任务同步，一个事件标准组包含多个事件标志位，每一位标志一个事件。当`configUSE_16BIT_TICKS`为1时，一个事件标志组有8位；当这个宏为0时，一个事件标志组有24位。  

创建事件标志组使用`xEventGroupCreate`。  
```C
#include <event_groups.h>
EventGroupHandle_t xEventGroupCreate(void);
//返回事件标志组句柄，失败返回NULL
```

置位和清除事件标志位使用`xEventGroupSetBits`和`xEventGroupClearBits`。参数是事件标志组句柄和要操作的位。  
```C
#include <event_groups.h>
 
EventBits_t xEventGroupSetBits(EventGroupHandle_t xEventGroup,const EventBits_t uxBitsToSet);
EventBits_t xEventGroupClearBits(EventGroupHandle_t xEventGroup,const EventBits_t uxBitsToClear);
```

`xEventGroupGetBits`获取事件标志组的值。
```C
#include <event_groups.h>
EventBits_t xEventGroupGetBits(EventGroupHandle_t xEventGroup);
```

`xEventGroupWaitBits`阻塞等待事件位。
```C
#include <event_groups.h>
EventBits_t xEventGroupWaitBits(EventGroupHandle_t xEventGroup, 
                                const EventBits_t uxBitsToWaitFor, 
                                const BaseType_t xClearOnExit, 
                                const BaseType_t xWaitForAllBits, 
                                TickType_t xTicksToWait );
```
* 第一个参数是事件标志组句柄  
* 第二个参数是要等待的事件标志位  
* 第三个参数是是否清除位,pdTRUE表示清除,pdFASLE表示不清除  
* 第四个参数是是否等待所有位，pdTRUE表示是，pdFASLE表示否  
* 第五个参数是阻塞超时时间  
```C
//等待bit0 bit1 bit2 bit3，其中任意一位置位就解除阻塞，之后清除bit0 bit1 bit2 bit3
xEventGroupWaitBits(handle,0x0f,pdTRUE,pdFALSE,100/portTICK_RATE_MS);
 
//等待bit0 bit1 bit2 bit3，四个位全部置位才解除阻塞，之后清除bit0 bit1 bit2 bit3
xEventGroupWaitBits(handle,0x0f,pdTRUE,pdTRUE,100/portTICK_RATE_MS);
```
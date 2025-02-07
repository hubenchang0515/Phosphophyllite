# FreeRTOS 中断处理和中断安全API  
FreeRTOS的任务优先级是数值越大，优先级越高，0是最低优先级；而Cortex-M的中断优先级是数值越大，优先级越低，0是最高优先级。  

`FreeRTOSConfig.h`中的宏`configLIBRARY_LOWEST_INTERRUPT_PRIORITY`表示最低中断优先级，从FreeRTOS的demo中复制出来的这个头文件中这个宏的值是15，即从0到15一共16个优先级。Cortex-M的中断优先级有抢占优先级和子优先级两个，但FreeRTOS中没有提供处理子优先级的功能，只使用抢占优先级。因此需要将STM32的中断优先级组设置为16个抢占优先级、1个子优先级，即第四组中断优先级组。  

```C
//优先级组是STM32中优先级分配方式的选择，"组"这个翻译可能不太合适
//使用第四组中断优先级组
NVIC_PriorityGroupConfig(NVIC_PriorityGroup_4);
//STM32有0到4共五组优先级组
//0组：1个抢占优先级，16个子优先级
//1组：2个抢占优先级，8个子优先级
//2组：4个抢占优先级，4个子优先级
//3组：8个抢占优先级，2个子优先级
//4组：16个抢占优先级，1个子优先级
```

`portmacro.h`中的宏`portDISABLE_INTERRUPT()`和`portENABLE_INTERRUPT()`分别关闭和打开优先级低于`FreeRTOSConfig.h`中的宏`configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY`的中断。  

在优先级高于`configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY`的中断服务程序中，不能使用FreeRTOS的任何API。  

FreeRTOS中的任务API可能会让任务进入阻塞，但中断服务程序不是FreeRTOS的任务，因此可能导致错误。因此在优先级低于`configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY`的中断服务程序中，不能使用FreeRTOS的普通API，而必须使用名称中含有`FromISR`的`中断安全API`。  

例如在中断服务程序中：保护临界区，不能使用`taskENTER_CRITICAL()`和`taskEXIT_CRITICAL()`，而应当使用`taskENTER_CRITICAL_FROM_ISR()`和`taskEXIT_CRITICAL_FROM_ISR()`；向队列发送数据不能使用`xQueueSendToBack()`而应当使用`xQueueSendToBackFromISR()`。  
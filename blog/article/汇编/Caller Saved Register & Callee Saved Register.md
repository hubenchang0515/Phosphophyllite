# Caller Saved Register & Callee Saved Register

在使用汇编编程时，调用间需要保存与恢复寄存器，这些寄存器可以由调用者保存恢复（Caller Saved Register）也可以由被调用者保存恢复（Callee Saved Register）。

由于调用者不知道哪些寄存器会被修改，因此只能将所有 Caller Saved Register 进行保存恢复，但这样做效率低下。

因此使用 Callee Saved Register 由被调用者根据需要保存和恢复会被改变的寄存器更常用。需要保存的寄存器如下:  

| 架构          | 被调用者保存的寄存器    |
| :-           | :-                     |
| AMD64        | r12-r15, rbx, rsp, rbp |
| aarch64      | r19-r29 SP v8-v15      |

> v8-v15 是 SIMD 寄存器，被调用者只需要保存低 64 位，高 64 位由调用者保存。
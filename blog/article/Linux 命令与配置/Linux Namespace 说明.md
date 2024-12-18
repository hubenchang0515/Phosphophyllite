# Linux Namespace 说明

Linux Namespace 是 Linux 内核的一组功能，它对内核资源进行分区，以便一组进程看到一组资源，而另一组进程看到一组不同的资源。

目前 Linux 支持 8 种命名空间:   

| 命名空间                                | 说明                              |   内核版本           |
| :-                                     | :-                               | :-                 |
| Mount Namespace                        | 挂载命名空间，用于隔离文件系统        | 2.4.19             |
| UNIX Time-Sharing Namespace            | UTS 命名空间，用于隔离主机名等        | 2.6.19             |
| Inter-Process Communication Namespace  | IPC 命名空间，用于隔离管道、共享内存等 | 2.6.19             |
| Process ID Namespace                   | PID 命名空间，用于隔离进程号         | 2.6.24             |
| Network Namespace                      | 网络命名空间，用于隔离、网络          | 2.6.24             |
| User Namespace                         | 用户命名空间，用于隔离用户            | 3.8               |
| CGroup Namespace                       | CGroup 命名空间，用于隔离 GGroup     | 4.6               |
| Time Namespace                         | 时间命名空间，用于隔离时间            | 5.6               |

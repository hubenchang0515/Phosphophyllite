# 在 enum class 中使用 bitmask 组合的方法

可以通过重载 `|` 运算符实现 bitmask 组合，例如:  

```c++
enum class SystemNamespaceType
{
    MOUNT   = CLONE_NEWNS,      // Mount Namespace
    UTS     = CLONE_NEWUTS,     // UNIX Time-Sharing Namespace
    IPC     = CLONE_NEWIPC,     // Inter-Process Communication Namespace
    PID     = CLONE_NEWPID,     // Process ID Namespace
    NET     = CLONE_NEWNET,     // Network Namespace
    USER    = CLONE_NEWUSER,    // User Namespace
    CGROUP  = CLONE_NEWCGROUP,  // CGroup Namespace
};

SystemNamespaceType operator | (SystemNamespaceType x, SystemNamespaceType y)
{
    return static_cast<SystemNamespaceType>(static_cast<int>(x) | static_cast<int>(y));
}
```
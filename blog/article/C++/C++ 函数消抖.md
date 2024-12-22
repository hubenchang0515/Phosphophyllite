# C++ 函数消抖

**函数消抖** 指在短时间内连续多次调用同一函数，仅最后一次调用生效。

形如:  
```c++
auto debouncedFn = debounce(fn, 100);
```

通常将需要消抖的函数封装成一个新的函数，新的函数进行延迟后调用原函数:  
* 如果在延时结束前再次调用，则重新开始延时
* 如果在延时结束前没有再次调用，则使调用原函数

## 实现

```c++
#include <functional>
#include <chrono>
#include <thread>
#include <mutex>
#include <future>
#include <memory>
#include <exception>

/*************************************************************************
 * @brief 函数消抖
 * @param fn 希望消抖函数
 * @param ms 消抖的延时时间，毫秒
 * @return 一个封装了消抖功能的函数
 *************************************************************************/
template<typename R, typename... ARGS>
std::function<std::shared_ptr<std::promise<R>>(ARGS...)> debounce(std::function<R(ARGS...)> fn, int ms)
{
    auto lambda = [fn = std::move(fn), ms](ARGS... args) mutable -> std::shared_ptr<std::promise<R>> {
        std::shared_ptr<std::promise<R>> promise = std::make_shared<std::promise<R>>();
        static auto lastCallTime = std::chrono::steady_clock::now();
        static bool cancel = false;
        static std::thread thread;
        static std::mutex mutex;

        if (thread.joinable())
        {
            mutex.lock();
            cancel = true;
            mutex.unlock();

            thread.join();

            mutex.lock();
            cancel = false;
            mutex.unlock();
        }

        thread = std::thread([fn, ms, promise, args...]() mutable {
            std::this_thread::sleep_until(lastCallTime + std::chrono::milliseconds(ms));

            mutex.lock();
            if (cancel)
            {
                mutex.unlock();
                promise->set_exception(std::make_exception_ptr(std::runtime_error("cancel")));
                return;
            }
            mutex.unlock();

            promise->set_value(fn(args...));
            thread.detach();
        });

        return promise;
    };

    return lambda;
}
```

## 测试

```c++
#include <cstdio>

int hello(int x, int y)
{
    int n = x + y;
    printf("hello world %d\n", n);
    return n;
}

int main()
{
    auto fn = debounce(std::function<int(int,int)>(hello), 1000);
    auto p1 = fn(2, 3);
    auto p2 = fn(4, 5);

    auto f1 = p1->get_future();
    auto f2 = p2->get_future();

    try {
        if (f1.valid())
            printf("%d\n", f1.get());
    } catch (std::runtime_error e) {
        printf("%s\n", e.what());
    }

    try {
        if (f2.valid())
            printf("%d\n", f2.get());
    } catch (std::runtime_error e) {
        printf("%s\n", e.what());
    }
    return 0;
}
```

结果:  

```
hello world 9
cancel
9
```
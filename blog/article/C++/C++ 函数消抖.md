# C++ 函数消抖

**函数消抖** 指在短时间内连续多次调用同一函数，仅最后一次调用生效。

形如:  
```c++
auto debouncedFn = debounce(fn, 100);
```

通常将需要消抖的函数封装成一个新的函数，新的函数进行延迟后调用原函数:  
* 如果在延时结束前再次调用，则重新开始延时
* 如果在延时结束前没有再次调用，则使调用原函数

## 示例

> 这个实现存在一个问题，那就是通过 `thread.join();` 等待上一次调用取消，会产生阻塞，不能用于实际开发。

```c++
#include <functional>
#include <chrono>
#include <thread>
#include <mutex>
#include <future>
#include <memory>
#include <exception>

namespace Utils
{

template<typename R, typename... ARGS>
std::enable_if_t<!std::is_void_v<R> && (!std::is_void_v<ARGS> && ...), void>
invoke(std::shared_ptr<std::promise<R>> promise, std::function<R(ARGS...)> fn, ARGS... args)
{
    promise->set_value(fn(args...));
}

template<typename R>
void invoke(std::shared_ptr<std::promise<R>> promise, std::function<R(void)> fn)
{
    promise->set_value(fn());
}

template<typename... ARGS>
void invoke(std::shared_ptr<std::promise<void>> promise, std::function<void(ARGS...)> fn, ARGS... args)
{
    fn(args...);
    promise->set_value();
}

void invoke(std::shared_ptr<std::promise<void>> promise, std::function<void(void)> fn)
{
    fn();
    promise->set_value();
}

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

            // promise->set_value(fn(args...));
            invoke(promise, fn, args...);
            thread.detach();
        });

        return promise;
    };

    return lambda;
}

template<typename R, typename... ARGS>
std::function<std::shared_ptr<std::promise<R>>(ARGS...)> debounce(R(*fn)(ARGS...), int ms)
{
    return debounce(static_cast<std::function<R(ARGS...)>>(fn), ms);
}

}; // namespace Utils
```

## 测试

```c++
int main()
{
    auto fn = Utils::debounce(test, 1000);
    auto p1 = fn(1, 2);
    auto p2 = fn(3, 4);

    auto f1 = p1->get_future();
    auto f2 = p2->get_future();

    f1.wait();
    f2.wait();

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
test 3 4
cancel
7
```
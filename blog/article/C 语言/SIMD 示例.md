# SIMD 示例

所谓 SIMD 就是一次指令计算多个数据，例如 AVX256 一次计算 256 位数据。
* int 是 32 位，所以 AVX256 一次计算 8 个
* double 是 64 位，所以一次计算 4 个

以计算 double 加法为例:  
```c
__m256d m256x; // 定义标识 AVX 寄存器的变量
__m256d m256y;

m256x = _mm256_set_pd(x[i+3], x[i+2], x[i+1], x[i]); // 向 AVX 寄存器中写入数据，大端序
m256y = _mm256_set_pd(y[i+3], y[i+2], y[i+1], y[i]);
m256x = _mm256_add_pd(m256x, m256y);                 // 一次操作 4 对 double 数据的加法

double o[4] __attribute__((aligned(32)));
_mm256_store_pd(o, m256x);                           // 读出结果，必须 32 位对齐
```

> 使用 gcc 编译时，需要附带 `-mavx2` 选项。

在 Linux 上，执行 `cat /proc/cpuinfo | grep flags` 命令可以查看 CPU 支持哪些特性:  
```
$ cat /proc/cpuinfo | grep flags
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat 
pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp 
lm constant_tsc rep_good nopl nonstop_tsc cpuid extd_apicid aperfmperf pni 
pclmulqdq monitor ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx 
f16c rdrand lahf_lm cmp_legacy svm extapic cr8_legacy abm sse4a misalignsse 
3dnowprefetch osvw ibs skinit wdt tce topoext perfctr_core perfctr_nb bpext 
perfctr_llc mwaitx cpb cat_l3 cdp_l3 hw_pstate ssbd mba ibrs ibpb stibp 
vmmcall fsgsbase bmi1 avx2 smep bmi2 erms invpcid cqm rdt_a rdseed adx smap 
clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves cqm_llc cqm_occup_llc 
cqm_mbm_total cqm_mbm_local clzero irperf xsaveerptr rdpru wbnoinvd arat npt 
lbrv svm_lock nrip_save tsc_scale vmcb_clean flushbyasid decodeassists 
pausefilter pfthreshold avic v_vmsave_vmload vgif v_spec_ctrl umip pku ospke 
vaes vpclmulqdq rdpid overflow_recov succor smca fsrm
```

| 名称   | 说明                                               |
| :-:    | :-                                                 |
| MMX    | 64位整型                                           |
| SSE	   | 128位单精度浮点                                     |
| SSE2   | 扩展128位整型、双精度浮点，CPU快取的控制指令          |
| SSE3   | 扩展类型转换，超线程支持                             |
| SSE4   | 扩展 CRC32 等指令                                  |
| AVX    | 256位浮点                                          |
| AVX2   | 扩展256位整型，三操作数指令（3-Operand Instructions）|
| AVX512 | 512位运算                                          |

* MMX 是 MultiMedia eXtensions 的缩写
* SSE 是 Streaming SIMD Extensions 的缩写
* AVX 是 Advanced Vector Extensions 的缩写

注意不要混用不同的指令（例如同时使用 AVX 和 SSE），否则将会引发 transition penalty，造成性能损失。

在 gcc 中需要引用 `x86intrin.h` 头文件，在 MSVC 中需要引用 `intrin.h` 头文件。

具体的:  

```c
#include <mmintrin.h>   // mmx, 4个64位寄存器
#include <xmmintrin.h>  // sse, 8个128位寄存器
#include <emmintrin.h>  // sse2, 8个128位寄存器
#include <pmmintrin.h>  // sse3, 8个128位寄存器
#include <smmintrin.h>  // sse4.1, 8个128位寄存器
#include <nmmintrin.h>  // sse4.2, 8个128位寄存器
#include <immintrin.h>  // avx, 16个256位寄存器
```

示例程序 demo1.c 中，可以看到使用 avx256 和直接计算，耗时差不多，甚至直接计算反而更快。这是因为运算过于简单，数据拷贝占用的时间更高。
因此使用 SIMD 的时候，需要把算法的步骤组合起来，在一次 IO 中进行尽可能多的运算。

> 另外还发现，在 AMD Ryzen 9 5900HX 上使用 gcc 编译，优化级别设为 `-O0` 时，AVX256 会比直接计算慢很多。
> 不清楚是 CPU 的原因还是编译器的原因。

## 示例1

```c
#include <stdio.h>
#include <string.h>
#include <x86intrin.h>
#include <time.h>

void avx256_vector_add(const double* x, const double* y, size_t n, double* out);
void avx256_vector_sub(const double* x, const double* y, size_t n, double* out);
void avx256_vector_mul(const double* x, const double* y, size_t n, double* out);
void avx256_vector_div(const double* x, const double* y, size_t n, double* out);

void vector_add(const double* x, const double* y, size_t n, double* out);
void vector_sub(const double* x, const double* y, size_t n, double* out);
void vector_mul(const double* x, const double* y, size_t n, double* out);
void vector_div(const double* x, const double* y, size_t n, double* out);

#define TEST(func, ...) do{                                             \
                            clock_t start = clock();                    \
                            func(__VA_ARGS__);                          \
                            clock_t end = clock();                      \
                            printf(#func " cost: %ld\n", end - start);  \
                        }while(0)

int main(void)
{
    const size_t N = 2048;
    double x[N];
    double y[N];
    double out[N];

    TEST(avx256_vector_add, x, y, N, out);
    TEST(avx256_vector_sub, x, y, N, out);
    TEST(avx256_vector_mul, x, y, N, out);
    TEST(avx256_vector_div, x, y, N, out);

    TEST(vector_add, x, y, N, out);
    TEST(vector_sub, x, y, N, out);
    TEST(vector_mul, x, y, N, out);
    TEST(vector_div, x, y, N, out);
}

void avx256_vector_add(const double* x, const double* y, size_t n, double* out)
{
    __m256d m256x;
    __m256d m256y;
    double o[4] __attribute__((aligned(32)));

    size_t i = 0;
    for (; i + 3 < n; i+=4)
    {
        m256x = _mm256_set_pd(x[i+3], x[i+2], x[i+1], x[i]);
        m256y = _mm256_set_pd(y[i+3], y[i+2], y[i+1], y[i]);
        m256x = _mm256_add_pd(m256x, m256y);
        _mm256_store_pd(o, m256x);

        memcpy(out, o, sizeof(double) * 4);
    }

    // 剩下少量没对齐的数据没必要使用 SIMD
    for(;i < n; i++)
    {
        out[i] = x[i] + y[i];
    }
}

void avx256_vector_sub(const double* x, const double* y, size_t n, double* out)
{
    __m256d m256x;
    __m256d m256y;
    double o[4] __attribute__((aligned(32)));

    size_t i = 0;
    for (; i + 3 < n; i+=4)
    {
        m256x = _mm256_set_pd(x[i+3], x[i+2], x[i+1], x[i]);
        m256y = _mm256_set_pd(y[i+3], y[i+2], y[i+1], y[i]);
        m256x = _mm256_sub_pd(m256x, m256y);
        _mm256_store_pd(o, m256x);

        memcpy(out, o, sizeof(double) * 4);
    }

    // 剩下少量没对齐的数据没必要使用 SIMD
    for(;i < n; i++)
    {
        out[i] = x[i] - y[i];
    }
}

void avx256_vector_mul(const double* x, const double* y, size_t n, double* out)
{
    __m256d m256x;
    __m256d m256y;
    double o[4] __attribute__((aligned(32)));

    size_t i = 0;
    for (; i + 3 < n; i+=4)
    {
        m256x = _mm256_set_pd(x[i+3], x[i+2], x[i+1], x[i]);
        m256y = _mm256_set_pd(y[i+3], y[i+2], y[i+1], y[i]);
        m256x = _mm256_mul_pd(m256x, m256y);
        _mm256_store_pd(o, m256x);

        memcpy(out, o, sizeof(double) * 4);
    }

    // 剩下少量没对齐的数据没必要使用 SIMD
    for(;i < n; i++)
    {
        out[i] = x[i] * y[i];
    }
}

void avx256_vector_div(const double* x, const double* y, size_t n, double* out)
{
    __m256d m256x;
    __m256d m256y;
    double o[4] __attribute__((aligned(32)));

    size_t i = 0;
    for (; i + 3 < n; i+=4)
    {
        m256x = _mm256_set_pd(x[i+3], x[i+2], x[i+1], x[i]);
        m256y = _mm256_set_pd(y[i+3], y[i+2], y[i+1], y[i]);
        m256x = _mm256_div_pd(m256x, m256y);
        _mm256_store_pd(o, m256x);

        memcpy(out, o, sizeof(double) * 4);
    }

    // 剩下少量没对齐的数据没必要使用 SIMD
    for(;i < n; i++)
    {
        out[i] = x[i] / y[i];
    }
}

void vector_add(const double* x, const double* y, size_t n, double* out)
{
    for (size_t i = 0; i < n; i++)
    {
        out[i] = x[i] + y[i];
    }
}
void vector_sub(const double* x, const double* y, size_t n, double* out)
{
    for (size_t i = 0; i < n; i++)
    {
        out[i] = x[i] - y[i];
    }
}

void vector_mul(const double* x, const double* y, size_t n, double* out)
{
    for (size_t i = 0; i < n; i++)
    {
        out[i] = x[i] * y[i];
    }
}

void vector_div(const double* x, const double* y, size_t n, double* out)
{
    for (size_t i = 0; i < n; i++)
    {
        out[i] = x[i] / y[i];
    }
}
```

## 示例2

```c
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <x86intrin.h>
#include <time.h>

double avx256_pi(size_t limit);
double pi(size_t limit);

#define TEST(func, ...) do{                                             \
                            clock_t start = clock();                    \
                            func(__VA_ARGS__);                          \
                            clock_t end = clock();                      \
                            printf(#func " cost: %ld\n", end - start);  \
                        }while(0)

int main(void)
{
    #define N 0xfffff

    TEST(pi, N);
    printf("%f\n", pi(N));

    TEST(avx256_pi, N);
    printf("%f\n", avx256_pi(N));


}

double avx256_pi(size_t limit)
{
    // ∑(1 / n^2) = pi^2 / 6

    __m256d sum = _mm256_set1_pd(0.0); // 四个 double 都设为同一个值 0.0
    __m256d one = _mm256_set1_pd(1.0);
    __m256d temp;

    for (size_t n = 1; n + 3 < limit; n+=4)
    {
        temp = _mm256_set_pd(n+3.0, n+2.0, n+1.0, n);
        temp = _mm256_mul_pd(temp, temp);
        temp = _mm256_div_pd(one, temp);
        sum = _mm256_add_pd(sum, temp);
    }


    double o[4] __attribute__((aligned(32)));
    _mm256_store_pd(o, sum);

    return sqrt(6*(o[0] + o[1] + o[2] + o[3]));
}

double pi(size_t limit)
{
    // // ∑(1 / n^2) = pi^2 / 6

    double sum = 0.0;
    for (size_t n = 1; n < limit; n++)
    {
        sum += 1.0 / n / n;
    }

    return sqrt(6 * sum);
}
```
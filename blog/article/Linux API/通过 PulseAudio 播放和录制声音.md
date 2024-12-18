# 通过 PulseAudio 播放和录制声音

```c
// libs: -lpulse 
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <stdbool.h>
#include <pulse/pulseaudio.h>

#ifdef DEBUG
    #define LOG(...) printf(__VA_ARGS__)
#else
    #define LOG(...)
#endif

typedef enum Method
{
    METHOD_PLAY,
    METHOD_RECORD
}Method;

typedef struct UserData
{
    pa_context* context;
    pa_stream* stream;
    pa_mainloop_api* api;
    FILE* fp;
    Method method;
}UserData;

static void mainloop_quit(UserData* userdata, int ret);
static void context_state_callback(pa_context* context, void* userdata) ;
static void stream_write_callback(pa_stream* stream, size_t length, void* userdata);
static void stream_read_callback(pa_stream* stream, size_t length, void* userdata);
static void stream_drain_complete(pa_stream* stream, int success, void* userdata);
static void context_drain_complete(pa_context* c, void* userdata);

int main(int argc, char* argv[]) 
{
    // 参数检查
    if(argc != 3)
    {
        printf("pademo [play|record] <sound-file>\n");
        return EXIT_FAILURE;
    }

    // 创建一个线程，并在该线程中创建 mainloop
    pa_mainloop* mainloop = pa_mainloop_new();
    if(mainloop == NULL)
    {
        fprintf(stderr, "pa_threaded_mainloop_new failed.\n");
        return EXIT_FAILURE;
    }

    // 获取API
    pa_mainloop_api* api = pa_mainloop_get_api(mainloop);
    if(api == NULL)
    {
        pa_mainloop_free(mainloop);
        fprintf(stderr, "pa_threaded_mainloop_get_api failed.\n");
        return EXIT_FAILURE;
    }

    // 创建上下文
    pa_context* context = pa_context_new(api, "demo");
    if(context == NULL)
    {
        pa_mainloop_free(mainloop);
        fprintf(stderr, "pa_context_new failed.\n");
        return EXIT_FAILURE;
    }

    UserData data;
    if(strcmp(argv[1],"play") == 0)
    {
        data.fp = fopen(argv[2], "rb");
        data.method = METHOD_PLAY;
    } 
    else if(strcmp(argv[1], "record") == 0)
    {
        data.fp = fopen(argv[2], "wb");
        data.method = METHOD_RECORD;
    }
    else
    {
        fprintf(stderr, "Unknown method %s\n", argv[1]);
        // 释放
        pa_context_unref(context);
        pa_mainloop_free(mainloop);
        return EXIT_FAILURE;
    }

    // 设置状态变化的回调函数,这是主入口
    data.context = context;
    data.api = api;
    pa_context_set_state_callback(context, context_state_callback, (void*)(&data));

    // 开始建立连接
    if(pa_context_connect(context, NULL, PA_CONTEXT_NOFAIL, NULL) < 0)
    {
        pa_context_unref(context);
        pa_mainloop_free(mainloop);
        fprintf(stderr, "pa_context_connect failed.\n");
        return EXIT_FAILURE;
    }
    
    // 运行mainloop
    int ret = pa_mainloop_run(mainloop, NULL);

    // 退出
    pa_context_unref(context);
    pa_mainloop_free(mainloop);
    return ret;
}

// 退出主循环
static void mainloop_quit(UserData* userdata, int ret)
{
    LOG("mainloop_quit\n");
    userdata->api->quit(userdata->api, ret);
}

// 状态变化的回调函数
static void context_state_callback(pa_context* context, void* userdata) 
{
    UserData* data = (UserData*)(userdata);
    pa_context_state_t state = pa_context_get_state(context);
    switch (state) 
    {
    case PA_CONTEXT_READY: // 上下文就绪
    {
        LOG("PA_CONTEXT_READY\n");

        // 创建spec
        pa_sample_spec sampleSpec;
        sampleSpec.rate = 44100;
        sampleSpec.format = PA_SAMPLE_S16LE;
        sampleSpec.channels = 2;

        // 创建channel map
        pa_channel_map channelMap;
        pa_channel_map_init_stereo(&channelMap);

        // 创建stream
        pa_stream* stream = pa_stream_new(context, "demo-stream", &sampleSpec, &channelMap);
        data->stream = stream;

        if(data->method == METHOD_PLAY) // 播放
        {
            pa_stream_connect_playback(stream, NULL, NULL, PA_STREAM_NOFLAGS, NULL, NULL);
            pa_stream_set_write_callback(stream, stream_write_callback, userdata);
        }
        else if(data->method == METHOD_RECORD) // 录音
        {
            pa_stream_connect_record(stream, NULL, NULL, PA_STREAM_NOFLAGS);
            pa_stream_set_read_callback(stream, stream_read_callback, userdata);
        }
        break;
    }

    case PA_CONTEXT_TERMINATED: // 结束
        LOG("PA_CONTEXT_TERMINATED\n");
        mainloop_quit(data, EXIT_SUCCESS);
        break;

    default:
        LOG("context state %d\n", state);
    }
}

// 播放的回调
static void stream_write_callback(pa_stream* stream, size_t length, void* userdata)
{
    UserData* data = (UserData*)(userdata);
    void* buffer;
    while(true)
    {
        // 给buffer分配空间，不需要手动释放
        pa_stream_begin_write(stream, &buffer, &length); 
        
        // 读取文件,写入stream
        length = fread(buffer, 1, length, data->fp);
        pa_stream_write(stream, buffer, length, NULL, 0, PA_SEEK_RELATIVE); // 会自动释放buffer
        LOG("play %zu bytes\n", length);

        // 文件读取完毕
        if(feof(data->fp))
        {
            pa_stream_cancel_write(stream);
            pa_stream_set_write_callback(stream, NULL, NULL); //清除回调
            pa_operation* o = pa_stream_drain(stream, stream_drain_complete, data); // 设置播放完毕时的回调
            if(o == NULL)
            {
                mainloop_quit(data, EXIT_FAILURE);
            }
            pa_operation_unref(o);
            break;
        }
    }
}

// 录音的回调
static void stream_read_callback(pa_stream* stream, size_t length, void* userdata)
{
    UserData* data = (UserData*)(userdata);
    const void *buffer;
    while(pa_stream_readable_size(stream) > 0)
    {
        pa_stream_peek(stream, &buffer, &length);
        if(buffer == NULL || length <= 0)
        {
            continue;
        }

        fwrite(buffer, length, 1, data->fp);
        fflush(data->fp);
        LOG("record %zu bytes\n", length);
        pa_stream_drop(stream);
    }
}

// 播放完毕的回调
static void stream_drain_complete(pa_stream* stream, int success, void* userdata) 
{
    (void)(success);
    LOG("stream_drain_complete\n");
    UserData* data = (UserData*)(userdata);

    // 释放stream
    pa_stream_disconnect(stream); 
    pa_stream_unref(stream);
    data->stream = NULL;

    // 设置上下文结束的回调
    pa_operation* o = pa_context_drain(data->context, context_drain_complete, NULL);
    if (o == NULL)
    {
        pa_context_disconnect(data->context);
    }
    else 
    {
        pa_operation_unref(o);
    }
}

// 上下文结束的回调
static void context_drain_complete(pa_context* context, void* userdata)
{
    (void)(userdata);
    LOG("context_drain_complete\n");
    pa_context_disconnect(context);
}
```
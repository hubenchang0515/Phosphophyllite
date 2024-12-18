# 通过 ALSA 显示音频设备的声道

```c
// apt install libasound2-dev
// LDFLAGS := -lasound
#include <stdio.h>
#include <stdlib.h>
#include <alsa/asoundlib.h>

int main(int argc, char* argv[])
{
    if(argc != 2)
    {
        fprintf(stderr, "Usage: %s <device>\n", argv[0]);
        fprintf(stderr, "       %s hw:0,0\n", argv[0]);
        return EXIT_FAILURE;
    }

    snd_pcm_t* pcm = NULL;
    if(snd_pcm_open(&pcm, argv[1], SND_PCM_STREAM_PLAYBACK, 0) < 0)
    {
        fprintf(stderr, "snd_pcm_open failed\n");
        return EXIT_FAILURE;
    }

    snd_pcm_chmap_query_t** chmaps = snd_pcm_query_chmaps(pcm);
    if(chmaps == NULL)
    {
        fprintf(stderr, "snd_pcm_query_chmaps failed\n");
        return EXIT_FAILURE;
    }

    for(int i = 0; chmaps[i] != NULL; i++)
    {
        snd_pcm_chmap_query_t* mapping = chmaps[i];
        printf("Mapping-%d\n", i);
        for(int ch = 0; ch < mapping->map.channels; ch++)
        {
            printf("\tchannel-%d %s\n", ch, snd_pcm_chmap_long_name(mapping->map.pos[ch]));
        }
    }

    snd_pcm_free_chmaps(chmaps);

    return EXIT_SUCCESS;
}
```
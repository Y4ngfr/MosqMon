#include <stdio.h>
#include <stdlib.h>
#include <SDL2/SDL.h>
#include "../IncludeFiles/AudioRecording.h"

// Baseado em https://gist.github.com/andraantariksa/f5e6d848364b11a425625ec7fbbfc187

int openRecordingDevice(AudioDevice** recordingDevice, int indexOfRecordingDevice)
{
    SDL_AudioSpec *desiredSpecPtr, *obtainedSpecPtr;

    *recordingDevice = (AudioDevice*)SDL_malloc(sizeof(AudioDevice));

    if(*recordingDevice == NULL)
    {
        printf("Erro ao alocar dispositivo de gravação\n");
        return -1;
    }

    (*recordingDevice)->audioData = (AudioData*)SDL_malloc(sizeof(AudioData));

    if((*recordingDevice)->audioData == NULL)
    {
        printf("Erro ao alocar dados de áudio\n");
        SDL_CloseAudioDevice((*recordingDevice)->deviceID);
        return -1;
    }

    (*recordingDevice)->index = indexOfRecordingDevice;
    (*recordingDevice)->name = SDL_GetAudioDeviceName((*recordingDevice)->index, SDL_TRUE);

    (*recordingDevice)->desiredSpec.format = AUDIO_S16SYS;
    (*recordingDevice)->desiredSpec.freq = 44100;
    (*recordingDevice)->desiredSpec.samples = 4096;
    (*recordingDevice)->desiredSpec.channels = 2;
    (*recordingDevice)->desiredSpec.callback = recordingCallback;
    (*recordingDevice)->desiredSpec.userdata = (*recordingDevice)->audioData;

    desiredSpecPtr = &((*recordingDevice)->desiredSpec);
    obtainedSpecPtr = &((*recordingDevice)->obtainedSpec);

    (*recordingDevice)->deviceID = SDL_OpenAudioDevice((*recordingDevice)->name, SDL_TRUE,
    desiredSpecPtr, obtainedSpecPtr, SDL_AUDIO_ALLOW_ANY_CHANGE);

    if((*recordingDevice)->deviceID == 0)
    {
        printf("Erro ao abrir o dispositivo de gravação. Erro: %s\n", SDL_GetError());
        SDL_CloseAudioDevice((*recordingDevice)->deviceID);
        free((*recordingDevice)->audioData);
        return -1;
    }

    return 0;
}

void record(AudioDevice* recordingDevice, Uint8* buffer, Uint32 bufferMaxPosition)
{
    recordingDevice->audioData->buffer = buffer;
    recordingDevice->audioData->position = 0;

    // start recording
    SDL_PauseAudioDevice(recordingDevice->deviceID, SDL_FALSE);

    while(1)
    {
        SDL_LockAudioDevice(recordingDevice->deviceID);

        if(recordingDevice->audioData->position > bufferMaxPosition)
        {   // end recording
            SDL_UnlockAudioDevice(recordingDevice->deviceID);
            SDL_PauseAudioDevice(recordingDevice->deviceID, SDL_TRUE);
            break;
        }

        SDL_UnlockAudioDevice(recordingDevice->deviceID);
    }
}

void recordingCallback(void* userdata, Uint8* stream, int streamLength)
{
    AudioData* recordingData = (AudioData*)userdata;

    SDL_memcpy(&((recordingData->buffer)[recordingData->position]), stream, streamLength);

    recordingData->position += (Uint32)streamLength;
}

Uint32 getBytesPerSecond(SDL_AudioSpec obtainedRecordingSpec)
{
    int bytesPerSample, channels, frequency;
    SDL_AudioFormat audioFormat;
    Uint32 bufferSize, bytesPerSecond;

    audioFormat = obtainedRecordingSpec.format;
    channels = (int)obtainedRecordingSpec.channels;
    frequency = obtainedRecordingSpec.freq;

    bytesPerSample = channels * (SDL_AUDIO_BITSIZE(audioFormat) / 8);
    bytesPerSecond = frequency * bytesPerSample;

    return bytesPerSecond;
}

void closeDevice(AudioDevice* audioDevice)
{
    free(audioDevice->audioData);
    SDL_CloseAudioDevice(audioDevice->deviceID);
    free(audioDevice);
}
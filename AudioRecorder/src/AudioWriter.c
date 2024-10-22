#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <SDL2/SDL.h>
#include <sndfile.h>
#include "../IncludeFiles/AudioRecording.h"
#include "../IncludeFiles/AudioWriter.h"

int saveRecordingAudio(char* directory, AudioDevice* recordingDevice, Uint32 bufferSize)
{
    SNDFILE* sndfp;
    SF_INFO sfInfo;
    sf_count_t size;   
    char* path;

    path = getPathString(directory);

    if(path == NULL){
        return -1;
    }

    printf("%s\n", path);

    memset(&sfInfo, 0, sizeof(SF_INFO));

    sfInfo.channels = recordingDevice->obtainedSpec.channels;
    sfInfo.format = SF_FORMAT_WAV | SF_FORMAT_PCM_16 | SF_ENDIAN_FILE;
    sfInfo.samplerate = recordingDevice->obtainedSpec.freq;

    if(sf_format_check(&sfInfo) == SF_TRUE)
    {
        sndfp = sf_open(path, SFM_WRITE, &sfInfo);

        if(sndfp == NULL)
        {
            printf("Erro, arquivo não encontrado\n");
            free(path);
            return -1;
        }

        sf_write_raw(sndfp, recordingDevice->audioData->buffer, bufferSize);
    }
    else{
        printf("formato de áudio inválido\n");
        free(path);
        return -1;
    }

    free(path);
    sf_close(sndfp);

    return 0;
}

char* getPathString(char* directory)
{
    char* fullPath, *dateTimeString;
    int pathStringSize;

    dateTimeString = getDateAndTimeString();

    if(dateTimeString == NULL){
        return NULL;
    }

    pathStringSize = strlen(directory) + strlen("/audio ");

    fullPath = (char*)malloc((pathStringSize + strlen(dateTimeString) + 5) * sizeof(char));

    if(fullPath == NULL)
    {
        printf("Falha ao alocar string do diretório\n");
        return NULL;
    }

    strcpy(fullPath, directory);
    strcat(fullPath, "/audio ");
    strcat(fullPath, dateTimeString);
    strcat(fullPath, ".wav");

    free(dateTimeString);

    return fullPath;
}

char* getDateAndTimeString()
{
    time_t seconds;
    struct tm *dateAndTime;
    char *dateBuffer, *millisseconds;

    dateBuffer = (char*)malloc(27*sizeof(char));
    memset(dateBuffer, '\0', 27);

    if(dateBuffer == NULL){
        printf("Erro ao alocar string de data e hora\n");
        return NULL;
    }

    time(&seconds);
    dateAndTime = localtime(&seconds);

    if(dateAndTime->tm_mday < 10)
    {
        dateBuffer[0] = '0';
        SDL_itoa(dateAndTime->tm_mday, dateBuffer+1, 10);
    }
    else{
        SDL_itoa(dateAndTime->tm_mday, dateBuffer, 10);
    }

    dateBuffer[2] = '-';

    if(dateAndTime->tm_mon + 1 < 10 )
    {
        dateBuffer[3] = '0';
        SDL_itoa(dateAndTime->tm_mon + 1, dateBuffer+4, 10);
    }
    else{
        SDL_itoa(dateAndTime->tm_mon + 1, dateBuffer+3, 10);
    }

    dateBuffer[5] = '-';

    SDL_itoa(dateAndTime->tm_year + 1900, dateBuffer+6, 10);

    dateBuffer[10] = ' '; dateBuffer[11] = -61; dateBuffer[12] = -96; 
    dateBuffer[13] = 's'; dateBuffer[14] = ' '; 

    if(dateAndTime->tm_hour < 10)
    {
        dateBuffer[15] = '0';
        SDL_itoa(dateAndTime->tm_hour, dateBuffer+16, 10);
    }
    else{
        SDL_itoa(dateAndTime->tm_hour, dateBuffer+15, 10);
    }

    dateBuffer[17] = ':';

    if(dateAndTime->tm_min < 10)
    {
        dateBuffer[18] = '0';
        SDL_itoa(dateAndTime->tm_min, dateBuffer+19, 10);
    }
    else{
        SDL_itoa(dateAndTime->tm_min, dateBuffer+18, 10);
    }

    dateBuffer[20] = ':';

    if(dateAndTime->tm_sec < 10)
    {
        dateBuffer[21] = '0';
        SDL_itoa(dateAndTime->tm_sec, dateBuffer+22, 10);
    }
    else{
        SDL_itoa(dateAndTime->tm_sec, dateBuffer+21, 10);
    }

    millisseconds = getMillisseconds();

    if(millisseconds == NULL){
        printf("Erro ao alocar string de data e hora\n");
        return NULL;
    }

    dateBuffer[23] = ':';
    dateBuffer[24] = millisseconds[0];
    dateBuffer[25] = millisseconds[1];
    dateBuffer[26] = '\0';

    free(millisseconds);

    return dateBuffer;
}

char* getMillisseconds()
{
    char *result, *aux;
    int length, index;
    float value;

    value = (float)clock() / CLOCKS_PER_SEC;
    length = snprintf(NULL, 0, "%f", value);

    aux = (char*)malloc((length+1)*sizeof(char));

    if(aux == NULL){
        return NULL;
    }

    sprintf(aux, "%f", value);

    result = (char*)malloc(2*sizeof(char));

    if(result == NULL){
        free(aux);
        return NULL;
    }

    index = 0;
    while(aux[index] != '.') index++;

    result[0] = aux[index + 1];
    result[1] = aux[index + 2];

    free(aux);

    return result;
}
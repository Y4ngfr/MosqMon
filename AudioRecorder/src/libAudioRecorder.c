#include "../IncludeFiles/libAudioRecorder.h"
#include <signal.h>

int endRecording = 0;

int runRecorder(RecordingParams *inputData)
{
    AudioDevice *recordingDevice;
    Uint32 byteRate, allocationSize;
    Uint8* audioBuffer;
    int repetitions;

    if(verifyInputData(inputData) < 0){
        return -1;
    }

    if(inputData->helpArgument){
        printHelpMessage();
        return 0;
    }

    if(SDL_Init(SDL_INIT_AUDIO) < 0)
    {
        printf("Erro ao iniciar SDL. Erro: %s\n", SDL_GetError());
        return -1;
    }

    if(inputData->deviceArgument){
        listDevices();
        SDL_Quit();
        return 0;
    }

    if(openRecordingDevice(&recordingDevice, inputData->deviceIndex) < 0)
    {
        SDL_Quit();
        return -1;
    }

    byteRate = getBytesPerSecond(recordingDevice->obtainedSpec);
    allocationSize = byteRate * ((Uint32)inputData->recordingTime + 1);
    audioBuffer = (Uint8*)SDL_malloc(allocationSize * sizeof(Uint8));

    if(audioBuffer == NULL)
    {
        printf("Erro ao alocar buffer de gravação\n");
        closeDevice(recordingDevice);
        SDL_Quit();
        return -1;
    }

    repetitions = inputData->repetitions;

    SDL_Thread *thread = SDL_CreateThread(threadWaitForInput, "thread", NULL);
    signal(SIGINT, sighandler);

    do{
        Uint32 bufferLength;

        bufferLength = byteRate * inputData->recordingTime;

        record(recordingDevice, audioBuffer, bufferLength);

        if(saveRecordingAudio(inputData->directory, recordingDevice,
        bufferLength) < 0)
        {
            SDL_free(audioBuffer);
            closeDevice(recordingDevice);
            SDL_Quit();
            return -1;
        }                    

        repetitions--;

    } while(!endRecording && (repetitions != 0 || inputData->repetitions == 0));

    // if(inputData->repetitions == 0){
        // SDL_WaitThread(thread, NULL);
    // }

    SDL_free(audioBuffer);
    closeDevice(recordingDevice);
    SDL_Quit();

    return 0;
}

int threadWaitForInput()
{
    while(getchar() != '\n')
    {
        SDL_Delay(10);
    }

    endRecording = 1;

    return 0;
}

void printHelpMessage()
{
    printf("Uso: audioRecorder [options] file...\n");
    printf("Options:\n");
    printf("--help                       Mostra informações de ajuda\n");
    printf("--devices                    Lista os dispositivos de gravação\n");
    printf("-t <arg>                     Define o tempo de gravação em segundos\n");
    printf("-o <directory>               Define o diretório de saída\n");
    printf("-r <arg>                     Define quantas vezes a gravação se repete (definir como 0 para repetir indefinidamente)\n");
    printf("-i <arg>                     Define o índice do dispositivo de gravação\n");
    printf("Exemplo: gravador -i 0 -o meu/diretorio/ -t 5 -r 10\n");
    printf("Grava 10 áudios de 5 segundos com o dispositivo de gravação 0 e coloca em meu/diretorio\n");
}

void listDevices()
{
    int numberOfRecordingDevices, i;

    numberOfRecordingDevices = SDL_GetNumAudioDevices(SDL_TRUE);

    if(numberOfRecordingDevices < 1)
    {
        printf("Falha ao encontrar dispositivos de gravação de áudio\n");
        return;
    }

    printf("Dispositivos de gravação de áudio:\n");

    for(i=0; i < numberOfRecordingDevices; i++)
    {
        const char* deviceName;

        deviceName = SDL_GetAudioDeviceName(i, SDL_TRUE);

        printf("index: %d; Device: %s\n", i, deviceName);
    }   
}

int verifyInputData(RecordingParams* inputData)
{
    if(inputData->deviceArgument == 0 && inputData->helpArgument == 0)
    {
        if(inputData->recordingTime == 0)
        {
            printf("Erro: Tempo de gravação não pode ser 0\n");
            return -1;
        }

        if(inputData->directory == NULL)
        {
            printf("Erro: Argumento de diretório inválido\n");
            return -1;
        }
    }

    return 0;
}

void sighandler()
{
    endRecording = 1;
}
#ifndef _AUDIORECORDING_H
#define _AUDIORECORDING_H

#include <SDL2/SDL.h>

/**
 * Estrutura que armazena os dados brutos do áudio gravado
*/
typedef struct AudioData{
    Uint8* buffer; /** Buffer que contém as amostras do áudio */
    Uint32 position; /** Valor usado como posição do buffer. Ex: buffer[position] */
} AudioData;

/**
 * Use a função openRecordingDevice() para abrir o dispositivo de áudio, definindo
 * os valores e alocando a memória necessária para os atributos dessa estrutura. 
 * Use closeDevice() para limpar a memória e fechar o dispositivo.
*/
typedef struct AudioDevice{
    int index; /** Indice do dispositivo de gravação */
    const char* name; /** Nome do dispositivo de gravação */
    SDL_AudioDeviceID deviceID; /** Estrutura SDL do dispositvo de áudio */
    SDL_AudioSpec desiredSpec; /** Estrutura SDL que contém as especificações desejadas do dispositivo de áudio */
    SDL_AudioSpec obtainedSpec; /** Estrutura SDL que contém as especificações obtidas do dispositivo de áudio */
    AudioData* audioData; /** Estrutura que contém os dados brutos do áudio */
} AudioDevice;

/**
 * Abre o dispositivo de áudio e define valores para todos os atributos da estrutura
 * AudioDevice.
 * \param recordingDevice Ponteiro duplo para a estrutura AudioDevice (não é necessário pré-alocar dinamicamente)
 * \param indexOfRecordingDevice Indice do dispositivo de gravação
 * \returns Retorna 0 caso sucesso e -1 caso ocorra um erro
 * 
*/
int openRecordingDevice(AudioDevice** recordingDevice, int indexOfRecordingDevice);

/**
 * Executa o loop de gravação e coloca todos os dados de áudio obtidos dentro de buffer
 * \param recordingDevice Dispositivo de gravação que será utilizado
 * \param buffer Buffer onde serão gravadas as amostras do áudio
 * \param bufferMaxPosition Posição máxima do buffer (pode ser obtido através da fórmula: bytesPerSecond * recordingTime )
*/
void record(AudioDevice* recordingDevice, Uint8* buffer, Uint32 bufferMaxPosition);

/**
 * Função de callback chamada automaticamente pela biblioteca SDL quando o
 * stream do dispositivo de gravação precisar de mais dados
 * \param userdata Parâmetro específico de aplicação utilizado pela função
 * \param stream Ponteiro para a stream de áudio
 * \param streamLength Tamanho da stream de áudio
*/
void recordingCallback(void* userdata, Uint8* stream, int streamLength);

/**
 * Calcula a taxa de bytes por segundo de acordo com as especificações obtidas
 * do dispositivo de gravação de áudio
 * \param obtainedRecordingSpec Especificações obtidas do dispositvo de gravação de áudio
 * \returns Retorna a taxa de bytes por segundo como um inteiro sem sinal de 32 bits 
*/
Uint32 getBytesPerSecond(SDL_AudioSpec obtainedRecordingSpec);

/**
 * Fecha o dispositivo de áudio (Não desaloca o buffer de AudioData)
 * \param audioDevice Ponteiro para AudioDevice que deseja liberar
*/
void closeDevice(AudioDevice* audioDevice);

#endif
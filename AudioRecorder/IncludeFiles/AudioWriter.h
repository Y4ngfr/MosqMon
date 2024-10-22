#ifndef _AUDIOWRITER_H
#define _AUDIOWRITER_H

#include <sndfile.h>
#include "AudioRecording.h"

/**
 * Salva o(s) audio(s) gravado(s) em formato WAV
 * \param directory String que indica o diretório de saída do áudios
 * \param recordingDevice Estrutura que contém informações importantes
 *        e o buffer do áudio gravado
 * \param bufferSize Tamanho, em bytes, do áudio gravado que será salvo
 * \returns Retorna 0 caso sucesso e -1 caso tenha ocorrido um erro
*/
int saveRecordingAudio(char* directory, AudioDevice* recordingDevice, Uint32 bufferSize);

/**
 * Retorna o caminho completo do arquivo de áudio que será salvo
 * \param directory String que indica o diretório de saída do áudio
 * \returns String alocada dinamicamente que contém o diretorio mais
 *          o nome e extensão do arquivo que será salvo
*/
char* getPathString(char* directory);

/**
 * Busca informações de data, horario e millissegundos e retora-os
 * para serem utilizados pela função saveRecordingAudio() para compor
 * o nome do arquivo
 * \returns Retorna uma string alocada dinamicamente que segue o padrão:
 * dd-mm-aa às hh:mm:ss:msms (dia-mês-ano às horas:minutos:segundos:milissegundos)
*/
char* getDateAndTimeString();

/**
 * Calcula, com precisão, quanto tempo em segundos desde que o programa começou, 
 * porém retorna apenas as duas primeiras casas decimais depois virgula. Por 
 * exemplo, se o programa está funcionando à 3.4567 segundos, o retorno será 45
 * \returns Retorna uma string (de tamanho 2), alocada dinamicamente, que representa
 * o número explicado acima
*/
char* getMillisseconds();

#endif
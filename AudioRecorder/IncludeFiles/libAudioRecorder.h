#ifndef _LIBAUDIORECORDER_H
#define _LIBAUDIORECORDER_H

#include "AudioRecording.h"
#include "AudioWriter.h"
#include "InputReader.h"

/**
 *  Executa o gravador com base nos argumentos de inputData
*/
int runRecorder(RecordingParams *inputData);

/**
 *  Função de thread que espera o usuário apertar enter para encerrar a gravação (função de uso interno)
*/
int threadWaitForInput();

/**
 * Imprime uma lista dos dispositivos de gravação detectados precedidos pelo seu indice
*/
void listDevices();

/**
 * Imprime as informações de ajuda
*/
void printHelpMessage();

/**
 * Verifica se os campos estão corretamente preenchidos
*/
int verifyInputData(RecordingParams* inputData);

void sighandler();

#endif
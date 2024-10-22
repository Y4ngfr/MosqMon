#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <string.h>
#include <ctype.h>
#include "../IncludeFiles/InputReader.h"

int readInput(int argc, char* argv[], RecordingParams* inputData)
{
    int option, opt_flag;
    int optT = 0, optI = 0, optR = 0, optO = 0;
    FILE *fp;

    Option long_options[] = {
        {"help", no_argument, &opt_flag, 0},
        {"devices", no_argument, &opt_flag, 1}
    };

    inputData->deviceArgument = 0;
    inputData->deviceIndex = 0;
    inputData->directory = NULL;
    inputData->helpArgument = 0;
    inputData->recordingTime = 0.0;
    inputData->repetitions = 0;

    if(argc == 1){
        inputData->helpArgument = 1;
        return 0;
    }

    do{
        option = getopt_long(argc, argv, "i:t:o:r:", long_options, NULL);

        switch(option)
        {
            case 0:
            {
                if(opt_flag == 1){
                    inputData->deviceArgument = 1;
                }

                if(opt_flag == 0){
                    inputData->helpArgument = 1;
                }

                return 0;
            }
                
            case 't':
            {
                char auxarg[5];

                if(strlen(optarg) <= 0){
                    printf("Erro na opção -t, não foi possível obter valor do parâmetro\n");
                    return -1;
                }

                sprintf(auxarg, "%.2f", strtod(optarg, NULL));

                inputData->recordingTime = strtod(auxarg, NULL);

                if(inputData->recordingTime == 0 || strtod(optarg, NULL) <= 0){
                    printf("Erro na opção -t: argumento inválido `%s`\n", optarg);
                    return -1;
                }

                optT = 1;

                break;
            }   

            case 'r':
            {
                int isZero;

                inputData->repetitions = atoi(optarg);
                isZero = !strcmp(optarg, "0");

                if(inputData->repetitions == 0 && !isZero || atoi(optarg) < 0){
                    printf("Erro na opção -r: argumento inválido `%s`\n", optarg);
                    return -1;
                }

                optR = 1;

                break;
            }
                
            case 'i':
            {
                int isZero;

                inputData->deviceIndex = atoi(optarg);
                isZero = !strcmp(optarg, "0");

                if(inputData->deviceIndex == 0 && !isZero || atoi(optarg) < 0){
                    printf("Erro na opção -i: argumento inválido `%s`\n", optarg);
                    return -1;
                }

                optI = 1;

                break;
            }

            case 'o':
            {
                inputData->directory = optarg;
                optO = 1;

                break;
            }

            case '?':
            {
                if(isprint(optopt)){ // Verifica se o caractere é imprimível
                    printf("Opção `-%c` não reconhecida\n", optopt);
                }
                else{
                    printf("Caractere `\\x%x` não reconhecido\n", optopt);
                }

                return -1;
            }
                
            case -1:
                break;
        }

    }while(option != -1);

    if(!(optI && optO && optR && optT)){
        
        if(!optI) printf("Erro: argumento -i ausente\n");
        if(!optT) printf("Erro: argumento -t ausente\n");
        if(!optR) printf("Erro: argumento -r ausente\n");
        if(!optO) printf("Erro: argumento -o ausente\n");

        return -1;
    }

    return 0;
}
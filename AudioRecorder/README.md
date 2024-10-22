O repositório presente trata-se de um gravador de áudio 100% escrito em C.

Dependências:
é necessário ter instalado as duas bibliotecas SDL2 e SNDFILE
SDL2: sudo apt install libsdl2-dev
SNDFILE: sudo apt install libsndfile1-dev

SDL2 faz o interfaceamento com o sistema operacional para acessar e utilizar os dispositivos de áudio do computador
o SNDFILE codifica o cabeçalho de um arquivo .WAV corretamente

Instalação:
Após a instalação das duas bibliotecas, para instalar o programa basta clonar o repositório e executa make all (irá pedir a senha de usuário).

Como usar:
Para usar o programa basta digitar audioRecorder no terminal que irá automaticamente mostrar a ajuda.
Uso: audioRecorder [options] file...
Options:
--help                       Mostra informações de ajuda
--devices                    Lista os dispositivos de gravação
-t <arg>                     Define o tempo de gravação em segundos
-o <directory>               Define o diretório de saída
-r <arg>                     Define quantas vezes a gravação se repete (definir como 0 para repetir indefinidamente)
-i <arg>                     Define o índice do dispositivo de gravação
Exemplo: gravador -i 0 -o meu/diretorio/ -t 5 -r 10
Grava 10 áudios de 5 segundos com o dispositivo de gravação 0 e coloca em meu/diretorio

API:
Você pode utilizar o gravador como uma API para seus programas, basta importar libAudioRecorder.h, em seguida preencher manualmente a struct RecordingParams (ler documentação).
Tendo feito isso, por fim basta chamar a função runRecorder passanto o ponteiro para o RecordingParams definido para executar o gravador dentro de qualquer processo.

Desenvolvimento:
O gravador está divido em 3 partes principais, as quais você pode encontrar no repositório: 
InputReader: Trata-se do parser de entrada. Foi escrito utilizando a biblioteca getopt do gnu, ela define structs e funções para analisar o vetor de strings da entrada.
AudioWritter: Parte do sistema que irá salvar o arquivo de áudio, utiliza a biblioteca sndfile que configura corretamente o cabeçalho do arquivo de áudio.
AudioRecording: Parte do sistema que irá de fato gravar o áudio utilizando a biblioteca SDL2

Além disso também há um parte do gravador que centraliza e coordenas essas 3 partes do sistema, para que assim seja priorizada a modularização.

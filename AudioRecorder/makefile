# ´;´ separa comando do shell e ´\´ ignora a quebra de linha
# sintaxe: if then fi ou if then else fi

all: Criar Mover CriarExecutavel MoverExecutavel

Criar:
	if [ ! -e /usr/local/include/libAudioRecorder ] ; then \
		sudo mkdir /usr/local/include/libAudioRecorder ; \
	fi

Mover: Compilar CriarBibliotecaEstatica
	sudo cp libAudioRecorder/libAudioRecorder.a /usr/local/lib
	sudo cp IncludeFiles/* /usr/local/include/libAudioRecorder

CriarBibliotecaEstatica: Compilar
	ar -rc libAudioRecorder/libAudioRecorder.a objects/*
	ranlib libAudioRecorder/libAudioRecorder.a

Compilar:
	gcc -c src/AudioRecording.c -g -o objects/AudioRecording.o
	gcc -c src/AudioWriter.c -g -o objects/AudioWriter.o
	gcc -c src/libAudioRecorder.c -g -o objects/libAudioRecorder.o
	gcc -c src/InputReader.c -g -o objects/InputReader.o

CriarExecutavel:
	gcc main.c src/* -g -o audioRecorder -lSDL2 -lsndfile

MoverExecutavel:
	if [ -e "/usr/local/bin/audioRecorder" ] ; then \
		sudo rm /usr/local/bin/audioRecorder ; \
	fi
	sudo cp audioRecorder /usr/local/bin
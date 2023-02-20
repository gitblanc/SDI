import os
from random import randrange


class Pregunta:
    def __init__(self, respuestasCorrecta, respuestas, enunciado):
        self.respuestasCorrectas = respuestasCorrecta
        self.respuestas = respuestas
        self.enunciado = enunciado

    def check_answer(self, str):
        for i in range(0, len(self.respuestas)):
            if((str+")") in self.respuestas[i]):
                if(i+1 in self.respuestasCorrectas):
                    return True
        return False


class Marks:
    def __init__(self):
        self.total = 0
        self.acertadas = 0
    def acierto(self):
        self.acertadas+=1
    def pregunta(self):
        self.total+=1
    def puntuacion(self):
        return "Resultado: "+bcolors.OKGREEN+str("%.2f" % ((self.acertadas/self.total)*10)) + bcolors.ENDC+" || Total:"+str(self.total)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ColorPrinter:
    def print( color, text):
        print(color + text + bcolors.ENDC)


def delete_answer(respuesta):
    return respuesta.replace(";", "")


def load_preguntas():
    file_preguntas = input("Fichero de preguntas: ")
    print("Leyendo preguntas de: "+file_preguntas)
    file_to_read = open(file_preguntas, 'r', encoding='utf-8')
    lines = file_to_read.readlines()
    preguntas = []
    num_respuestas = int(lines[0].split(";")[0])+1
    for i in range(1, len(lines), num_respuestas):
        respuestas = list([])
        correctIndex = list([])
        for j in range(i+1, i+num_respuestas):
            if(";" in lines[j]):
                correctIndex.append((j-1) % (num_respuestas))
        for k in range(1, num_respuestas):
            respuestas.append(lines[k+i].replace("\n", ""))
        preguntas.append(Pregunta(correctIndex, list( map(delete_answer, respuestas)), lines[i].replace("\n","")))
    return preguntas

##Inicio
preguntas = load_preguntas()

print("Todas las preguntas procesadas! Comenzando:")
marks=Marks()
playing = True
acertadas = 0
totales = 0
while (playing):
    index = randrange(start=0, stop=len(preguntas))
    pregunta = preguntas[index]
    ColorPrinter.print(bcolors.BOLD, pregunta.enunciado)
    
    for respuesta in pregunta.respuestas:
        print(respuesta)
    answer = input("Respuesta: ")
    if(answer == "0"):
        playing = False
    else:
        os.system ("cls") 
        if(Pregunta.check_answer(pregunta, answer)):
            marks.acierto()
            ColorPrinter.print(bcolors.OKGREEN, "Correcta!!")
        else:
            ColorPrinter.print(bcolors.FAIL, pregunta.enunciado)
            ColorPrinter.print(bcolors.WARNING, "Respuesta incorrecta")
            for i in pregunta.respuestasCorrectas:
                ColorPrinter.print(bcolors.OKGREEN, "Correcta: "+bcolors.WARNING + pregunta.respuestas[i-1]+bcolors.ENDC)
        marks.pregunta()

print(marks.puntuacion())
print("Adios")

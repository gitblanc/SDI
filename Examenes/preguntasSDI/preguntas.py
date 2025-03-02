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



class RandomIndex:
    def __init__(self, number_of_questions):
        self.number_of_questions = number_of_questions
    
    def first_index(self):
        return randrange(start=0, stop=self.number_of_questions)
    
    def next_index(self):
        return randrange(start=0, stop=self.number_of_questions)
    
    def restart(self):
        pass
    
class RandomIndexNoRepetition:
    def __init__(self, number_of_questions):
        self.number_of_questions = number_of_questions
        self.indexes = {}
    
    def first_index(self):
        index = randrange(start=0, stop=self.number_of_questions)
        self.indexes[index] = True
        return index
    
    def next_index(self):
        index = randrange(start=0, stop=self.number_of_questions)
        while index in self.indexes:
            index = randrange(start=0, stop=self.number_of_questions)
        self.indexes[index] = True
        if(len(self.indexes) == self.number_of_questions):
            self.restart()
        return index
    
    def restart(self):
        self.indexes = {}

class SequentialIndex:
    def __init__(self, number_of_questions):
        self.number_of_questions = number_of_questions
        self.index = 0
    
    def first_index(self):
        return 0
    
    def next_index(self):
        returnIndex = self.index + 1
        self.index = returnIndex
        if returnIndex == self.number_of_questions - 1:
            self.restart()
        return returnIndex
    
    def restart(self):
        self.index = -1
    


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

def load_indexmode():
    print("Selecciona orden de preguntas: ")
    print("1. Aleatorio")
    print("2. Aleatorio sin repeticion")
    print("3. Secuencial")
    mode = input("Modo: ")
    if mode == "1":
        return RandomIndex(len(preguntas))
    elif mode == "2":
        return RandomIndexNoRepetition(len(preguntas))
    elif mode == "3":
        return SequentialIndex(len(preguntas))
    else:
        print("Modo inválido")
        return load_indexmode()

##Inicio
preguntas = load_preguntas()
modoIndex = load_indexmode()

print("Todas las preguntas procesadas! Comenzando:")
marks=Marks()
playing = True
acertadas = 0
totales = 0
index = modoIndex.first_index()
while (playing):
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
    index = modoIndex.next_index()

print(marks.puntuacion())
print("Adios")

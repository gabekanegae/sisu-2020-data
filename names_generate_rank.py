import csv
import os
from time import time

class Curso:
    def __init__(self, a):
        self.alunos = [Aluno(a[i:i+6], a[0]) for i in range(1, len(a), 6)]

class Aluno:
    def __init__(self, m, curso):
        self.codigo, self.nome, self.posicao, self.nota, self.modNome, self.bonus = m
        self.curso = curso
        self.nota = float(self.nota) / (1 + float(self.bonus)/100)

t0 = time()

directory = "data"
filename = input("Filename (without extension): /{}/".format(directory)).strip()

##################################################

# Read csv and process strings
try:
    with open(os.path.join(directory, filename + ".csv"), "r", encoding="UTF-8") as csvFile:
        csvFileReader = csv.reader(csvFile, delimiter=";")
        cursos = [Curso(a) for a in csvFileReader]
except FileNotFoundError:
    print("File /{}/{}.csv not found.".format(directory, filename))
    exit()

alunos = []
for c in cursos:
    alunos += c.alunos

alunos = sorted(alunos, key=lambda x: (x.nota), reverse=True)

# Write to .txt
with open(os.path.join(directory, filename + "_rank" + ".txt"), "w+", encoding="UTF-8") as humanFile:
    for i, a in enumerate(alunos):
        pct = (1-(i+1)/len(alunos))*100
        humanFile.write("{:>6} - {:>7.3f}% | {:>6.2f} - {} ({})\n".format(i+1, pct, a.nota, a.nome, a.curso))

print("Written {} students to '{}_rank.txt' in {:.1f}s.".format(len(alunos), directory+"/"+filename, time()-t0))
import csv
import os
from time import time

class Modalidade:
    def __init__(self, m):
        self.modNome, self.vagas, self.nota, self.bonus, self.dataNota = m

class Curso:
    def __init__(self, l):
        self.codigo, self.cursoNome, self.cursoGrau, self.cursoTurno, self.vagasTotais = l[:5]
        self.campusNome, self.campusCidade, self.campusUF, self.iesNome, self.iesSG = l[5:10]
        self.pesNAT, self.pesHUM, self.pesLIN, self.pesMAT, self.pesRED = l[10:15]
        self.minNAT, self.minHUM, self.minLIN, self.minMAT, self.minRED, self.minTOT = l[15:21]

        self.modalidades = [Modalidade(l[i:i+5]) for i in range(21, len(l), 5)]

directory = "data"
filenames = ["cursos_22", "cursos_23", "cursos_24", "cursos_25", "cursos_26"]

t0 = time()

dados = dict()
for filename in filenames:
    with open(os.path.join(directory, filename + ".csv"), "r", encoding="UTF-8") as csvFile:
        dados[filename] = [Curso(l) for l in csv.reader(csvFile, delimiter=";")]

stats = dict()
for filename in filenames:
    totalCursos = len(dados[filename])
    totalMod = sum(len(curso.modalidades) for curso in dados[filename])
    totalACMod = sum([sum([m.modNome == "Ampla concorrência" for m in curso.modalidades]) for curso in dados[filename]])
    totalVagas = sum([int(curso.vagasTotais) for curso in dados[filename]])
    totalACVagas = sum([sum([int(m.vagas) for m in curso.modalidades if m.modNome == "Ampla concorrência"]) for curso in dados[filename]])

    stats[filename] = (totalCursos, totalMod, totalACMod, totalVagas, totalACVagas)
    # print(filename, stats[filename])

# Verify if all .csv files have the same attributes
for filename in filenames[1:]:
    assert(stats[filename] == stats[filenames[0]])

print("="*25 + " Geral " + "="*25)

totalCursos, totalMod, totalACMod, totalVagas, totalACVagas = stats[filenames[0]]

print("Total de cursos: {}".format(totalCursos))
print("Total de modalidades: {}".format(totalMod))
# print("  Modalidades AC: {} ({:.2f}%)".format(totalACMod, totalACMod/totalMod*100))
print("Total de vagas: {}".format(totalVagas))
print("  Vagas AC: {} ({:.2f}%)".format(totalACVagas, totalACVagas/totalVagas*100))

print("="*57)
print()

for dia, dado in dados.items():
    print("="*25 + " {}/01 ".format(dia[-2:]) + "="*25)

    inscritosMod = sum([sum([m.nota != ".00" for m in curso.modalidades]) for curso in dado])
    print("Modalidades com nota de corte: {} ({:.2f}%)".format(inscritosMod, inscritosMod/totalMod*100))

    # totalACMod = sum([sum([m.modNome == "Ampla concorrência" for m in curso.modalidades]) for curso in dado])
    # inscritosACMod = sum([sum([m.nota != ".00" for m in curso.modalidades if m.modNome == "Ampla concorrência"]) for curso in dado])
    # print("  Modalidades AC com nota de corte: {} ({:.2f}%)".format(inscritosACMod, inscritosACMod/totalACMod*100))

    # totalNaoACMod = sum([sum([m.modNome != "Ampla concorrência" for m in curso.modalidades]) for curso in dado])
    # inscritosNaoACMod = sum([sum([m.nota != ".00" for m in curso.modalidades if m.modNome != "Ampla concorrência"]) for curso in dado])
    # print("  Modalidades não AC com nota de corte: {} ({:.2f}%)".format(inscritosNaoACMod, inscritosNaoACMod/totalNaoACMod*100))

    totalVagasAcima0 = sum([sum([int(m.vagas) for m in curso.modalidades if float(m.nota) > 0]) for curso in dado])
    totalVagas = sum([sum([int(m.vagas) for m in curso.modalidades]) for curso in dado])
    print("Vagas com nota de corte: {} ({:.2f}%)".format(totalVagasAcima0, totalVagasAcima0/totalVagas*100))

    # somaNotasMod = sum([sum([float(m.nota) for m in curso.modalidades]) for curso in dado])
    # print("Nota de corte média: {:.2f}".format(somaNotasMod/totalMod))
    # print("Nota de corte média: {:.2f}".format(somaNotasMod/inscritosMod))

    somaNotasMod = sum([sum([float(m.nota)*int(m.vagas) for m in curso.modalidades]) for curso in dado])
    print("Nota de corte média: {:.2f}".format(somaNotasMod/totalVagasAcima0))

    for corte in [600, 650, 700, 750, 800, 850, 900]:
        totalVagasAcimaCorte = sum([sum([int(m.vagas) for m in curso.modalidades if float(m.nota) > corte]) for curso in dado])
        print("  Vagas com nota de corte abaixo de {}: {} ({:.2f}%)".format(corte, totalVagasAcimaCorte, totalVagasAcimaCorte/totalVagasAcima0*100))

print("="*57)
print()

print("Done in {:.3f}s.".format(time()-t0))
import requests
import csv
import os
from datetime import datetime
from time import time

modNomeReduzido = {
"Ampla concorrência": "AC",

"Candidato (s) Pessoas com Deficiências - PCD": "PCD",
"com deficiência": "PCD",
"Candidato (s) com deficiência.": "PCD",
"Candidatos com deficiência:": "PCD",

"que independentemente da renda, tenham cursado integralmente o ensino médio em escolas públicas. (L3)": "EP",
"Candidatos que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "EP",
"Candidatos que tenham cursado integral e exclusivamente os ensinos fundamental e médio em estabelecimentos da rede pública de ensino.": "EP",
"Candidato (s) que tenham cursado integral, exclusiva e regularmente os anos finais do Ensino Fundamental (6º ao 9º ano) e todo o Ensino Médio em escolas da rede pública estadual ou municipal, excluindo-se os candidatos que tenham concluído curso de nível superior ainda que pendente a colação de grau.": "EP",
"Candidato (s) Oriundos da rede pública de ensino.": "EP",
"COTAS - Escolas Públicas -  Lei Estadual no 6.542, de 7 de dezembro de 2004": "EP",
"Candidatos Egressos da Escola Pública, de baixa renda:": "EP",

"Candidatos autodeclarados pretos, pardos ou indígenas que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PPI + EP",
"Candidatos que tenha cursado integral e exclusivamente os ensinos fundamental e médio em estabelecimentos da rede pública de ensino e que se autodeclarem negros.": "PPI + EP",
"NEGROS (pretos e pardos) que cursaram integralmente o Ensino Médio em escolas públicas (Banca avaliadora obrigatória)": "PPI + EP",
"autodeclarados pretos, pardos ou indígenas que, independentemente da renda, tenham cursado integralmente o ensino médio em escolas públicas. (L4)": "PPI + EP",

"Candidatos com deficiência que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + EP",
"com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo, que tenham cursado integralmente o ensino médio em escolas públicas. (L1)": "RENDA + EP",
"Candidatos com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "RENDA + EP",
"autodeclarados pretos, pardos ou indígenas com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo, que tenham cursado integralmente o ensino médio em escolas públicas. (L2)": "PPI + RENDA + EP",
"Candidatos autodeclarados pretos, pardos ou indígenas, com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PPI + RENDA + EP",
"Candidatos com deficiência autodeclarados pretos, pardos ou indígenas que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PPI + PCD + EP",
"Candidatos com deficiência autodeclarados pretos, pardos ou indígenas, que tenham renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012)": "PPI + PCD + RENDA + EP",
"Candidatos com deficiência que tenham renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + RENDA + EP",
"Candidatos autodeclarados indígenas que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "INDIGENA + EP",
"INDÍGENAS que cursaram integralmente o Ensino Médio em escolas públicas": "INDIGENA + EP",
"Candidatos autodeclarados indígenas, com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e  que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "INDIGENA + RENDA + EP",
"Candidatos Indígenas, de baixa renda que sejam egressos de escola pública:": "INDIGENA + RENDA + EP",
"Candidatos Negros, de baixa renda que sejam egresso de escola pública:": "PRETO/PARDO + RENDA + EP",
"Candidatos autodeclarados pretos ou pardos que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PRETO/PARDO + EP",
"Candidatos autodeclarados pretos ou pardos, com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PRETO/PARDO + RENDA + EP",
"Candidatos com deficiência autodeclarados pretos ou pardos que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + PRETO/PARDO + EP",
"Candidatos com deficiência autodeclarados pretos ou pardos, que tenham renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + PRETO/PARDO + RENDA + EP",
}

class Modalidade:
    def __init__(self, m):
        self.modNome, self.vagas, self.nota, self.bonus, self.dataNota = m

        for k, v in modNomeReduzido.items():
            if self.modNome == k:
                self.modNome = v
                break

    def __str__(self):
        s = [
             "\t{}{}:".format(self.modNome, " (+{}%)".format(self.bonus) if self.bonus and self.bonus != ".00" else ""),
             "\t\tVagas: {} | Nota de Corte: {}".format(self.vagas, self.nota)
            ]

        return "\n".join(s)

class Curso:
    def __init__(self, l):
        self.codigo, self.cursoNome, self.cursoGrau, self.cursoTurno, self.vagasTotais = l[:5]
        self.campusNome, self.campusCidade, self.campusUF, self.iesNome, self.iesSG = l[5:10]
        self.pesNAT, self.pesHUM, self.pesLIN, self.pesMAT, self.pesRED = l[10:15]
        self.minNAT, self.minHUM, self.minLIN, self.minMAT, self.minRED, self.minTOT = l[15:21]

        self.modalidades = [Modalidade(l[i:i+5]) for i in range(21, len(l), 5)]

    def __str__(self):
        s = [
             "{} ({}) - {}, {}, {}".format(self.iesNome, self.iesSG, self.campusNome, self.campusCidade, self.campusUF),
             "{}, {}, {}".format(self.cursoNome, self.cursoGrau, self.cursoTurno),
             "Total de Vagas: {}".format(self.vagasTotais),
             "Pesos: NAT={}, HUM={}, LIN={}, MAT={}, RED={} | Mínimo: NAT={}, HUM={}, LIN={}, MAT={}, RED={}, TOTAL={}".format(self.pesNAT, self.pesHUM, self.pesLIN, self.pesMAT, self.pesRED, self.minNAT, self.minHUM, self.minLIN, self.minMAT, self.minRED, self.minTOT)
            ]

        self.modalidades = sorted(self.modalidades, key=lambda x: (x.nota), reverse=True)
        mods = [m.__str__() for m in self.modalidades]

        return "\n".join(s+mods)

t0 = time()

directory = "data"
filename = "cursos_" + str(datetime.today().day)

##################################################

with open(os.path.join(directory, filename + ".csv"), "r", encoding="UTF-8") as csvFile:
    csvFileReader = csv.reader(csvFile, delimiter=";")
    cursos = [Curso(l) for l in csvFileReader]

cursos = sorted(cursos, key=lambda x: (x.campusUF, x.iesNome, x.campusCidade, x.campusNome, x.cursoNome))

with open(os.path.join(directory, filename + ".txt"), "w+", encoding="UTF-8") as humanFile:
    for i, curso in enumerate(cursos):
        nl = str(curso).index("\n")

        if str(cursos[i]).split("\n")[0] != str(cursos[i-1]).split("\n")[0]:
            humanFile.write("="*50 + "\n")
            humanFile.write(str(curso)[:nl] + "\n")
            humanFile.write("="*50 + "\n")
        humanFile.write(str(curso)[nl+1:] + "\n")
        humanFile.write("\n")

print("Written to '{}.txt' in {:.1f}s.".format(directory+"/"+filename, time()-t0))
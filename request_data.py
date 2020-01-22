import requests
import csv
import os
from datetime import datetime
from time import time

directory = "data"
filename = "cursos_" + str(datetime.today().day) + ".csv"

baseURL = "https://sisu-api.apps.mec.gov.br/api/v1/oferta/{}/modalidades"

t0 = time()
errors = []

##################################################

with open("ids_cursos.txt") as f:
    ids = [int(id_.strip()) for id_ in f.readlines() if id_]

ids = sorted(list(set(ids))) # Sort and remove duplicates

csvFile = open(os.path.join(directory, filename), "w+", encoding="UTF-8")
csvFileWriter = csv.writer(csvFile,  delimiter=";", quotechar="\"", quoting=csv.QUOTE_ALL, lineterminator="\n")

print("Reading {} responses...".format(len(ids)))

for id_ in ids:
    response = requests.get(baseURL.format(id_))
    if response.status_code != 200:
        print("[{}] Error {}".format(id_, response.status_code))
        errors.append((id_, response.status_code))
        continue
    response = response.json()

    codigo = response["oferta"]["co_oferta"]
    cursoNome = response["oferta"]["no_curso"]
    cursoGrau = response["oferta"]["no_grau"]
    cursoTurno = response["oferta"]["no_turno"]
    vagasTotais = response["oferta"]["qt_vagas_sem1"]

    campusNome = response["oferta"]["no_campus"]
    campusCidade = response["oferta"]["no_municipio_campus"]
    campusUF = response["oferta"]["sg_uf_campus"]
    iesNome = response["oferta"]["no_ies"]
    iesSG = response["oferta"]["sg_ies"]

    pesNAT = response["oferta"]["nu_peso_cn"]
    pesHUM = response["oferta"]["nu_peso_ch"]
    pesLIN = response["oferta"]["nu_peso_l"]
    pesMAT = response["oferta"]["nu_peso_m"]
    pesRED = response["oferta"]["nu_peso_r"]

    minNAT = response["oferta"]["nu_nmin_cn"]
    minHUM = response["oferta"]["nu_nmin_ch"]
    minLIN = response["oferta"]["nu_nmin_l"]
    minMAT = response["oferta"]["nu_nmin_m"]
    minRED = response["oferta"]["nu_nmin_r"]
    minTOT = response["oferta"]["nu_media_minima"]

    modalidades = [{campo: m[campo] for campo in ["no_concorrencia", "qt_vagas", "nu_nota_corte", "qt_bonus_perc", "dt_nota_corte"]} for m in response["modalidades"]]

    print("[{}] {} ({}) - {}".format(codigo, iesNome, iesSG, cursoNome))

    # Write to CSV
    csvLine = [codigo, cursoNome, cursoGrau, cursoTurno, vagasTotais,
                 campusNome, campusCidade, campusUF, iesNome, iesSG,
                 pesNAT, pesHUM, pesLIN, pesMAT, pesRED,
                 minNAT, minHUM, minLIN, minMAT, minRED, minTOT]
    for m in modalidades:
        if int(m["qt_vagas"]) > 0: # Remove modalities with no available roles
            csvLine += [v for v in m.values()]
    
    csvFileWriter.writerow(tuple(csvLine))

print("Parsed {} responses to '{}' in {:.1f}s with {} errors.".format(len(ids), directory+"/"+filename, time()-t0, len(errors)))
if errors:
    print("Errors:")
    for e in errors:
        print("\t{} - Error {}".format(e[0], e[1]))
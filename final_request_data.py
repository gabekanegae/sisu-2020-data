import requests
import csv
import os
from time import time, sleep

directory = "data"
filename = input("Filename (without extension): /{}/".format(directory)).strip()

baseURL = "https://sisu-api.apps.mec.gov.br/api/v1/oferta/{}/selecionados"

t0 = time()
errors = []

##################################################

with open("all_id_list.txt") as f:
    ids = [int(id_.strip()) for id_ in f.readlines() if id_]

ids = sorted(list(set(ids))) # Sort and remove duplicates

print("Will write to file '/{}/{}.csv'.".format(directory, filename))

csvFile = open(os.path.join(directory, filename + ".csv"), "w+", encoding="UTF-8")
csvFileWriter = csv.writer(csvFile,  delimiter=";", quotechar="\"", quoting=csv.QUOTE_ALL, lineterminator="\n")

print("Reading {} responses...".format(len(ids)))

for id_ in ids:
    while True:
        try:
            response = requests.get(baseURL.format(id_))
            break
        except:
            print("[{}] An exception occured, retrying...".format(id_))
            sleep(1)

    if response.status_code != 200:
        print("[{}] Error {}".format(id_, response.status_code))
        errors.append((id_, response.status_code))
        continue
    response = response.json()

    csvLine = [id_]
    for r in response:
        codigo_aluno = r["co_inscricao_enem"]
        nome = r["no_inscrito"]
        classificacao = r["nu_classificacao"]
        nota = r["nu_nota_candidato"]
        modalidade = r["no_mod_concorrencia"]

        csvLine += [codigo_aluno, nome, classificacao, nota, modalidade]

    print("[{}]".format(id_))
    # print("[{}] {} ({}) - {}".format(codigo, iesNome, iesSG, cursoNome))

    # Write to .csv
    csvFileWriter.writerow(tuple(csvLine))

print("Parsed {} responses to '{}/{}.csv' in {:.1f}s with {} errors.".format(len(ids), directory, filename, time()-t0, len(errors)))
if errors:
    print("Errors:")
    for e in errors:
        print("\t{} - Error {}".format(e[0], e[1]))
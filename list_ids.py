import requests
from time import time

baseURL = "https://sisu-api.apps.mec.gov.br/api/v1/oferta/"

filename = "ids_cursos"

t0 = time()
ofertas = []

response = requests.get(baseURL+"instituicoes").json()
instituicoes = [r["co_ies"] for r in response]
for instituicao in instituicoes:
    response = requests.get(baseURL+"instituicao/"+instituicao).json()
    ofertas += [response[str(i)]["co_oferta"] for i in range(len(response)-1)]

with open(filename + ".txt", "w+", encoding="UTF-8") as f:
    f.write("\n".join(ofertas))

print("written {} valid IDs to '{}.txt' in {:.1f}s.".format(len(ofertas), filename, time()-t0))
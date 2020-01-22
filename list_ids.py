import requests

baseURL = "https://sisu-api.apps.mec.gov.br/api/v1/oferta/{}/modalidades"

# <100k     - probably doesn't exist
# 100k-141k - checked and listed
# >141k     - probably doesn't exist

a, b = 100000, 141000

f = open("ids_cursos.txt", "w+", encoding="UTF-8")
for i in range(a, b):
    if i % 100 == 0: print("Testing {}-{}...".format(i, i+99))
    response = requests.get(baseURL.format(i))
    if response.status_code != 204:
        f.write(str(i) + "\n")
        print(i)
    i += 1
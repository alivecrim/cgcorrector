import json

import devices.ssi as ssi
from utils import writers

writers.clear_output()
with open("servicedata/data/config_routes.json", "r") as read_file:
    data = json.load(read_file)

SSIList = []
for idx, ssiDef in enumerate(data):
    ssiItem = ssi.SSI(ssiDef, idx + 1)
    SSIList.append(ssiItem)

isUnicode = False
type_CGs = ['dev', 'sw', 'conf', 'all', 'meas']
for s in SSIList:
    for type_CG in type_CGs:
        writers.writeCG(s, type_CG, isUnicode)
    writers.writePlan(s.getPlan())

for i in range(1, 6):
    writers.writePlan({'filename': f'763_ВХСЕК', 'planstr': f'Входная секция {i} = @763_ВХСЕК{i}.pla'})

# # Генератор ключей
# startKeyGenerator = False
# if startKeyGenerator:

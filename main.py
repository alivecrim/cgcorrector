import json

import devices.ssi as ssi
from utils import writers

writers.clear_output()
with open("servicedata/data/config_routes.json", "r") as read_file:
    data = json.load(read_file)

SSIList = []
counter = 0
for ssiDef in data:
    ssiItem = ssi.SSI(ssiDef)
    SSIList.append(ssiItem)
    counter += 1

isUnicode = False
type_CGs = ['dev', 'dev_off', 'sw', 'conf', 'all', 'meas']
counter = 0
for s in SSIList:
    for type_CG in type_CGs:
        writers.writeCG(s, type_CG, isUnicode)
    writers.writePlan(s.getPlan())
    counter += 1

for i in range(1, 6):
    writers.writePlan({'filename': f'763_ВХСЕК', 'planstr': f'Входная секция {i} = @763_ВХСЕК{i}.pla'})

import json
import devices.ssi as ssi
from utils import writers

with open("servicedata/data/config_routes.json", "r") as read_file:
    data = json.load(read_file)
SSIList = []

for idx, ssiDef in enumerate(data):
    ssiItem = ssi.SSI(ssiDef, idx + 1)
    SSIList.append(ssiItem)

for s in SSIList:
    writers.writeCG(s, 'dev', False)
    writers.writeCG(s, 'sw', False)
    writers.writeCG(s, 'conf', False)
    writers.writeCG(s, 'all', False)
    writers.writeCG(s, 'meas', False)
    writers.writePlan(s._getPlan())

for s in SSIList:
    pass

for i in range(1, 6):
    writers.writePlan({'filename': f'763_ВХСЕК', 'planstr': f'Входная секция {i} = @763_ВХСЕК{i}.pla'})


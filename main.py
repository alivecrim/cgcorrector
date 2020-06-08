import json

import devices.ssi as ssi
from utils import writers

stage_map = {
    "INPUT_SECTION": {
        "file_name_json": "servicedata/data/config_routes.json",
        "cg_prefix": "ВХСЕК",
        "main_cg_name": "ВХСЕК",
        "name_proc": "Входная секция"
    },
    "RSRE": {
        "main_cg_name": "RSRE",
        "file_name_json": "servicedata/data/RSRE/config_routes.json",
        "cg_prefix": "RSRE",
        "name_proc": "RSRE"
    },
    "ETE": {}
}

stage = "RSRE"

file_name = stage_map[stage]["file_name_json"]
cg_prefix = stage_map[stage]["cg_prefix"]
name_proc = stage_map[stage]["name_proc"]
writers.clear_output()
with open(file_name, "r") as read_file:
    data = json.load(read_file)

SSIList = []
counter = 1
for ssiDef in data:
    ssiItem = ssi.SSI(ssiDef, stage_map[stage]["main_cg_name"])
    SSIList.append(ssiItem)
    counter += 1

isUnicode = False
type_CGs = ['dev', 'dev_off', 'sw', 'conf', 'all', 'meas', 'rf_on_off']
counter = 0
for s in SSIList:
    for type_CG in type_CGs:
        writers.writeCG(s, type_CG, isUnicode)
    writers.writePlan(s.getPlan())
    counter += 1

# for i in range(1, 6):
#     writers.writePlan({'filename': f'763_{cg_prefix}', 'planstr': f'{name_proc} {i} = @763_{cg_prefix}{i}.pla'})

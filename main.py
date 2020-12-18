import json
import sys
from enum import Enum

import devices.ssi as ssi
from utils import writers
from utils.merger import Merger


def process_stage(selector):
    if selector == '-stage':
        return_map = {
            "1": Stage.INPUT_SECTION.value,
            "2": Stage.RSRE.value,
            "3": Stage.ETE.value,
            "4": Stage.INTEGRATION.value,
        }
        if selector in sys.argv:
            selector_value = sys.argv[sys.argv.index(selector) + 1]
            return return_map[selector_value]
        return return_map["4"]

    if selector == '-debug':
        return_map = {
            "0": False,
            "1": True,
        }
        if selector in sys.argv:
            selector_value = sys.argv[sys.argv.index(selector) + 1]
            return return_map[selector_value]
        return return_map["1"]


class Stage(Enum):
    INPUT_SECTION = "INPUT_SECTION"
    RSRE = "RSRE"
    ETE = "ETE"
    INTEGRATION = "INTEGRATION"


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
    "ETE": {
        "main_cg_name": "ETE_",
        "file_name_json": "servicedata/data/ETE/config_routes.json",
        "cg_prefix": "ETE",
        "name_proc": "ETE"
    },
    "INTEGRATION": {
        "main_cg_name": "INT_",
        "file_name_json": "servicedata/data/INTEGRATION/config_routes.json",
        "cg_prefix": "INT",
        "name_proc": "INT"
    },
    "H100": {
        "main_cg_name": "H100_",
        "file_name_json": "servicedata/data/H100/low_level.json",
        "cg_prefix": "H100",
        "name_proc": "H100"
    },
    "TVAC_C": {
        "main_cg_name": "TVAC_C_",
        "file_name_json": "servicedata/ПМ3.5/ЭТВИ_С-диапазон/config_tvac_C.json",
        "cg_prefix": "TVAC_C_",
        "name_proc": "TVAC_C_"
    },
    "TVAC_OUTGAS": {
        "main_cg_name": "TVAC_OUTGAS_",
        "file_name_json": "servicedata/ПМ3.5/ЭТВИ_дегазация/config_routes_tvac_degassing.json",
        "cg_prefix": "TVAC_OUTGAS_",
        "name_proc": "TVAC_OUTGAS_"
    }
}

stage = process_stage('-stage')
isDebug = process_stage('-debug')

file_name = stage_map[stage]["file_name_json"]
cg_prefix = stage_map[stage]["cg_prefix"]
name_proc = stage_map[stage]["name_proc"]
writers.clear_output()
with open(file_name, "r") as read_file:
    data = json.load(read_file)

SSIList = []

with open('servicedata/data/INTEGRATION/ete_complex_mes_.json', "r") as read_file:
    integration_data = json.load(read_file)

if not (stage == 'INTEGRATION'):
    for ssiDef in data:
        ssiItem = ssi.SSI(ssiDef, stage_map[stage]["main_cg_name"])
        SSIList.append(ssiItem)
else:
    for ssiDef in integration_data:
        with open(file_name, "r") as read_file:
            data = json.load(read_file)
        merger = Merger(ssi_bsk1=data, ssi_integration=ssiDef)
        ssiItem = ssi.SSI(merger.merge(), stage_map[stage]["main_cg_name"])
        SSIList.append(ssiItem)

isUnicode = isDebug

type_CGs = ['dev', 'dev_off', 'sw', 'conf', 'all', 'meas', 'rf_on_off']
counter = 0
for s in SSIList:
    for type_CG in type_CGs:
        writers.writeCG(s, type_CG, isUnicode)
    writers.writePlan(s.getPlan())
    counter += 1

for i in range(1, 6):
    writers.writePlan({'filename': f'763_{cg_prefix}', 'planstr': f'{name_proc} {i} = @763_{cg_prefix}{i}.pla'})

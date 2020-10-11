import json
import sys
from enum import Enum

import devices.ssi as ssi
from utils import writers


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
counter = 1
in_batch: {}
out_batch: {}


def batch_combine(in_batch, out_batch):
    merged = {"id": int(in_batch.pop("id")[:3])}
    for item in in_batch:
        if item in ["frequency_start",
                    "power_in",
                    "cnv_cif",
                    "cnv_ska",
                    "cnv_ifs",
                    "bw"
                    ]:
            merged[item] = in_batch[item]
        elif (item in ["twta_tas",
                       "twta_mda",
                       "frequency_out"]):
            merged[item] = out_batch[item]
        else:
            if type(in_batch[item]) == dict:
                merged[item] = {**in_batch[item], **out_batch[item]}
            else:
                merged[item] = in_batch[item] + out_batch[item]
    return merged


for ssiDef in data:
    if type(ssiDef["id"]) == str:
        if "in" in ssiDef["id"]:
            in_batch = ssiDef
            continue
        else:
            out_batch = ssiDef
            m = batch_combine(in_batch, out_batch)
            ssiItem = ssi.SSI(m, stage_map[stage]["main_cg_name"])
    else:
        ssiItem = ssi.SSI(ssiDef, stage_map[stage]["main_cg_name"])
    SSIList.append(ssiItem)
    counter += 1

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

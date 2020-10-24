import json
from unittest import TestCase

ssi_bsk1 = [
    {"id": "817_in_L",
     "query_route": ["WIC2", "WLNA1-J09", "C062", "W3CN2", "WDTP1-J28", "WDTP1-J29", "W4CN3-J22", "WF15", "C278"],
     "route": [["WIC2", "J1", "J2"], ["WG2", "A", "B"], ["WF2", "J01", "J02"], ["002", "A", "B"], ["WSC2", "J4", "J3"],
               ["006", "A", "B"], ["WLNA1", "J08", "J09"], ["010", "A", "B"], ["WSC4", "J3", "J2"], ["017", "A", "B"],
               ["WISOK2", "1", "2"], ["018", "A", "B"], ["WD2", "J1", "J3"], ["019", "A", "B"], ["WISOK9", "1", "2"],
               ["020", "A", "B"], ["WSC9", "J1", "J2"], ["168", "A", "B"], ["WST9", "J1", "J2"], ["062", "A", "B"],
               ["WST15", "J1", "J2"], ["150", "A", "B"], ["WST39", "J1", "J2"], ["176", "A", "B"],
               ["W3CN2", "J01", "J02"], ["177", "A", "B"], ["WST48", "J1", "J2"], ["211", "A", "B"],
               ["WDTP1", "J28", "J29"], ["223", "A", "B"], ["WST58", "J1", "J2"], ["236", "A", "B"],
               ["WU60", "J1", "J2"], ["W4CN3", "J21", "J22"], ["237", "A", "B"], ["WST63", "J1", "J2"],
               ["249", "A", "B"], ["WF15", "J1", "J2"], ["250", "A", "B"], ["WISOK19", "1", "2"], ["251", "A", "B"],
               ["WD7", "1", "4"], ["254", "A", "B"], ["WISOK24", "1", "2"], ["255", "A", "B"], ["WD11", "1", "3"],
               ["277", "A", "B"], ["WISOK31", "1", "2"], ["278", "A", "B"]],
     "route_long_name": "WIC2-J1-J2 WG2-A-B WF2-J01-J02 002-A-B WSC2-J4-J3 006-A-B WLNA1-J08-J09 010-A-B WSC4-J3-J2 017-A-B WISOK2-1-2 018-A-B WD2-J1-J3 019-A-B WISOK9-1-2 020-A-B WSC9-J1-J2 168-A-B WST9-J1-J2 062-A-B WST15-J1-J2 150-A-B WST39-J1-J2 176-A-B W3CN2-J01-J02 177-A-B WST48-J1-J2 211-A-B WDTP1-J28-J29 223-A-B WST58-J1-J2 236-A-B WU60-J1-J2 W4CN3-J21-J22 237-A-B WST63-J1-J2 249-A-B WF15-J1-J2 250-A-B WISOK19-1-2 251-A-B WD7-1-4 254-A-B WISOK24-1-2 255-A-B WD11-1-3 277-A-B WISOK31-1-2 278-A-B",
     "route_short_name": "WIC2_WLNA1-J09_C062_W3CN2_WDTP1-J28_WDTP1-J29_W4CN3-J22_WF15_C278",
     "config_name": "6095.0_250.0_-67.0L_CIF-5420.0G40.0_SKA0_KKA0_MLO10", "power_in": -67.0, "power_level": "L",
     "frequency_start": 6095.0, "bw": 250.0, "cnv_cif": {"LO": -5420.0, "G": 40.0}, "cnv_ska": {"LO": 0},
     "cnv_kka": {"LO": 0}, "dtp_conf": 1, "mlo": {"N": 1, "R": 0},
     "dtp": {"TC_N": 1, "TC_R": 0, "G_N": 1, "G_R": 0, "B1": 1, "B2": 1, "B3": 0, "B4": 0, "INV": 0, "ALC": 0,
             "G_NUM": -26, "ALC_LEVEL": -26, "LO": -320},
     "twta_tas": {"status": 0, "FCA": 0, "GCA": 0, "SCA": 0, "FGM": 1},
     "twta_mda": {"status": 0, "FCA": 0, "GCA": 0, "SCA": 0, "FGM": 1}, "channel": "Ch6",
     "channel_type": "\u0424\u041b\u0421", "channel_band": "C-band", "frequency_out": 2200.0, "global_lo": 3895.0,
     "cnv_ifs": {"LO": 1845}, "cnv_kuc": {"LO": 0}, "cnv_lc": {"LO": 0},
     "query_route_ports": [["WIC2", "J1"], ["WLNA1", "J09"], ["062", "B"], ["W3CN2", "J02"], ["WDTP1", "J28"],
                           ["WDTP1", "J29"], ["W4CN3", "J22"], ["WF15", "J2"], ["278", "B"]],
     "calc_set_config": {"CNVCIF": {"LO": -5420.0, "G": 40.0}, "CNVSK": {}, "CNVKKA": {},
                         "DTP": {"INV": 0, "G": -26, "LO": -320, "ALC": 0, "ALC_LEVEL": -26}, "frequency_start": 6095.0,
                         "bw": 250.0, "power_in": -67.0}},
    {"id": "817_in_H",
     "query_route": ["WIC2", "WLNA1-J09", "C063", "W3CN2",
                     "WDTP1-J28", "WDTP1-J29", "W4CN3-J22",
                     "WF15", "C278"],
     "route": [["WIC2", "J1", "J2"], ["WG2", "A", "B"],
               ["WF2", "J01", "J02"], ["002", "A", "B"],
               ["WSC2", "J4", "J3"], ["006", "A", "B"],
               ["WLNA1", "J08", "J09"], ["010", "A", "B"],
               ["WSC4", "J3", "J2"], ["017", "A", "B"],
               ["WISOK2", "1", "2"], ["018", "A", "B"],
               ["WD2", "J1", "J3"], ["019", "A", "B"],
               ["WISOK9", "1", "2"], ["020", "A", "B"],
               ["WSC9", "J1", "J2"], ["168", "A", "B"],
               ["WST9", "J1", "J4"], ["WU38", "J2", "J1"],
               ["063", "A", "B"], ["WU51", "J1", "J2"],
               ["WST15", "J4", "J2"], ["150", "A", "B"],
               ["WST39", "J1", "J2"], ["176", "A", "B"],
               ["W3CN2", "J01", "J02"], ["177", "A", "B"],
               ["WST48", "J1", "J2"], ["211", "A", "B"],
               ["WDTP1", "J28", "J29"], ["223", "A", "B"],
               ["WST58", "J1", "J2"], ["236", "A", "B"],
               ["WU60", "J1", "J2"], ["W4CN3", "J21", "J22"],
               ["237", "A", "B"], ["WST63", "J1", "J2"],
               ["249", "A", "B"], ["WF15", "J1", "J2"],
               ["250", "A", "B"], ["WISOK19", "1", "2"],
               ["251", "A", "B"], ["WD7", "1", "4"],
               ["254", "A", "B"], ["WISOK24", "1", "2"],
               ["255", "A", "B"], ["WD11", "1", "3"],
               ["277", "A", "B"], ["WISOK31", "1", "2"],
               ["278", "A", "B"]],
     "route_long_name": "WIC2-J1-J2 WG2-A-B WF2-J01-J02 002-A-B WSC2-J4-J3 006-A-B WLNA1-J08-J09 010-A-B WSC4-J3-J2 017-A-B WISOK2-1-2 018-A-B WD2-J1-J3 019-A-B WISOK9-1-2 020-A-B WSC9-J1-J2 168-A-B WST9-J1-J4 WU38-J2-J1 063-A-B WU51-J1-J2 WST15-J4-J2 150-A-B WST39-J1-J2 176-A-B W3CN2-J01-J02 177-A-B WST48-J1-J2 211-A-B WDTP1-J28-J29 223-A-B WST58-J1-J2 236-A-B WU60-J1-J2 W4CN3-J21-J22 237-A-B WST63-J1-J2 249-A-B WF15-J1-J2 250-A-B WISOK19-1-2 251-A-B WD7-1-4 254-A-B WISOK24-1-2 255-A-B WD11-1-3 277-A-B WISOK31-1-2 278-A-B",
     "route_short_name": "WIC2_WLNA1-J09_C063_W3CN2_WDTP1-J28_WDTP1-J29_W4CN3-J22_WF15_C278",
     "config_name": "6095.0_250.0_-45.0H_CIF-5420.0G30.0_SKA0_KKA0_MLO10",
     "power_in": -45.0, "power_level": "H",
     "frequency_start": 6095.0, "bw": 250.0,
     "cnv_cif": {"LO": -5420.0, "G": 30.0}, "cnv_ska": {"LO": 0},
     "cnv_kka": {"LO": 0}, "dtp_conf": 1,
     "mlo": {"N": 1, "R": 0},
     "dtp": {"TC_N": 1, "TC_R": 0, "G_N": 1, "G_R": 0, "B1": 1,
             "B2": 1, "B3": 0, "B4": 0, "INV": 0, "ALC": 0,
             "G_NUM": -26, "ALC_LEVEL": -26, "LO": -320},
     "twta_tas": {"status": 0, "FCA": 0, "GCA": 0, "SCA": 0,
                  "FGM": 1},
     "twta_mda": {"status": 0, "FCA": 0, "GCA": 0, "SCA": 0,
                  "FGM": 1}, "channel": "Ch6",
     "channel_type": "\u0424\u041b\u0421",
     "channel_band": "C-band", "frequency_out": 2200.0,
     "global_lo": 3895.0, "cnv_ifs": {"LO": 1845},
     "cnv_kuc": {"LO": 0}, "cnv_lc": {"LO": 0},
     "query_route_ports": [["WIC2", "J1"], ["WLNA1", "J09"],
                           ["063", "B"], ["W3CN2", "J02"],
                           ["WDTP1", "J28"], ["WDTP1", "J29"],
                           ["W4CN3", "J22"], ["WF15", "J2"],
                           ["278", "B"]],
     "calc_set_config": {"CNVCIF": {"LO": -5420.0, "G": 30.0},
                         "CNVSK": {}, "CNVKKA": {},
                         "DTP": {"INV": 0, "G": -26, "LO": -320,
                                 "ALC": 0, "ALC_LEVEL": -26},
                         "frequency_start": 6095.0, "bw": 250.0,
                         "power_in": -45.0}},
    {"id": "817_out", "query_route": ["C333", "WIM2-O2", "WTW3B", "WOM2-J06", "WOC1"],
     "route": [["333", "A", "B"], ["WU77", "J1", "J2"], ["WSC19", "J4", "J1"], ["331", "A", "B"], ["WSC18", "J2", "J3"],
               ["330", "A", "B"], ["WIM2", "I2", "O2"], ["343", "A", "B"], ["WSC21", "J1", "J2"], ["342", "A", "B"],
               ["WU85", "J1", "J2"], ["WST79", "J1", "J2"], ["352", "A", "B"], ["WU92", "J1", "J2"],
               ["WCPA3", "J01B", "J02B"], ["3BT", "A", "B"], ["WU3B", "J1", "J2"], ["WTW3B", "Input", "Output"],
               ["WG22.1", "A", "B"], ["WG22.2", "A", "B"], ["WG22.3", "A", "B"], ["WISO6", "J01", "J02"],
               ["WG23", "A", "B"], ["WSR6", "J4", "J2"], ["WG24.1", "A", "B"], ["WG24.2", "A", "B"],
               ["WG24.3", "A", "B"], ["WG24.4", "A", "B"], ["WOM2", "J06", "J08"], ["WG37.1", "A", "B"],
               ["WG37.2", "A", "B"], ["WG37.3", "A", "B"], ["WG37.4", "A", "B"], ["WOC1", "1", "2"]],
     "route_long_name": "333-A-B WU77-J1-J2 WSC19-J4-J1 331-A-B WSC18-J2-J3 330-A-B WIM2-I2-O2 343-A-B WSC21-J1-J2 342-A-B WU85-J1-J2 WST79-J1-J2 352-A-B WU92-J1-J2 WCPA3-J01B-J02B 3BT-A-B WU3B-J1-J2 WTW3B-Input-Output WG22.1-A-B WG22.2-A-B WG22.3-A-B WISO6-J01-J02 WG23-A-B WSR6-J4-J2 WG24.1-A-B WG24.2-A-B WG24.3-A-B WG24.4-A-B WOM2-J06-J08 WG37.1-A-B WG37.2-A-B WG37.3-A-B WG37.4-A-B WOC1-1-2",
     "route_short_name": "C333_WIM2-O2_WTW3B_WOM2-J06_WOC1",
     "config_name": "20668.0_234.0_-10.0L_CIF-0.0G40.0_SKA0_KKA0_MLO10", "power_in": -10.0, "power_level": "L",
     "frequency_start": 20668.0, "bw": 234.0, "cnv_cif": {"LO": -0.0, "G": 40.0}, "cnv_ska": {"LO": 0},
     "cnv_kka": {"LO": 0}, "dtp_conf": 1, "mlo": {"N": 1, "R": 0},
     "dtp": {"TC_N": 1, "TC_R": 0, "G_N": 1, "G_R": 0, "B1": 1, "B2": 1, "B3": 0, "B4": 0, "INV": 0, "ALC": 0,
             "G_NUM": -26, "ALC_LEVEL": -26, "LO": -320},
     "twta_tas": {"status": 1, "FCA": 33, "GCA": 35, "SCA": 41, "FGM": 1},
     "twta_mda": {"status": 0, "FCA": 0, "GCA": 0, "SCA": 0, "FGM": 1}, "channel": "Ch5",
     "channel_type": "\u0424\u041b\u0421", "channel_band": "K-band", "frequency_out": 20668.0, "global_lo": 0.0,
     "cnv_ifs": {"LO": 0}, "cnv_kuc": {"LO": 0}, "cnv_lc": {"LO": 0},
     "query_route_ports": [["333", "A"], ["WIM2", "O2"], ["WTW3B", "Output"], ["WOM2", "J06"], ["WOC1", "2"]],
     "calc_set_config": {"CNVCIF": {"LO": -0.0, "G": 40.0}, "CNVSK": {}, "CNVKKA": {},
                         "DTP": {"INV": 0, "G": -26, "LO": -320, "ALC": 0, "ALC_LEVEL": -26},
                         "frequency_start": 20668.0, "bw": 234.0, "power_in": -10.0}}
]
ssi_integration = [
    {
        "id": 1000,
        "level": "L",
        "band_letter": "Ka",
        "in": "AR14",
        "out": "WOC1",
        "id_bsk1": "801",
        "id_bsk2": "2.1",
        "id_bsk3": "1.3 \u0438 2.1",
        "Fc_in": 28000,
        "Fc_out": 20785,
        "BW": 250,
        "dF": 0,
        "Pin": -77.5,
        "ch_out": "Ch5",
        "SP": 1,
        "GF": 0,
        "GD": 0,
        "IM3": 0,
        "PN": 0,
        "PN_DS": 0,
        "MOD": 1,
        "SPECTRUM": 1
    },
    {
        "id": 1040,
        "level": "L",
        "band_letter": "C",
        "in": "WIC2",
        "out": "WOC1",
        "id_bsk1": 817,
        "id_bsk2": 0,
        "id_bsk3": "3.1",
        "Fc_in": 6220,
        "Fc_out": 20785,
        "BW": 250,
        "dF": 0,
        "Pin": -67,
        "ch_out": "Ch5",
        "SP": 0,
        "GF": 0,
        "GD": 0,
        "IM3": 0,
        "PN": 0,
        "PN_DS": 0,
        "MOD": 1,
        "SPECTRUM": 1
    },
    {
        "id": 1041,
        "level": "H",
        "band_letter": "C",
        "in": "WIC2",
        "out": "WOC1",
        "id_bsk1": 817,
        "id_bsk2": 0,
        "id_bsk3": "3.1",
        "Fc_in": 6220,
        "Fc_out": 20785,
        "BW": 250,
        "dF": 0,
        "Pin": -45,
        "ch_out": "Ch5",
        "SP": 0,
        "GF": 0,
        "GD": 0,
        "IM3": 0,
        "PN": 0,
        "PN_DS": 0,
        "MOD": 1,
        "SPECTRUM": 1
    },
]


class Merger(object):
    def __init__(self, ssi_integration, ssi_bsk1) -> None:
        self.ssi_integration_item = ssi_integration
        self.ssi_bsk = ssi_bsk1
        self.config_id = self.ssi_integration_item["id"]
        self.lvl = self.ssi_integration_item["level"]
        self.bsk1_id = self.ssi_integration_item["id_bsk1"]
        self.power_in = self.ssi_integration_item["Pin"]
        self.bw = self.ssi_integration_item["BW"]
        self.bsk2_id = self.ssi_integration_item["id_bsk2"]
        self.bsk3_id = self.ssi_integration_item["id_bsk3"]

    def merge(self) -> dict:
        bsk1_in = None
        bsk1_out = None
        bsk_full_level = None
        finded_out = False
        finded_in = False
        finded_full_level = False
        finded_full = False

        finded_string = str(self.bsk1_id) + "_in_" + self.lvl
        for ssi in self.ssi_bsk:
            if ssi["id"] == finded_string:
                bsk1_in = ssi
                finded_in = True
                break

        finded_string = str(self.bsk1_id) + "_out"
        for ssi in ssi_bsk1:
            if ssi["id"] == finded_string:
                bsk1_out = ssi
                finded_out = True
                break

        finded_string = str(self.bsk1_id) + '_' + self.lvl
        for ssi in self.ssi_bsk:
            if ssi['id'] == finded_string:
                bsk_full = ssi
                finded_full_level = True
                break

        for ssi in self.ssi_bsk:
            if ssi['id'] == self.bsk1_id:
                bsk_full = ssi
                finded_full = True
                break
        if finded_in and finded_out:
            merged_ssi = self.merge_ssi_in_and_out(bsk1_in, bsk1_out)
        elif finded_full_level or finded_full:
            merged_ssi = self.merge_ssi_full(bsk_full_level)
        else:
            raise Exception()
        return merged_ssi

    def merge_ssi_in_and_out(self, bsk1_in, bsk1_out):
        z = {'id': self.config_id,
             'query_route': bsk1_in['query_route'] + bsk1_out['query_route'],
             'route': bsk1_in['route'] + bsk1_out['route'],
             'route_long_name': bsk1_in['route_long_name'] + ' ' + bsk1_out['route_long_name'],
             'route_short_name': bsk1_in['route_short_name'] + '_' + bsk1_out['route_short_name'],
             'frequency_start': self.ssi_integration_item['Fc_in'] - self.bw / 2,
             'power_level': self.lvl,
             'config_name': bsk1_in['config_name'],
             'power_in': self.power_in,
             'cnv_cif': bsk1_in['cnv_cif'],
             'cnv_ska': bsk1_in['cnv_ska'],
             }
        return z

    def merge_ssi_full(self, bsk_full):
        z = bsk_full
        z["id"] = self.config_id
        z["route_short_name"] = z["route_short_name"] + ' BSK2: ' + self.bsk2_id + ' BSK3: ' + self.bsk3_id
        return z


class TestMerge(TestCase):
    def test_merge_simple(self):
        merger = Merger(ssi_integration[0], ssi_bsk1)

        print(json.dumps(merger.merge(), indent=4))

# class Test(TestCase):
#     def test_input_data(self):
#         self.assertEqual(len(ssi_bsk1), 2)
#         self.assertEqual(len(ssi_integration), 2)
#
#     def test_merge_ssi(self):
#         in_ssi_bsk1 = ssi_bsk1[0]
#         out_ssi_bsk1 = ssi_bsk1[1]
#         test_ssi = ssi_integration[0]
#         merger = Merger(in_ssi_bsk1, out_ssi_bsk1, test_ssi)
#         merged_ssi = merger.merge()
#         self.assertEqual(merged_ssi["id"], 33, "ssi id should be 33")
#         self.assertEqual(merged_ssi["integration"], True)
#         self.assertEqual(merged_ssi["freq_in"], test_ssi["Fc_in"])
#         self.assertEqual(merged_ssi["freq_out"], test_ssi["Fc_out"])
#         self.assertEqual(merged_ssi["rout"], test_ssi["Fc_out"])

#  'cnv_cif': {'LO': -5420.0, 'G': 40.0}, 'cnv_ska': {'LO': 0}, 'cnv_kka': {'LO': 0}, 'dtp_conf': 1, 'mlo': {'N': 1, 'R': 0}, 'dtp': {'TC_N': 1, 'TC_R': 0, 'G_N': 1, 'G_R': 0, 'B1': 1, 'B2': 1, 'B3': 0, 'B4': 0, 'INV': 0, 'ALC': 0, 'G_NUM': -26, 'ALC_LEVEL': -26, 'LO': -320}, 'twta_tas': {'status': 0, 'FCA': 0, 'GCA': 0, 'SCA': 0, 'FGM': 1},    'twta_mda': {'status': 0, 'FCA': 0, 'GCA': 0, 'SCA': 0, 'FGM': 1}, 'channel': 'Ch6', 'channel_type': 'ФЛС', 'channel_band': 'C-band', 'frequency_out': 2200.0, 'global_lo': 3895.0, 'cnv_ifs': {'LO': 1845}, 'cnv_kuc': {'LO': 0}, 'cnv_lc': {'LO': 0}, 'query_route_ports': [['WIC2', 'J1'], ['WLNA1', 'J09'], ['062', 'B'], ['W3CN2', 'J02'], ['WDTP1', 'J28'], ['WDTP1', 'J29'], ['W4CN3', 'J22'], ['WF15', 'J2'], ['278', 'B']], 'calc_set_config': {'CNVCIF': {'LO': -5420.0, 'G': 40.0}, 'CNVSK': {}, 'CNVKKA': {}, 'DTP': {'INV': 0, 'G': -26, 'LO': -320, 'ALC': 0, 'ALC_LEVEL': -26}, 'frequency_start': 6095.0, 'bw': 250.0, 'power_in': -67.0}}
#  'cnv_cif': {'LO': -0.0, 'G': 40.0},    'cnv_ska': {'LO': 0}, 'cnv_kka': {'LO': 0}, 'dtp_conf': 1, 'mlo': {'N': 1, 'R': 0}, 'dtp': {'TC_N': 1, 'TC_R': 0, 'G_N': 1, 'G_R': 0, 'B1': 1, 'B2': 1, 'B3': 0, 'B4': 0, 'INV': 0, 'ALC': 0, 'G_NUM': -26, 'ALC_LEVEL': -26, 'LO': -320}, 'twta_tas': {'status': 1, 'FCA': 33, 'GCA': 35, 'SCA': 41, 'FGM': 1}, 'twta_mda': {'status': 0, 'FCA': 0, 'GCA': 0, 'SCA': 0, 'FGM': 1}, 'channel': 'Ch5', 'channel_type': 'ФЛС', 'channel_band': 'K-band', 'frequency_out': 20668.0, 'global_lo': 0.0,   'cnv_ifs': {'LO': 0},    'cnv_kuc': {'LO': 0}, 'cnv_lc': {'LO': 0}, 'query_route_ports': [['333', 'A'], ['WIM2', 'O2'], ['WTW3B', 'Output'], ['WOM2', 'J06'], ['WOC1', '2']],                                                                    'calc_set_config': {'CNVCIF': {'LO': -0.0, 'G': 40.0},    'CNVSK': {}, 'CNVKKA': {}, 'DTP': {'INV': 0, 'G': -26, 'LO': -320, 'ALC': 0, 'ALC_LEVEL': -26}, 'frequency_start': 20668.0,'bw': 234.0, 'power_in': -10.0}}

import json
from unittest import TestCase

from utils.merger import Merger


class TestMerge(TestCase):
    ssi_bsk1 = [
        {
            "id": 801,
            "query_route": [
                "C333",
                "WIM2-O2",
                "WTW3B",
                "WOM2-J06",
                "WOC1"
            ],
            "route": [
                [
                    "333",
                    "A",
                    "B"
                ],
                [
                    "WU77",
                    "J1",
                    "J2"
                ],
                [
                    "WSC19",
                    "J4",
                    "J1"
                ],
                [
                    "331",
                    "A",
                    "B"
                ],
                [
                    "WSC18",
                    "J2",
                    "J3"
                ],
                [
                    "330",
                    "A",
                    "B"
                ],
                [
                    "WIM2",
                    "I2",
                    "O2"
                ],
                [
                    "343",
                    "A",
                    "B"
                ],
                [
                    "WSC21",
                    "J1",
                    "J2"
                ],
                [
                    "342",
                    "A",
                    "B"
                ],
                [
                    "WU85",
                    "J1",
                    "J2"
                ],
                [
                    "WST79",
                    "J1",
                    "J2"
                ],
                [
                    "352",
                    "A",
                    "B"
                ],
                [
                    "WU92",
                    "J1",
                    "J2"
                ],
                [
                    "WCPA3",
                    "J01B",
                    "J02B"
                ],
                [
                    "3BT",
                    "A",
                    "B"
                ],
                [
                    "WU3B",
                    "J1",
                    "J2"
                ],
                [
                    "WTW3B",
                    "Input",
                    "Output"
                ],
                [
                    "WG22.1",
                    "A",
                    "B"
                ],
                [
                    "WG22.2",
                    "A",
                    "B"
                ],
                [
                    "WG22.3",
                    "A",
                    "B"
                ],
                [
                    "WISO6",
                    "J01",
                    "J02"
                ],
                [
                    "WG23",
                    "A",
                    "B"
                ],
                [
                    "WSR6",
                    "J4",
                    "J2"
                ],
                [
                    "WG24.1",
                    "A",
                    "B"
                ],
                [
                    "WG24.2",
                    "A",
                    "B"
                ],
                [
                    "WG24.3",
                    "A",
                    "B"
                ],
                [
                    "WG24.4",
                    "A",
                    "B"
                ],
                [
                    "WOM2",
                    "J06",
                    "J08"
                ],
                [
                    "WG37.1",
                    "A",
                    "B"
                ],
                [
                    "WG37.2",
                    "A",
                    "B"
                ],
                [
                    "WG37.3",
                    "A",
                    "B"
                ],
                [
                    "WG37.4",
                    "A",
                    "B"
                ],
                [
                    "WOC1",
                    "1",
                    "2"
                ]
            ],
            "route_long_name": "333-A-B WU77-J1-J2 WSC19-J4-J1 331-A-B WSC18-J2-J3 330-A-B WIM2-I2-O2 343-A-B WSC21-J1-J2 342-A-B WU85-J1-J2 WST79-J1-J2 352-A-B WU92-J1-J2 WCPA3-J01B-J02B 3BT-A-B WU3B-J1-J2 WTW3B-Input-Output WG22.1-A-B WG22.2-A-B WG22.3-A-B WISO6-J01-J02 WG23-A-B WSR6-J4-J2 WG24.1-A-B WG24.2-A-B WG24.3-A-B WG24.4-A-B WOM2-J06-J08 WG37.1-A-B WG37.2-A-B WG37.3-A-B WG37.4-A-B WOC1-1-2",
            "route_short_name": "C333_WIM2-O2_WTW3B_WOM2-J06_WOC1",
            "config_name": "20668.0_234.0_-10.0L_CIF-0.0G40.0_SKA0_KKA0_MLO10",
            "power_in": -10.0,
            "power_level": "L",
            "frequency_start": 20668.0,
            "bw": 234.0,
            "cnv_cif": {
                "LO": -0.0,
                "G": 40.0
            },
            "cnv_ska": {
                "LO": 0
            },
            "cnv_kka": {
                "LO": 0
            },
            "dtp_conf": 1,
            "mlo": {
                "N": 1,
                "R": 0
            },
            "dtp": {
                "TC_N": 1,
                "TC_R": 0,
                "G_N": 1,
                "G_R": 0,
                "B1": 1,
                "B2": 1,
                "B3": 0,
                "B4": 0,
                "INV": 0,
                "ALC": 0,
                "G_NUM": -26,
                "ALC_LEVEL": -26,
                "LO": -320
            },
            "twta_tas": {
                "status": 1,
                "FCA": 33,
                "GCA": 35,
                "SCA": 41,
                "FGM": 1
            },
            "twta_mda": {
                "status": 0,
                "FCA": 0,
                "GCA": 0,
                "SCA": 0,
                "FGM": 1
            },
            "channel": "Ch5",
            "channel_type": "\u0424\u041b\u0421",
            "channel_band": "K-band",
            "frequency_out": 20668.0,
            "global_lo": 0.0,
            "cnv_ifs": {
                "LO": 0
            },
            "cnv_kuc": {
                "LO": 0
            },
            "cnv_lc": {
                "LO": 0
            },
            "query_route_ports": [
                [
                    "333",
                    "A"
                ],
                [
                    "WIM2",
                    "O2"
                ],
                [
                    "WTW3B",
                    "Output"
                ],
                [
                    "WOM2",
                    "J06"
                ],
                [
                    "WOC1",
                    "2"
                ]
            ],
            "calc_set_config": {
                "CNVCIF": {
                    "LO": -0.0,
                    "G": 40.0
                },
                "CNVSK": {},
                "CNVKKA": {},
                "DTP": {
                    "INV": 0,
                    "G": -26,
                    "LO": -320,
                    "ALC": 0,
                    "ALC_LEVEL": -26
                },
                "frequency_start": 20668.0,
                "bw": 234.0,
                "power_in": -10.0
            }
        },
        {"id": "817_in_L",
         "query_route": ["WIC2", "WLNA1-J09", "C062", "W3CN2", "WDTP1-J28", "WDTP1-J29", "W4CN3-J22", "WF15", "C278"],
         "route": [["WIC2", "J1", "J2"], ["WG2", "A", "B"], ["WF2", "J01", "J02"], ["002", "A", "B"],
                   ["WSC2", "J4", "J3"],
                   ["006", "A", "B"], ["WLNA1", "J08", "J09"], ["010", "A", "B"], ["WSC4", "J3", "J2"],
                   ["017", "A", "B"],
                   ["WISOK2", "1", "2"], ["018", "A", "B"], ["WD2", "J1", "J3"], ["019", "A", "B"],
                   ["WISOK9", "1", "2"],
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
                             "DTP": {"INV": 0, "G": -26, "LO": -320, "ALC": 0, "ALC_LEVEL": -26},
                             "frequency_start": 6095.0,
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
         "route": [["333", "A", "B"], ["WU77", "J1", "J2"], ["WSC19", "J4", "J1"], ["331", "A", "B"],
                   ["WSC18", "J2", "J3"],
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

    def test_merge_simple_id0(self):
        merger = Merger(self.ssi_integration[0], self.ssi_bsk1)
        merger_config = merger.merge()
        # print(json.dumps(merger_config, indent=4))
        self.assertEqual(250, merger_config['bw'][0])

    def test_merge_simple_id1(self):
        merger = Merger(self.ssi_integration[1], self.ssi_bsk1)
        print(json.dumps(merger.merge(), sort_keys=True, indent=2))

    def test_merge_simple_id2(self):
        merger = Merger(self.ssi_integration[2], self.ssi_bsk1)
        print(json.dumps(merger.merge(), indent=4))

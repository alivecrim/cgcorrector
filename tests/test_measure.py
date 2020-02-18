from unittest import TestCase
import unittest

from measure.measure import Measure

config2 = {
    "id": 198,
    "route_comb_alias": "179-235_C1-K2",
    "route_in_alias": "179-C1-D",
    "route_in": [
        "WIC3",
        "WLNA2-J06",
        "C077",
        "W3CN9",
        "WDTP1-J98"
    ],
    "route_in_band_letters": [
        "C1",
        "D"
    ],
    "route_in_bands": [
        5725.0,
        6725.0,
        0.0,
        1.0
    ],
    "route_out_alias": "235-D-K2",
    "route_out": [
        "WDTP1-J49",
        "W4CN2-J22",
        "W5CN4",
        "WIM1-O2",
        "C348"
    ],
    "route_out_band_letters": [
        "D",
        "K2"
    ],
    "route_out_bands": [
        0.0,
        1.0,
        20310.0,
        20390.0
    ],
    "query_route": [
        "WIC3",
        "WLNA2-J06",
        "C077",
        "W3CN9",
        "WDTP1-J98",
        "WDTP1-J49",
        "W4CN2-J22",
        "W5CN4",
        "WIM1-O2",
        "C348"
    ],
    "route": [
        [
            "WIC3",
            "J1",
            "J2"
        ],
        [
            "WG3",
            "A",
            "B"
        ],
        [
            "WF3",
            "J01",
            "J02"
        ],
        [
            "023",
            "A",
            "B"
        ],
        [
            "WST1",
            "J1",
            "J2"
        ],
        [
            "026",
            "A",
            "B"
        ],
        [
            "WLNA2",
            "J05",
            "J06"
        ],
        [
            "029",
            "A",
            "B"
        ],
        [
            "WST5",
            "J1",
            "J2"
        ],
        [
            "031",
            "A",
            "B"
        ],
        [
            "WISOK3",
            "1",
            "2"
        ],
        [
            "032",
            "A",
            "B"
        ],
        [
            "WD3",
            "J1",
            "J3"
        ],
        [
            "033",
            "A",
            "B"
        ],
        [
            "WISOK11",
            "1",
            "2"
        ],
        [
            "164",
            "A",
            "B"
        ],
        [
            "WSC14",
            "J3",
            "J2"
        ],
        [
            "173",
            "A",
            "B"
        ],
        [
            "WST14",
            "J1",
            "J2"
        ],
        [
            "077",
            "A",
            "B"
        ],
        [
            "WST20",
            "J1",
            "J2"
        ],
        [
            "397",
            "A",
            "B"
        ],
        [
            "WST46",
            "J1",
            "J2"
        ],
        [
            "190",
            "A",
            "B"
        ],
        [
            "W3CN9",
            "J01",
            "J02"
        ],
        [
            "191",
            "A",
            "B"
        ],
        [
            "WST55",
            "J1",
            "J2"
        ],
        [
            "218",
            "A",
            "B"
        ],
        [
            "WDTP1",
            "J98",
            "J49"
        ],
        [
            "225",
            "A",
            "B"
        ],
        [
            "WST60",
            "J1",
            "J2"
        ],
        [
            "240",
            "A",
            "B"
        ],
        [
            "WU62",
            "J1",
            "J2"
        ],
        [
            "W4CN2",
            "J21",
            "J22"
        ],
        [
            "241",
            "A",
            "B"
        ],
        [
            "WST65",
            "J1",
            "J2"
        ],
        [
            "263",
            "A",
            "B"
        ],
        [
            "WF17",
            "J1",
            "J2"
        ],
        [
            "264",
            "A",
            "B"
        ],
        [
            "WISOK21",
            "1",
            "2"
        ],
        [
            "265",
            "A",
            "B"
        ],
        [
            "WD9",
            "1",
            "3"
        ],
        [
            "266",
            "A",
            "B"
        ],
        [
            "WISOK27",
            "1",
            "2"
        ],
        [
            "267",
            "A",
            "B"
        ],
        [
            "WU68",
            "J1",
            "J2"
        ],
        [
            "WST69",
            "J1",
            "J2"
        ],
        [
            "296",
            "A",
            "B"
        ],
        [
            "W5CN4",
            "J01",
            "J02"
        ],
        [
            "302",
            "A",
            "B"
        ],
        [
            "WST73",
            "J1",
            "J2"
        ],
        [
            "WU73.1",
            "J2",
            "J1"
        ],
        [
            "326",
            "A",
            "B"
        ],
        [
            "WU73.2",
            "J1",
            "J2"
        ],
        [
            "WSC17",
            "J4",
            "J1"
        ],
        [
            "325",
            "B",
            "A"
        ],
        [
            "WSC15",
            "J2",
            "J1"
        ],
        [
            "317",
            "A",
            "B"
        ],
        [
            "WIM1",
            "I2",
            "O2"
        ],
        [
            "WU81",
            "J2",
            "J1"
        ],
        [
            "337",
            "A",
            "B"
        ],
        [
            "WST75",
            "J1",
            "J2"
        ],
        [
            "348",
            "A",
            "B"
        ]
    ],
    "route_long_name": "WIC3-J1-J2 WG3-A-B WF3-J01-J02 023-A-B WST1-J1-J2 026-A-B WLNA2-J05-J06 029-A-B WST5-J1-J2 031-A-B WISOK3-1-2 032-A-B WD3-J1-J3 033-A-B WISOK11-1-2 164-A-B WSC14-J3-J2 173-A-B WST14-J1-J2 077-A-B WST20-J1-J2 397-A-B WST46-J1-J2 190-A-B W3CN9-J01-J02 191-A-B WST55-J1-J2 218-A-B WDTP1-J98-J49 225-A-B WST60-J1-J2 240-A-B WU62-J1-J2 W4CN2-J21-J22 241-A-B WST65-J1-J2 263-A-B WF17-J1-J2 264-A-B WISOK21-1-2 265-A-B WD9-1-3 266-A-B WISOK27-1-2 267-A-B WU68-J1-J2 WST69-J1-J2 296-A-B W5CN4-J01-J02 302-A-B WST73-J1-J2 WU73.1-J2-J1 326-A-B WU73.2-J1-J2 WSC17-J4-J1 325-B-A WSC15-J2-J1 317-A-B WIM1-I2-O2 WU81-J2-J1 337-A-B WST75-J1-J2 348-A-B",
    "route_short_name": "WIC3_WLNA2-J06_C077_W3CN9_WDTP1-J98_WDTP1-J49_W4CN2-J22_W5CN4_WIM1-O2_C348",
    "config_name": "6095.0_250.0_-71.0L_CIF@-5420.0G40.0_SKA@18080_KKA@0_MLO@10_DTP@-320G-26@1001101010",
    "file_name": "198_C1-K2#6095.0_250.0_-71.0L_CIF@-5420.0G40.0_SKA@18080_KKA@0_MLO@10_DTP@-320G-26@1001101010",
    "power_in": -71.0,
    "power_level": "L",
    "frequency_start": 6095.0,
    "bw": 250.0,
    "cnv_cif": {
        "LO": -5420.0,
        "G": 40.0
    },
    "cnv_ska": {
        "LO": 18080
    },
    "cnv_kka": {
        "LO": 0
    },
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
        "B2": 0,
        "B3": 0,
        "B4": 1,
        "INV": 0,
        "G_NUM": -26,
        "ALC": 1,
        "ALC_LEVEL": -26,
        "LO": -320
    },
    "twta_tas": 0,
    "twta_mda": 0,
    "query_route_ports": [
        [
            "WIC3",
            "J1"
        ],
        [
            "WLNA2",
            "J06"
        ],
        [
            "077",
            "B"
        ],
        [
            "W3CN9",
            "J02"
        ],
        [
            "WDTP1",
            "J98"
        ],
        [
            "WDTP1",
            "J49"
        ],
        [
            "W4CN2",
            "J22"
        ],
        [
            "W5CN4",
            "J02"
        ],
        [
            "WIM1",
            "O2"
        ],
        [
            "348",
            "B"
        ]
    ],
    "calc_set_config": {
        "CNVCIF": {
            "LO": -5420.0,
            "G": 40.0
        },
        "CNVSK": {
            "LO": 18080
        },
        "CNVKKA": {},
        "DTP": {
            "INV": 0,
            "G": -26,
            "LO": -320,
            "ALC": 1,
            "ALC_LEVEL": -26
        },
        "frequency_start": 6095.0,
        "bw": 250.0,
        "power_in": -71.0
    }
}
config1 = {
    "id": 30,
    "route_comb_alias": "030-030_C1-C1",
    "route_in_alias": "030-C1-C1",
    "route_in": [
        "WIC1",
        "WLNA1-J03",
        "WU5"
    ],
    "route_in_band_letters": [
        "C1",
        "C1"
    ],
    "route_in_bands": [
        5725.0,
        6725.0,
        5725.0,
        6725.0
    ],
    "route_out_alias": "030-C1-C1",
    "route_out": [],
    "route_out_band_letters": [
        "C1",
        "C1"
    ],
    "route_out_bands": [
        5725.0,
        6725.0,
        5725.0,
        6725.0
    ],
    "query_route": [
        "WIC1",
        "WLNA1-J03",
        "WU5"
    ],
    "route": [
        [
            "WIC1",
            "J1",
            "J2"
        ],
        [
            "WG1",
            "A",
            "B"
        ],
        [
            "WF1",
            "J01",
            "J02"
        ],
        [
            "001",
            "A",
            "B"
        ],
        [
            "WSC1",
            "J4",
            "J1"
        ],
        [
            "003",
            "A",
            "B"
        ],
        [
            "WLNA1",
            "J02",
            "J03"
        ],
        [
            "007",
            "A",
            "B"
        ],
        [
            "WSC3",
            "J1",
            "J2"
        ],
        [
            "011",
            "A",
            "B"
        ],
        [
            "WISOK1",
            "1",
            "2"
        ],
        [
            "012",
            "A",
            "B"
        ],
        [
            "WD1",
            "J1",
            "J4"
        ],
        [
            "015",
            "A",
            "B"
        ],
        [
            "WISOK8",
            "1",
            "2"
        ],
        [
            "016",
            "A",
            "B"
        ],
        [
            "WU5",
            "J1",
            "J2"
        ]
    ],
    "route_long_name": "WIC1-J1-J2 WG1-A-B WF1-J01-J02 001-A-B WSC1-J4-J1 003-A-B WLNA1-J02-J03 007-A-B WSC3-J1-J2 011-A-B WISOK1-1-2 012-A-B WD1-J1-J4 015-A-B WISOK8-1-2 016-A-B WU5-J1-J2",
    "route_short_name": "WIC1_WLNA1-J03_WU5",
    "config_name": "5725.0_1000.0_-71.0L_CIF@0G0_SKA@0_KKA@0_MLO@00_DTP@0G0@0000000000",
    "file_name": "30_C1-C1#5725.0_1000.0_-71.0L_CIF@0G0_SKA@0_KKA@0_MLO@00_DTP@0G0@0000000000",
    "power_in": -71.0,
    "power_level": "L",
    "frequency_start": 5725.0,
    "bw": 1000.0,
    "cnv_cif": {
        "LO": 0,
        "G": 0
    },
    "cnv_ska": {
        "LO": 0
    },
    "cnv_kka": {
        "LO": 0
    },
    "mlo": {
        "N": 0,
        "R": 0
    },
    "dtp": {
        "TC_N": 0,
        "TC_R": 0,
        "G_N": 0,
        "G_R": 0,
        "B1": 0,
        "B2": 0,
        "B3": 0,
        "B4": 0,
        "INV": 0,
        "G_NUM": 0,
        "ALC": 0,
        "ALC_LEVEL": 0,
        "LO": 0
    },
    "twta_tas": 0,
    "twta_mda": 0,
    "query_route_ports": [
        [
            "WIC1",
            "J1"
        ],
        [
            "WLNA1",
            "J03"
        ],
        [
            "WU5",
            "J2"
        ]
    ],
    "calc_set_config": {
        "CNVCIF": {
            "LO": 0,
            "G": 0
        },
        "CNVSK": {},
        "CNVKKA": {},
        "DTP": {
            "INV": 0,
            "G": 0,
            "LO": 0,
            "ALC": 0,
            "ALC_LEVEL": 0
        },
        "frequency_start": 5725.0,
        "bw": 1000.0,
        "power_in": -71.0
    }
}


class TestMeasure(TestCase):
    def setUp(self) -> None:
        self.m_config1 = Measure(config1)
        self.m_config2 = Measure(config2)

    def test_getMeasureName(self):
        self.assertEqual('WIC1_5725_6725_@MEAS@_L', self.m_config1.calibrationFileNameMain)
        self.assertEqual('WIC3_6225_20350_250_@MEAS@_L', self.m_config2.calibrationFileNameMain)


if __name__ == '__main__':
    unittest.main()

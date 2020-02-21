import re
from typing import Dict

from cg_creator.cg_form import CycleGramGenerator


def get_im3_keys(CSANAME=None, AVERNUMPNA=None, FIXDELF=None, IFBMMT=None, IFBWIM=None, IFBWPNA=None, IM3OR5=None,
                 POINTNUMPNA=None, SMOOTHNUM=None, ISQRANGE=None, SPANPNA=None):
    return {
        'CSANAME': CSANAME,
        'AVERNUMPNA': AVERNUMPNA,
        'FIXDELF': FIXDELF,
        'IFBMMT': IFBMMT,
        'IFBWIM': IFBWIM,
        'IFBWPNA': IFBWPNA,
        'IM3OR5': IM3OR5,
        'POINTNUMPNA': POINTNUMPNA,
        'SMOOTHNUM': SMOOTHNUM,
        'ISQRANGE': ISQRANGE,
        'SPANPNA': SPANPNA,
    }


def get_afc_gd_keys(CSANAME=None, AVERNUMPNA=None, IFBWPNA=None, MDELAY=None, POINTNUMPNA=None, SMOOTHNUM=None,
                    ISQRANGE=None, SPANPNA=None):
    return {
        'CSANAME': CSANAME,
        'AVERNUMPNA': AVERNUMPNA,
        'IFBWPNA': IFBWPNA,
        'MDELAY': MDELAY,
        'POINTNUMPNA': POINTNUMPNA,
        'SMOOTHNUM': SMOOTHNUM,
        'ISQRANGE': ISQRANGE,
        'SPANPNA': SPANPNA,
    }


class Measure:
    def __init__(self, config, nameOfCg, ssi):
        self.config = config
        self._numberOfMeasurePoints = 1601
        self._isConverted = self._getIsConverted()
        self._powerIn = self.config['power_in']
        self._powerIn_coma = str(self._powerIn).replace('.', ',')
        self.bw = int(self.config['bw'])
        self.frequencyInCenter = int((self.config['route_in_bands'][0] + self.config['route_in_bands'][1]) / 2)
        self.frequencyOutCenter = int((self.config['route_out_bands'][2] + self.config['route_out_bands'][3]) / 2)
        self.powerLevel = self.config['power_level']
        self.calibrationFileNameMain = self._getCalibrationFileName()
        self.nameOfCg = nameOfCg

    def _getIsConverted(self) -> bool:
        if re.findall(r'W\dCN\d', self.config['route_long_name']):
            return True
        else:
            return False

    def _getCalibrationFileName(self) -> str:
        if not self._isConverted:
            return f"{self.config['route_in'][0]}_{int(self.config['route_in_bands'][0])}_{int(self.config['route_in_bands'][1])}_@MEAS@_{self.config['power_level']}"
        else:
            return f"{self.config['route_in'][0]}_" \
                   f"{self.frequencyInCenter}_" \
                   f"{self.frequencyOutCenter}_" \
                   f"{int(self.config['bw'])}_@MEAS@_{self.powerLevel}"

    def _get_calibration_file_name_measure(self, measureName) -> str:
        suf: str = ''
        if self.config['dtp']['INV'] == 1:
            suf = '_inv'
        return self.calibrationFileNameMain.replace('@MEAS@', measureName) + suf

    def getCGStr(self):
        cg = CycleGramGenerator(0)
        cg.program(self.nameOfCg)
        cg.compute([
            ['SSI', '=', f'"{self.nameOfCg}"']
        ])
        cg.repeat(1, 32000)
        cg.comment('Общие для всех измерений ключи')
        cg.compute([
            ['FRINCENT', '=', self.frequencyInCenter],
            ['POWIN', '=', self._powerIn_coma],
            ['FROUTCENT', '=', self.frequencyOutCenter],
            ['POWOUT', '=', -20],
        ])
        cg.comment('Выбор измерения')

        cg.menu([
            'Измерение АЧХ',
            'Измерение НГВЗ',
            'Измерение ИМ_3',
            'Выход',
        ])

        cg.select_()
        self._measure_insert(cycl_gen=cg, num_of_meas=1, name_of_meas='АЧХ', keys_of_measure=get_afc_gd_keys(
            CSANAME=f'"{self._get_calibration_file_name_measure("AFC")}"',
            AVERNUMPNA=5,
            IFBWPNA=1000,
            MDELAY=0,
            POINTNUMPNA=self._numberOfMeasurePoints,
            SMOOTHNUM=2,
            ISQRANGE=1,
            SPANPNA=self.bw,
        ))

        self._measure_insert(cycl_gen=cg, num_of_meas=2, name_of_meas='НГВЗ', keys_of_measure=get_afc_gd_keys(
            CSANAME=f'"{self._get_calibration_file_name_measure("GD")}"',
            AVERNUMPNA=5,
            IFBWPNA=1000,
            MDELAY=0,
            POINTNUMPNA=self._numberOfMeasurePoints,
            SMOOTHNUM=2,
            ISQRANGE=1,
            SPANPNA=self.bw,
        ))

        self._measure_insert(cycl_gen=cg, num_of_meas=3, name_of_meas='ИМ_3', keys_of_measure=get_im3_keys(
            CSANAME=f'"{self._get_calibration_file_name_measure("IMD")}"',
            AVERNUMPNA=5,
            FIXDELF=1,
            IFBMMT=10000,
            IFBWIM=10000,
            IFBWPNA=1000,
            IM3OR5=0,
            POINTNUMPNA=41,
            SMOOTHNUM=5,
            ISQRANGE=1,
            SPANPNA=24,
        ))

        cg.select_var(4)
        cg.exit()
        cg.select_end()
        cg.repeat_end()
        cg.program_end()

        return cg.all_data

    @staticmethod
    def _measure_insert(cycl_gen: CycleGramGenerator, num_of_meas: int, name_of_meas: str, keys_of_measure: Dict):

        keys_list = []
        for k in keys_of_measure:
            if not (keys_of_measure[k] is None):
                keys_list.append([k, '=', keys_of_measure[k]])
        cycl_gen.select_var(num_of_meas)
        cycl_gen.comment(f'персональные ключи для {name_of_meas}')
        cycl_gen.compute(keys_list)
        cycl_gen.call_(name_of_meas)

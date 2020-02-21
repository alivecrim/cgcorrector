import re

# from devices.ssi import SSI
from cg_creator.cg_form import CycleGramGenerator


class Measure:
    def __init__(self, config, nameOfCg, ssi):
        self.config = config
        # self.ssi: SSI = ssi
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

    def _getCalibrationFileNameMeasure(self, measureName) -> str:
        suf: str = ''
        if self.config['dtp']['INV'] == 1:
            suf = '_inv'
        return self.calibrationFileNameMain.replace('@MEAS@', measureName) + suf

    def getCGStr(self):
        # config_name = self.config['file_name'].replace('@', '').replace('#', '_')
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

        cg.select_([
            'Измерение АЧХ',
            'Измерение НГВЗ',
            'Измерение ИМ_3',
            'Выход',
        ])

        cg.select_var(1)
        cg.comment('персональные ключи для АЧХ')
        cg.compute([
            ['CSANAME', '=', f'"{self._getCalibrationFileNameMeasure("AFC")}"'],
            ['AVERNUMPNA', '=', 5],
            ['IFBWPNA', '=', 1000],
            ['MDELAY', '=', 0],
            ['POINTNUMPNA', '=', self._numberOfMeasurePoints],
            ['SMOOTHNUM', '=', 2],
            ['ISQRANGE', '=', 1],
            ['SPANPNA', '=', self.bw],
        ])
        cg.call_('АЧХ')

        cg.select_var(2)
        cg.comment('персональные ключи для НГВЗ')
        cg.compute([
            ['CSANAME', '=', f'"{self._getCalibrationFileNameMeasure("GD")}"'],
            ['AVERNUMPNA', '=', 5],
            ['IFBWPNA', '=', 1000],
            ['MDELAY', '=', 0],
            ['POINTNUMPNA', '=', self._numberOfMeasurePoints],
            ['SMOOTHNUM', '=', 2],
            ['ISQRANGE', '=', 1],
            ['SPANPNA', '=', self.bw],
        ])
        cg.call_('НГВЗ')

        cg.select_var(3)
        cg.comment('персональные ключи для ИМ3')
        cg.compute([
            ['CSANAME', '=', f'"{self._getCalibrationFileNameMeasure("IMD")}"'],
            ['AVERNUMPNA', '=', 5],
            ['FIXDELF', '=', 1],
            ['IFBMMT', '=', 10000],
            ['IFBWIM', '=', 10000],
            ['IFBWPNA', '=', 1000],
            ['IM3OR5', '=', 0],
            ['POINTNUMPNA', '=', 41],
            ['SMOOTHNUM', '=', 5],
            ['ISQRANGE', '=', 1],
            ['SPANPNA', '=', 24],
        ])
        cg.call_('ИМ_3')

        cg.select_var(4)
        cg.exit()
        cg.select_end()
        cg.repeat_end()
        cg.program_end()

        return cg.all_data

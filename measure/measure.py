import re


# from devices.ssi import SSI


class Measure:
    def __init__(self, config, nameOfCg, ssi):
        self.config = config
        # self.ssi: SSI = ssi
        self._numberOfMeasurePoints = 1601
        self._isConverted = self._getIsConverted()
        self._powerIn = self.config['power_in']
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
        return f'О|1   |          |ПРОГРАМ     |     |{self.nameOfCg}|               |        ||READY\n' + \
               f'О|2   |          |ВЫЧИСЛ      |     |               |               |        ||\n' + \
               f' |    |          |         SSI|  =  |EMPTY|               |        ||\n' + \
               f' |    |          |       SSI_1|  =  |               |               |        |МШУ|\n' + \
               f' |    |          |       SSI_2|  =  |       21      |               |        |CN1|\n' + \
               f' |    |          |       SSI_3|  =  |       A       |               |        |CN2|\n' + \
               f' |    |          |       SSI_4|  =  |      043      |               |        |CN3|\n' + \
               f' |    |          |       SSI_5|  =  |       20      |               |        |CN4|\n' + \
               f' |    |          |       SSI_6|  =  |       20      |               |        |CN4|\n' + \
               f' |    |          |       SSI_7|  =  |       20      |               |        |CN4|\n' + \
               f'О|3   |          |ПОВТ        |     |       1       |     32000     |        ||\n' + \
               f'К|Общие для всех измерений ключи\n' + \
               f'О|4   |          |ВЫЧИСЛ      |     |               |               |        ||\n' + \
               f' |    |          |    FRINCENT|  =  |     {self.frequencyInCenter}     |               |        ||\n' + \
               f' |    |          |       POWIN|  =  |     {self._powerIn}     |               |        ||\n' + \
               f' |    |          |   FROUTCENT|  =  |     {self.frequencyOutCenter}     |               |        ||\n' + \
               f' |    |          |      POWOUT|  =  |      -20      |               |        ||\n' + \
               f'К|Выбор измерения\n' + \
               f'О|5   |          |МЕНЮ        |     |      +ВЧИ     |               |        ||\n' + \
               f'Ф|Измерение АЧХ\n' + \
               f'Ф|Измерение НГВЗ\n' + \
               f'Ф|Измерение ИМ_3\n' + \
               f'О|6   |          |ВЫБОР       |     |     #ЛМЕН     |               |        ||\n' + \
               f'О|7   |          |ВАРИАНТ     |     |       1       |               |        ||\n' + \
               f'К|персональные ключи для АЧХ\n' + \
               f'О|19  |          |ВЫЧИСЛ      |     |               |               |        ||\n' + \
               f' |    |          |     CSANAME|  =  |{self._getCalibrationFileNameMeasure("AFC")}|               |        ||\n' + \
               f' |    |          |  AVERNUMPNA|  =  |       5       |               |        ||\n' + \
               f' |    |          |     IFBWPNA|  =  |      1000     |               |        ||\n' + \
               f' |    |          |      MDELAY|  =  |       0       |               |        ||\n' + \
               f' |    |          | POINTNUMPNA|  =  |{self._numberOfMeasurePoints}      |               |        ||\n' + \
               f' |    |          |   SMOOTHNUM|  =  |       2       |               |        ||\n' + \
               f' |    |          |    ISQRANGE|  =  |       1       |               |        ||\n' + \
               f' |    |          |     SPANPNA|  =  |      {self.bw}      |               |        ||\n' + \
               f'О|8   |          |ВЫЗВАТЬ     |     |               |      АЧХ      |        ||\n' + \
               f'О|9   |          |ВАРИАНТ     |     |       2       |               |        ||\n' + \
               f'К|персональные ключи для НГВЗ\n' + \
               f'О|10  |          |ВЫЧИСЛ      |     |               |               |        ||\n' + \
               f' |    |          |     CSANAME|  =  |{self._getCalibrationFileNameMeasure("GD")}|               |        ||\n' + \
               f' |    |          |  AVERNUMPNA|  =  |       5       |               |        ||\n' + \
               f' |    |          |     IFBWPNA|  =  |      1000     |               |        ||\n' + \
               f' |    |          |      MDELAY|  =  |       0       |               |        ||\n' + \
               f' |    |          | POINTNUMPNA|  =  |      {self._numberOfMeasurePoints}      |               |        ||\n' + \
               f' |    |          |   SMOOTHNUM|  =  |       2       |               |        ||\n' + \
               f' |    |          |    ISQRANGE|  =  |       1       |               |        ||\n' + \
               f' |    |          |     SPANPNA|  =  |      {self.bw}      |               |        ||\n' + \
               f'О|11  |          |ВЫЗВАТЬ     |     |               |      НГВЗ     |        ||\n' + \
               f'К|И З М Е Р Е Н И Е  - НГВЗ\n' + \
               f'К|персональные ключи для ИМ_3\n' + \
               f'О|12  |          |ВЫЧИСЛ      |     |               |               |        ||\n' + \
               f' |    |          |     CSANAME|  =  |{self._getCalibrationFileNameMeasure("IMD")}|               |        ||\n' + \
               f' |    |          |  AVERNUMPNA|  =  |       5       |               |        ||\n' + \
               f' |    |          |     FIXDELF|  =  |       1       |               |        ||\n' + \
               f' |    |          |      IFBMMT|  =  |     10000     |               |        ||\n' + \
               f' |    |          |      IFBWIM|  =  |     10000     |               |        ||\n' + \
               f' |    |          |     IFBWPNA|  =  |      1000     |               |        ||\n' + \
               f' |    |          |      IM3OR5|  =  |       0       |               |        ||\n' + \
               f' |    |          |      MDELAY|  =  |       2       |               |        ||\n' + \
               f' |    |          | POINTNUMPNA|  =  |       41      |               |        ||\n' + \
               f' |    |          |   SMOOTHNUM|  =  |       5       |               |        ||\n' + \
               f' |    |          |    ISQRANGE|  =  |       1       |               |        ||\n' + \
               f' |    |          |     SPANPNA|  =  |       24      |               |        ||\n' + \
               f'О|13  |          |ВЫЗВАТЬ     |     |               |      ИМ_3     |        ||\n' + \
               f'О|14  |          |ВАРИАНТ     |     |       3       |               |        ||\n' + \
               f'К|И З М Е Р Е Н И Е  - ИМ_3\n' + \
               f'О|15  |          |КПРОГРАМ    |     |               |               |        ||\n'

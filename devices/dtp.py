from cg_creator.cg_form import CycleGramGenerator
from cg_creator.enums import KPI


def calcGain(reqGain, alc, bw) -> int:
    if alc:
        # return round((reqGain + 103.725 - 10 * m.log10(bw)) / 0.0625)
        return 100
    return 0


class DTP:
    def __init__(self, route, config):
        self._config = config
        self._num = 1
        self._inputPort = int(route[1][1])
        self._outputPort = int(route[2][1])

        self._bw = self._config['bw']
        self._alc = self._config['dtp']['ALC'] == 1
        if self._alc:
            self._gain = self._config['dtp']['ALC_LEVEL']
        else:
            self._gain = self._config['dtp']['G_NUM']

        self._fill_data()

    def getNum(self):
        return self._num

    def _makeDtpNotation(self):
        self.dtpNotation = [
            {
                'ch': 0,
                'chmod': 1,
                'input': self._inputPort - 1,
                'output': self._outputPort - 1,
                'alc': self._alc,
                'bw': round(self._bw / 0.3125) - 1,
                'gain': calcGain(self._gain, self._alc, round(self._bw / 0.3125)),
                'ifStart': 0,
                'ofStart': 0,
            },
        ]

    def _fill_data(self):
        self._makeDtpNotation()

    def _getNum(self):
        pass

    def _createCh(self, d, num):
        alc_fgm = lambda x: 'АРУ' if x else 'ФРУ'
        create_mode = lambda x: '<без маршрутизации>' if (x == 0) else (
            "<маршрутизация с удалением>" if (x == 1) else "<маршрутизация без удаления>")

        cg = CycleGramGenerator(num)
        cg.comment([
            f'Включение канала {d["ch"]}',
            f'Входной порт:{d["input"]}, Выходной порт:{d["output"]}',
            f'Полоса:{self._bw} МГц',
            f'Начальная частота: ВХОД-{d["ifStart"] * 0.3125 + 675} МГц',
            f'Начальная частота: ВЫХОД-{d["ofStart"] * 0.3125 + 355.0} МГц',
            f'Режим работы: {alc_fgm(d["alc"])}',
            f'Режим создания: {create_mode(d["chmod"])}',
        ])

        if d['alc']:
            cg.send('R15173')
        else:
            cg.send('R15174')
        cg.pause(1)

        if d['chmod'] == 0:
            cg.send('R15170')
        elif d['chmod'] == 1:
            cg.send('R15171')
        elif d['chmod'] == 2:
            cg.send('R15172')
        cg.pause(1)

        cg.send(KPI.KPI_CMD, [[KPI.PAR, '"НОМКАНАЛ"'], [KPI.VAL, d['ch']]])
        cg.send(KPI.KPI_CMD, [[KPI.PAR, '"ВХПОРТ"'], [KPI.VAL, d['input']]])
        cg.send(KPI.KPI_CMD, [[KPI.PAR, '"ВЫХПОРТ"'], [KPI.VAL, d['output']]])
        cg.send(KPI.KPI_CMD, [[KPI.PAR, '"ПОЛОСА"'], [KPI.VAL, d['bw']]])
        cg.send(KPI.KPI_CMD, [[KPI.PAR, '"ВХЧАСТ"'], [KPI.VAL, d['ifStart']]])
        cg.send(KPI.KPI_CMD, [[KPI.PAR, '"ВЫХЧАСТ"'], [KPI.VAL, d['ofStart']]])
        cg.send(KPI.KPI_CMD, [[KPI.PAR, '"УРУСИЛ"'], [KPI.VAL, d['gain']]])

        cg.send('R15167')

        cg.comment('ЗАПУСК ОПРОСА ТМИ')
        row = cg.all_data
        reqTm = [
            [15016, 0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]],
            [15017, 0,
             [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]],
            [15020, 0, [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]],
            [15021, 1, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]],
            [15022, 1,
             [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]],
            [15023, 1, [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]],
            [15024, 2, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]],
            [15025, 2,
             [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]],
            [15026, 2, [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]],
            [15027, 3, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]],
            [15030, 3,
             [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]],
            [15031, 3, [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]],
            [15032, 4, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]],
            [15033, 4,
             [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]],
            [15034, 4, [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]],
            [15035, 5, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]],
            [15036, 5,
             [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]],
            [15037, 5, [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]],
        ]
        cmd = ''

        for s in reqTm:
            if d['output'] == s[1]:
                if d['ch'] in s[2]:
                    cmd = 'R' + str(s[0])

        if d['ch'] + 1 < 10:
            ch = '0' + str(d['ch'] + 1)
        else:
            ch = str(d['ch'] + 1)
        op = str(d['output'])
        ip = str(d['input'])
        cs = str(d['chmod'])
        bw = str(d['bw'])
        if str(d['alc']):
            gm = 0
        else:
            gm = 1
        inF = str(d['ifStart'])
        outF = str(d['ofStart'])
        gl = str(d['gain'])

        cg.send(cmd)
        cg.pause(1)

        cg.if_([['DTPN', 1]])
        cg.wait(60, [
            [f'OP{op}CH{ch}IP_N', ip],
            [f'OP{op}CH{ch}CS_N', cs],
            [f'OP{op}CH{ch}GM_N', int(gm)],
            [f'OP{op}CH{ch}IF_N', inF],
            [f'OP{op}CH{ch}OF_N', outF],
            [f'OP{op}CH{ch}BW_N', bw],
            [f'OP{op}CH{ch}GL_N', gl],
        ])
        cg.if_end()

        cg.if_([['DTPR', 1]])
        cg.wait(60, [
            [f'OP{op}CH{ch}IP_R', ip],
            [f'OP{op}CH{ch}CS_R', cs],
            [f'OP{op}CH{ch}GM_R', int(gm)],
            [f'OP{op}CH{ch}IF_R', inF],
            [f'OP{op}CH{ch}OF_R', outF],
            [f'OP{op}CH{ch}BW_R', bw],
            [f'OP{op}CH{ch}GL_R', gl],
        ])
        cg.if_end()
        return [cg.all_data, cg.idx.get_value()]

    def getCGStrConfig(self, num) -> []:
        row = ''
        for dtpConfig in self.dtpNotation:
            tmp = self._createCh(dtpConfig, num)
            row += tmp[0]
            num = tmp[1]
        return [row, num]

    def getCGStrOn(self, num) -> []:
        if self._config['dtp']['TC_N'] == 1:
            cg_name = '763_БСК1_DTP_О_ВКЛ'
        elif self._config['dtp']['TC_R'] == 1:
            cg_name = '763_БСК1_DTP_Р_ВКЛ'
        else:
            return ['', num]
        cg = CycleGramGenerator(num)
        cg.comment('Включение DTP')
        cg.call_(cg_name)
        return [cg.all_data, cg.idx.get_value()]

    def getCGStrSwitch(self, num) -> []:
        row = ''
        return [row, num]

    def isDevice(self):
        return True

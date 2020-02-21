from utils.cg_form import getCGStrFormat
from utils.enums import Op, CMD, KPI


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
        alcfgm = lambda x: 'АРУ' if x else 'ФРУ'

        createmode = lambda x: '<без маршрутизации>' if (x == 0) else (
            "<маршрутизация с удалением>" if (x == 1) else "<маршрутизация без удаления>")

        row = ''
        # cg =
        row += getCGStrFormat(operation=Op.k, numOrComment=f'Включение канала {d["ch"]}')
        row += getCGStrFormat(operation=Op.k, numOrComment=f'Входной порт:{d["input"]}, Выходной порт:{d["output"]}')
        row += getCGStrFormat(operation=Op.k, numOrComment=f'Полоса:{self._bw} МГц')
        row += getCGStrFormat(operation=Op.k, numOrComment=f'Начальная частота: ВХОД-{d["ifStart"] * 0.3125 + 675} МГц')
        row += getCGStrFormat(operation=Op.k,
                              numOrComment=f'Начальная частота: ВЫХОД-{d["ofStart"] * 0.3125 + 355.0} МГц')
        row += getCGStrFormat(operation=Op.k, numOrComment=f'Режим работы: {alcfgm(d["alc"])}')
        row += getCGStrFormat(operation=Op.k, numOrComment=f'Режим создания: {createmode(d["chmod"])}')

        if d['alc']:
            row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value='R15173')
        else:
            row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value='R15174')
        num += 1
        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.PAUSE, value=1)
        num += 1

        if d['chmod'] == 0:
            row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value='R15170')
        elif d['chmod'] == 1:
            row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value='R15171')
        elif d['chmod'] == 2:
            row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value='R15172')
        num += 1
        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.PAUSE, value=1)
        num += 1

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value='M_KPI_PAR')
        row += getCGStrFormat(command=KPI.PAR, value='"ВЫХПОРТ"')
        row += getCGStrFormat(command=KPI.VAL, value=d['output'])
        num += 1

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value='M_KPI_PAR')
        row += getCGStrFormat(command=KPI.PAR, value='"НОМКАНАЛ"')
        row += getCGStrFormat(command=KPI.VAL, value=d['ch'])
        num += 1

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value='M_KPI_PAR')
        row += getCGStrFormat(command=KPI.PAR, value='"ВХПОРТ"')
        row += getCGStrFormat(command=KPI.VAL, value=d['input'])
        num += 1

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value='M_KPI_PAR')
        row += getCGStrFormat(command=KPI.PAR, value='"ВХЧАСТ"')
        row += getCGStrFormat(command=KPI.VAL, value=d['ifStart'])
        num += 1

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value='M_KPI_PAR')
        row += getCGStrFormat(command=KPI.PAR, value='"ВЫХЧАСТ"')
        row += getCGStrFormat(command=KPI.VAL, value=d['ofStart'])
        num += 1

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value='M_KPI_PAR')
        row += getCGStrFormat(command=KPI.PAR, value='"ПОЛОСА"')
        row += getCGStrFormat(command=KPI.VAL, value=d['bw'])
        num += 1

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value='M_KPI_PAR')
        row += getCGStrFormat(command=KPI.PAR, value='"УРУСИЛ"')
        row += getCGStrFormat(command=KPI.VAL, value=d['gain'])
        num += 1

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value='R15167')
        num += 1

        row += getCGStrFormat(operation=Op.k, numOrComment='ЗАПУСК ОПРОСА ТМИ')
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

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.SEND, value=cmd)
        num += 1
        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.PAUSE, value=1)
        num += 1
        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.IF)
        num += 1
        row += getCGStrFormat(command='DTPN', value=1)

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.WAIT, value=60)
        num += 1
        row += getCGStrFormat(command=f'OP{op}CH{ch}IP_N', value=ip)
        row += getCGStrFormat(command=f'OP{op}CH{ch}CS_N', value=cs)
        row += getCGStrFormat(command=f'OP{op}CH{ch}GM_N', value=int(gm))
        row += getCGStrFormat(command=f'OP{op}CH{ch}IF_N', value=inF)
        row += getCGStrFormat(command=f'OP{op}CH{ch}OF_N', value=outF)
        row += getCGStrFormat(command=f'OP{op}CH{ch}BW_N', value=bw)
        row += getCGStrFormat(command=f'OP{op}CH{ch}GL_N', value=gl)

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.IF_END)
        num += 1

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.IF)
        num += 1
        row += getCGStrFormat(command='DTPR', value=1)

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.WAIT, value=60)
        num += 1
        row += getCGStrFormat(command=f'OP{op}CH{ch}IP_R', value=ip)
        row += getCGStrFormat(command=f'OP{op}CH{ch}CS_R', value=cs)
        row += getCGStrFormat(command=f'OP{op}CH{ch}GM_R', value=int(gm))
        row += getCGStrFormat(command=f'OP{op}CH{ch}IF_R', value=inF)
        row += getCGStrFormat(command=f'OP{op}CH{ch}OF_R', value=outF)
        row += getCGStrFormat(command=f'OP{op}CH{ch}BW_R', value=bw)
        row += getCGStrFormat(command=f'OP{op}CH{ch}GL_R', value=gl)

        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.IF_END)
        num += 1

        return [row, num + 1]

    def getCGStrConfig(self, num) -> []:
        row = ''
        for dtpConfig in self.dtpNotation:
            tmp = self._createCh(dtpConfig, num)
            row += tmp[0]
            num = tmp[1]
        return [row, num]

    def getCGStrOn(self, num) -> []:
        row = ''
        if self._config['dtp']['TC_N'] == 1:
            cg_name = '763_БСК1_DTP_О_ВКЛ'
        elif self._config['dtp']['TC_R'] == 1:
            cg_name = '763_БСК1_DTP_Р_ВКЛ'
        else:
            return [row, num]
        row += getCGStrFormat(operation=Op.k, numOrComment='Включение DTP')
        row += getCGStrFormat(operation=Op.o, numOrComment=num, command=CMD.CALL, nameOfCg=cg_name)
        num += 1
        return [row, num]

    def getCGStrSwitch(self, num) -> []:
        row = ''
        return [row, num]

    def isDevice(self):
        return True

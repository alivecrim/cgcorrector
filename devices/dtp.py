import math

from cg_creator.cg_form import CycleGramGenerator
from cg_creator.enums import KPI, DtpCmd, DtpKPI


def calcGain(reqGain, alc, bw) -> int:
    if alc:
        numberOfElementary = bw / 0.3125
        powerPerElementary = reqGain - 10 * math.log10(numberOfElementary)
        return round(((powerPerElementary + 103.7125) * 8))
    else:
        return round(((reqGain + 86) * 8))
    return 0


class DTP:
    def __init__(self, route, config):
        self._config = config
        self._num = 1
        nom = ''
        if self._config['dtp']['TC_N'] == 1:
            nom = 'N'
        if self._config['dtp']['TC_R'] == 1:
            nom = 'R'
        self.name = 'D' + nom
        if len(route[1]) == 4:
            self._inputPort_hw = int(route[1][1:3])
        else:
            self._inputPort_hw = int(route[1][1])
        self._outputPort_hw = int(route[2][1])

        dtp_hard_to_soft = {
            1: -1,
            2: 0,
            3: 1,
            4: 2,
            5: 3,
            6: 4,
            7: 5,
            8: 6,
            9: -2,
            10: 7,
        }
        self._inputPort = dtp_hard_to_soft[self._inputPort_hw]
        self._outputPort = dtp_hard_to_soft[self._outputPort_hw]

        self._bw = self._config['bw']
        self._alc = self._config['dtp']['ALC'] == 1
        if self._alc:
            self._gain = self._config['dtp']['ALC_LEVEL']
        else:
            self._gain = self._config['dtp']['G_NUM']

        self._fill_data()

    def _fill_data(self):
        self._makeDtpNotation()

    def _makeDtpNotation(self):
        self.dtpNotation = [
            {
                'ch': 0,
                'chmod': 1,
                'input': self._inputPort,
                'output': self._outputPort,
                'alc': self._alc,
                'bw': round(self._bw / 0.3125) - 1,
                'gain': calcGain(self._gain, self._alc, self._bw),
                'ifStart': 0,
                'ofStart': 0,
            },
        ]

    def _getNum(self):
        pass

    def _createCh(self, dtpNotationItem, num):
        alc_fgm = lambda x: 'АРУ' if x else 'ФРУ'
        create_mode = lambda x: '<без маршрутизации>' if (x == 0) else (
            "<маршрутизация с удалением>" if (x == 1) else "<маршрутизация без удаления>")
        cg = CycleGramGenerator(num)

        # Проверка на резервные вход 1!
        if self._inputPort == -1 or self._outputPort == -1:
            cg.comment([f'Проверка на включенный резерв RT0'])
            self.check_for_redundant_RT0(cg)
            if self._inputPort == -1:
                self.dtpNotation[0]['input'] = 0
            if self._outputPort == -1:
                self.dtpNotation[0]['output'] = 0
        # Проверка на резервные вход 9!
        if self._inputPort == -2:
            cg.comment([f'Проверка на включенный резерв RT7'])
            self.check_for_redundant_RT7(cg)
            self.dtpNotation[0]['input'] = 7

        cg.comment([
            f'Включение канала {dtpNotationItem["ch"]}',
            f'Входной порт:{self._inputPort_hw}, Выходной порт:{self._outputPort_hw}',
            f'Полоса:{self._bw} МГц',
            f'Начальная частота: ВХОД-{dtpNotationItem["ifStart"] * 0.3125 + 675} МГц',
            f'Начальная частота: ВЫХОД-{dtpNotationItem["ofStart"] * 0.3125 + 355.0} МГц',
            f'Режим работы: {alc_fgm(dtpNotationItem["alc"])}',
            f'Режим создания: {create_mode(dtpNotationItem["chmod"])}',
        ])


        if dtpNotationItem['alc']:
            cg.send(DtpCmd.ALC)
        else:
            cg.send(DtpCmd.FGM)
        cg.pause(1)

        if dtpNotationItem['chmod'] == 0:
            cg.send(DtpCmd.CreateInMemory)
        elif dtpNotationItem['chmod'] == 1:
            cg.send(DtpCmd.CreateWithDelete)
        elif dtpNotationItem['chmod'] == 2:
            cg.send(DtpCmd.CreateWithoutDelete)
        cg.pause(1)

        cg.send(KPI.KPI_CMD, [[KPI.PAR, DtpKPI.chNum], [KPI.VAL, dtpNotationItem['ch']]])
        cg.send(KPI.KPI_CMD, [[KPI.PAR, DtpKPI.inputPort], [KPI.VAL, dtpNotationItem['input']]])
        cg.send(KPI.KPI_CMD, [[KPI.PAR, DtpKPI.outputPort], [KPI.VAL, dtpNotationItem['output']]])
        cg.send(KPI.KPI_CMD, [[KPI.PAR, DtpKPI.bandwidth], [KPI.VAL, dtpNotationItem['bw']]])
        cg.send(KPI.KPI_CMD, [[KPI.PAR, DtpKPI.input_frequency], [KPI.VAL, dtpNotationItem['ifStart']]])
        cg.send(KPI.KPI_CMD, [[KPI.PAR, DtpKPI.output_frequency], [KPI.VAL, dtpNotationItem['ofStart']]])
        cg.send(KPI.KPI_CMD, [[KPI.PAR, DtpKPI.gain], [KPI.VAL, dtpNotationItem['gain']]])

        cg.send(DtpCmd.CreateChannel)

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
            if (dtpNotationItem['output']) == s[1]:
                if dtpNotationItem['ch'] in s[2]:
                    cmd = 'R' + str(s[0])

        if dtpNotationItem['ch'] + 1 < 10:
            ch = '0' + str(dtpNotationItem['ch'] + 1)
        else:
            ch = str(dtpNotationItem['ch'] + 1)
        op = str(dtpNotationItem['output'] + 1)
        ip = str(dtpNotationItem['input'])
        cs = str(3)
        bw = str(dtpNotationItem['bw'])
        if dtpNotationItem['alc']:
            gm = 0
        else:
            gm = 1
        inF = str(dtpNotationItem['ifStart'])
        outF = str(dtpNotationItem['ofStart'])
        gl = str(dtpNotationItem['gain'] * 2)

        cg.send(cmd)
        cg.pause(20)

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

    def check_for_redundant_RT0(self, cg):

        cg.if_([['DTPN', 1]])
        cg.if_([['RT0S0_N', 1]])
        cg.if_([['RT0RED_N', 0]])
        cg.call_("763_БСК1_RT_ВКЛ_О", [
            "0",
            "1"
        ])
        cg.if_end()
        cg.if_end()
        cg.if_end()

        cg.if_([['DTPR', 1]])
        cg.if_([['RT0S0_R', 1]])
        cg.if_([['RT0RED_R', 0]])
        cg.call_("763_БСК1_RT_ВКЛ_Р", [
            "0",
            "1"
        ])
        cg.if_end()
        cg.if_end()
        cg.if_end()

    def check_for_redundant_RT7(self, cg):
        cg.if_([['DTPN', 1]])
        cg.if_([['RT7S0_N', 1]])
        cg.if_([['RT7RED_N', 0]])
        cg.call_("763_БСК1_RT_ВКЛ_О", [
            "7",
            "2"
        ])
        cg.if_end()
        cg.if_end()
        cg.if_end()

        cg.if_([['DTPR', 1]])
        cg.if_([['RT7S0_R', 1]])
        cg.if_([['RT7RED_R', 0]])
        cg.call_("763_БСК1_RT_ВКЛ_Р", [
            "7",
            "2"
        ])
        cg.if_end()
        cg.if_end()
        cg.if_end()

    def getCGStrConfig(self, num) -> []:
        row = ''
        for dtpConfig in self.dtpNotation:
            dtp_create_ch_result = self._createCh(dtpConfig, num)
            row += dtp_create_ch_result[0]
            num = dtp_create_ch_result[1]
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

    def getCGStrOff(self, num) -> []:
        if self._config['dtp']['TC_N'] == 1:
            cg_name = '763_БСК1_DTP_О_ОТКЛ'
        elif self._config['dtp']['TC_R'] == 1:
            cg_name = '763_БСК1_DTP_Р_ОТКЛ'
        else:
            return ['', num]
        cg = CycleGramGenerator(num)
        cg.comment('Отключение DTP')
        cg.call_(cg_name)
        return [cg.all_data, cg.idx.get_value()]

    @staticmethod
    def getCGStrSwitch(num) -> []:
        return ['', num]

    @staticmethod
    def isDevice():
        return True

    def getNum(self):
        return self._num

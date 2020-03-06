from cg_creator.cg_form import CycleGramGenerator


class CN:

    def __init__(self, definition: list, config: list):
        self.num: int = 0
        self._definition = definition
        self.type: str = ''
        self._gain = 0
        self._lo = 0
        self._config = config
        self._fill_data()
        self.name = 'CN' + str(self.num)

    def _fill_data(self):
        self._setNum()
        self._setGainLo()

    def getNum(self):
        return self.num

    def _setNum(self):
        self.firstNum = self._definition[0][1]
        if self.firstNum == '1':
            self.type = 'KuC'
        if self.firstNum == '2':
            self.type = 'LC'
        if self.firstNum == '3':
            self.type = 'CIF'
        if self.firstNum == '4':
            self.type = 'IFS'
        if self.firstNum == '5':
            self.type = 'SKa'
        if self.firstNum == '6':
            self.type = 'KKa'

        self.secondNum = self._definition[0][4:]
        if len(self.secondNum) < 2:
            self.secondNum = '0' + self.secondNum

        self.num = int(self.firstNum + self.secondNum)

    def _setGainLo(self):
        if self.type in ['CIF']:
            self._lo = self._config['cnv_cif']['LO']
            self._gain = self._config['cnv_cif']['G']
        if self.type in ['KKa']:
            self._lo = self._config['cnv_kka']['LO']
        if self.type in ['SKa']:
            self._lo = self._config['cnv_ska']['LO']
        if self.type in ['IFS']:
            self._lo = self._config['cnv_ifs']['LO']
        if self.type in ['LC']:
            self._lo = self._config['cnv_lc']['LO']
        if self.type in ['KuC']:
            self._lo = self._config['cnv_kuc']['LO']

    def __repr__(self):
        return f'{self.type}{self.num}'

    def getCGStrSwitch(self, num) -> []:
        row = ''
        return [row, num]

    def getCGStrOn(self, num) -> []:
        row = ''
        switchOnStr = self._switchOn(num)
        row += switchOnStr[0]
        num = switchOnStr[1]
        return [row, num]

    def getCGStrOff(self, num) -> []:
        row = ''
        switchOffStr = self._switchOff(num)
        row += switchOffStr[0]
        num = switchOffStr[1]
        return [row, num]

    def getCGStrConfig(self, num) -> []:
        row = ''
        setLoStr = self._setLo(num)
        row += setLoStr[0]
        num = setLoStr[1]

        setGainStr = self._setGain(num)
        row += setGainStr[0]
        num = setGainStr[1]
        return [row, num]

    def _switchOn(self, num) -> []:
        cg = CycleGramGenerator(num)
        cg.comment(f'Включение КНВ W{self.firstNum}CN{self.secondNum}')
        cg.call_('763_БСК1_КНВ_ВКЛ', [self.num])
        cg.pause(1)
        return [cg.all_data, cg.idx.get_value()]

    def _switchOff(self, num) -> []:
        cg = CycleGramGenerator(num)
        cg.comment(f'Отлючение КНВ W{self.firstNum}CN{self.secondNum}')
        cg.call_('763_БСК1_КНВ_ОТКЛ', [self.num])
        cg.pause(1)
        return [cg.all_data, cg.idx.get_value()]

    def _setLo(self, num) -> []:
        row = ''
        if self.type in ['CIF', 'KKa', 'SKa']:
            cg = CycleGramGenerator(num)
            cg.comment(f'Установка частоты переноса КНВ W{self.firstNum}CN{self.secondNum}')
            cg.call_('763_БСК1_КНВ_УСТ_ЧАСТ', [self.num,
                                               int(abs(self._lo))
                                               ])
            cg.pause(1)
            return [cg.all_data, cg.idx.get_value()]
        return [row, num]

    def _setGain(self, num) -> []:
        row = ''
        if self.type in ['CIF']:
            cg = CycleGramGenerator(num)
            cg.comment(f'Установка усиления КНВ W{self.firstNum}CN{self.secondNum}')
            cg.call_('763_БСК1_КНВ_УСТ_ШАГ', [
                self.num,
                int(self._gain)
            ])
            cg.pause(1)
            return [cg.all_data, cg.idx.get_value()]
        return [row, num]

    def isConfigurable(self):
        if self.type in ['CIF', 'KKa', 'SKa']:
            return True
        return False

    def isDevice(self):
        return True

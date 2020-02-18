class CN:

    def __init__(self, definition: list, config: list):
        self._num: int = 0
        self._definition = definition
        self._type: str = ''
        self._gain = 0
        self._lo = 0
        self._config = config
        self._fill_data()

    def _fill_data(self):
        self._setNum()
        self._setGainLo()

    def getNum(self):
        return self._num

    def _setNum(self):
        self.firstNum = self._definition[0][1]
        if self.firstNum == '1':
            self._type = 'KuC'
        if self.firstNum == '2':
            self._type = 'LC'
        if self.firstNum == '3':
            self._type = 'CIF'
        if self.firstNum == '4':
            self._type = 'IFC'
        if self.firstNum == '5':
            self._type = 'SKa'
        if self.firstNum == '6':
            self._type = 'KKa'

        self.secondNum = self._definition[0][4:]
        if len(self.secondNum) < 2:
            self.secondNum = '0' + self.secondNum

        self._num = int(self.firstNum + self.secondNum)

    def _setGainLo(self):
        if self._type in ['CIF']:
            self._lo = self._config['cnv_cif']['LO']
            self._gain = self._config['cnv_cif']['G']
        if self._type in ['KKa']:
            self._lo = self._config['cnv_kka']['LO']
        if self._type in ['SKa']:
            self._lo = self._config['cnv_ska']['LO']

    def __repr__(self):
        return f'{self._type}{self._num}'

    def getCGStrSwitch(self, num) -> []:
        row = ''
        return [row, num]

    def getCGStrOn(self, num) -> []:
        row = ''
        switchOnStr = self._switchOn(num)
        row += switchOnStr[0]
        num = switchOnStr[1]
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
        cg_name = '763_БСК1_КНВ_ВКЛ'
        row = ''

        row += f'К|Включение КНВ W{self.firstNum}CN{self.secondNum}|          |            |     |               |               |        |               ||\n'
        row += f'О|   {num + 1}|          |     ВЫЗВАТЬ|     |               |{cg_name}|        |               ||\n'
        row += f' |    |          |            |  &1 |              {self._num}|               |        |               ||\n'
        row += f'О|   {num + 2}|          |       ПАУЗА|     |       1       |               |        |               ||\n'
        return [row, num + 2]

    def _setLo(self, num) -> []:
        row = ''
        if self._type in ['CIF', 'KKa', 'SKa']:
            cg_name = '763_БСК1_КНВ_УСТ_ЧАСТ'
            row += f'К|Установка частоты переноса КНВ W{self.firstNum}CN{self.secondNum}|          |            |     |               |               |        |               ||\n'
            row += f'О|   {num + 1}|          |     ВЫЗВАТЬ|     |               |{cg_name}|        |               ||\n'
            row += f' |    |          |            |  &1 |              {self._num}|               |        |               ||\n'
            row += f' |    |          |            |  &2 |              {int(abs(self._lo))}|               |        |               ||\n'
            row += f'О|   {num + 2}|          |       ПАУЗА|     |       1       |               |        |               ||\n'
            return [row, num + 2]
        return [row, num]

    def _setGain(self, num) -> []:
        row = ''
        if self._type in ['CIF']:
            cg_name = '763_БСК1_КНВ_УСТ_ШАГ'
            row += f'К|Установка усиления КНВ W{self.firstNum}CN{self.secondNum}|          |            |     |               |               |        |               ||\n'
            row += f'О|   {num + 1}|          |     ВЫЗВАТЬ|     |               |{cg_name}|        |               ||\n'
            row += f' |    |          |            |  &1 |              {self._num}|               |        |               ||\n'
            row += f' |    |          |            |  &2 |              {int(self._gain)}|               |        |               ||\n'
            row += f'О|   {num + 2}|          |       ПАУЗА|     |       1       |               |        |               ||\n'
            return [row, num + 2]
        return [row, num]

    def isConfigurable(self):
        if self._type in ['CIF', 'KKa', 'SKa']:
            return True
        return False

    def isDevice(self):
        return True

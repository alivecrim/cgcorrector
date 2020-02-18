class MLO:
    def __init__(self, config: list):
        self._num: int = 0
        self._config = config
        self._fill_data();

    def _fill_data(self):
        self._setNum()

    def _setNum(self):
        if self._config['N'] == 1:
            self._num = 1
        if self._config['R'] == 1:
            self._num = 2
        else:
            self._num = 0

    def getNum(self):
        return self._num
    def _getSwitchDef(self):
        if self._num == 1:
            return [['WSCT1', 'J1', 'J2'], ['WSCT2', 'J1', 'J4']]
        if self._num == 2:
            return [['WSCT1', 'J1', 'J4'], ['WSCT2', 'J1', 'J2']]
        return []

    def getCGStrSwitch(self, num) -> []:
        row = ''
        return [row, num]

    def getCGStrOn(self, num) -> []:
        row = ''
        if not (self._num == 0):
            cg_name = '763_БСК1_MLO_ВКЛ'
            row += f'К|Включение MLO {self._num}|          |            |     |               |               |        |               ||\n'
            row += f'О|   {num + 1}|          |     ВЫЗВАТЬ|     |               |{cg_name}|        |               ||\n'
            row += f' |    |          |            |  &1 |              {self._num}|               |        |               ||\n'
            row += f'О|   {num + 2}|          |       ПАУЗА|     |       1       |               |        |               ||\n'
            return [row, num + 2]
        return [row, num]

    def getCGStrConfig(self, num) -> []:
        row = ''
        return [row, num]

    def isConfigurable(self):
        return False

    def isDevice(self):
        if not (self._num == 0):
            return True
        return False
import utils.splitters as u


class LNA:
    def __init__(self, definition: list):
        self._num: int = 0
        self._definition = definition
        self._type: str = 'LNA'
        self._fillData()

    def _setNum(self):
        self._num = int(u.splitByDigit(self._definition[0])[1]) * 10
        inner_num = int(self._definition[1][-1:] + self._definition[2][-1:])
        if inner_num == 23:
            self._num += 1
        if inner_num == 56:
            self._num += 2
        if inner_num == 89:
            self._num += 3

    def getNum(self):
        return self._num

    def _fillData(self):
        self._setNum()

    def __repr__(self):
        return f'{self._type}{self._num}'

    def getCGStrOn(self, num) -> []:
        cg_name = '763_БСК1_МШУ_ВКЛ'
        row = ''

        row += f'К|Включение МШУ {self._num}|          |            |     |               |               |        |               ||\n'
        row += f'О|   {num + 1}|          |     ВЫЗВАТЬ|     |               |{cg_name}|        |               ||\n'
        row += f' |    |          |            |  &1 |              {self._num}|               |        |               ||\n'
        row += f'О|   {num + 2}|          |       ПАУЗА|     |       1       |               |        |               ||\n'
        return [row, num + 2]

    def getCGStrSwitch(self, num) -> []:
        row = ''
        return [row, num]

    def getCGStrConfig(self, num) -> []:
        row = ''
        return [row, num]

    def isConfigurable(self):
        return False

    def isDevice(self):
        return True

import utils.splitters as u


def _checkPosition(position: str, checkedStr: str) -> bool:
    positionInverse: str = position[1] + position[0]
    if checkedStr == position or checkedStr == positionInverse:
        return True
    else:
        return False


class Switch:

    def __init__(self, definition: list):
        self._position: int = 0
        self._type: str = ''
        self._num: int = 0
        self._definition = definition
        self._fill_data()

    def _fill_data(self):
        self._setNum()
        self._setType()
        self._getPosition()

    def _getPosition(self):
        position: str = self._definition[1][1] + self._definition[2][1]

        if self._type == 'C' or self._type == 'A' or self._type == 'CW' or self._type == 'CT':
            if _checkPosition(position, '12') or _checkPosition(position, '34'):
                self._position = 1
            elif _checkPosition(position, '32') or _checkPosition(position, '14'):
                self._position = 2
            else:
                self._position = 0

        if self._type == 'T':
            if _checkPosition(position, '14') or _checkPosition(position, '32'):
                self._position = 1
            elif _checkPosition(position, '12') or _checkPosition(position, '34'):
                self._position = 2
            elif _checkPosition(position, '13') or _checkPosition(position, '24'):
                self._position = 3
            else:
                self._position = 0

        if self._type == 'R':
            if _checkPosition(position, '12') or _checkPosition(position, '34'):
                self._position = 1
            elif _checkPosition(position, '13'):
                self._position = 2
            elif _checkPosition(position, '14') or _checkPosition(position, '23'):
                self._position = 3
            elif _checkPosition(position, '24'):
                self._position = 4
            else:
                self._position = 0

    def _setNum(self):
        switchName: str = self._definition[0]
        self._num = int(u.splitByDigit(switchName)[1])

    def _setType(self):
        switchName: str = self._definition[0]
        self._type = u.splitByDigit(switchName)[0][2:]

    def __repr__(self):
        return f'WS{self._type}{self._num} = {self._position}'

    def getCGStrSwitch(self, num) -> []:
        cg_name = ''
        if self._type == "C":
            cg_name = '763_БСК1_ПРК_C_WSC_ПОЗ'
        if self._type == "A":
            cg_name = '763_БСК1_ПРК_C_WSA_ПОЗ'
        if self._type == "CW":
            cg_name = '763_БСК1_ПРК_C_WSCW_ПОЗ'
        if self._type == "CT":
            cg_name = '763_БСК1_ПРК_C_WSCT_ПОЗ'
        if self._type == "R":
            cg_name = '763_БСК1_ПРК_R_WSRH_ПОЗ'
        if self._type == "T":
            cg_name = '763_БСК1_ПРК_T_WST_ПОЗ'
        row = ''
        row += f'К|Установка переключателя WS{self._type}{self._num} в позицию {self._position}|          |            |     |               |               |        |               ||\n'
        row += f'О|   {num + 1}|          |     ВЫЗВАТЬ|     |               |{cg_name}|        |               ||\n'
        row += f' |    |          |            |  &1 |              {self._num}|               |        |               ||\n'
        row += f' |    |          |            |  &2 |              {self._position}|               |        |               ||\n'
        return [row, num + 1]

    def getCGStrConfig(self, num) -> []:
        row = ''
        return [row, num]

    def getCGStrOn(self, num) -> []:
        row = ''
        return [row, num]

    def isConfigurable(self):
        return False

    def isDevice(self):
        return False

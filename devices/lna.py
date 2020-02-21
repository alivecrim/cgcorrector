import utils.splitters as u
from utils.cg_form import CycleGramGenerator


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

        cg = CycleGramGenerator(num)
        cg.comment([f'Включение МШУ {self._num}'])
        cg.call_('763_БСК1_МШУ_ВКЛ', [self._num])
        cg.pause(1)
        return [cg.all_data, cg.idx.get_value()]

    @staticmethod
    def getCGStrSwitch(num) -> []:
        row = ''
        return [row, num]

    @staticmethod
    def getCGStrConfig(num) -> []:
        row = ''
        return [row, num]

    @staticmethod
    def isConfigurable():
        return False

    @staticmethod
    def isDevice():
        return True

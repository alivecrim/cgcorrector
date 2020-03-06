import utils.splitters as u
from cg_creator.cg_form import CycleGramGenerator


class LNA:
    def __init__(self, definition: list):
        self.num: int = 0
        self._definition = definition
        self._type: str = 'LNA'
        self._fillData()
        self.name = 'L' + str(self.num)

    def _setNum(self):
        self.num = int(u.splitByDigit(self._definition[0])[1]) * 10
        inner_num = int(self._definition[1][-1:] + self._definition[2][-1:])
        if inner_num == 23:
            self.num += 1
        if inner_num == 56:
            self.num += 2
        if inner_num == 89:
            self.num += 3

    def getNum(self):
        return self.num

    def _fillData(self):
        self._setNum()

    def __repr__(self):
        return f'{self._type}{self.num}'

    def getCGStrOn(self, num) -> []:

        cg = CycleGramGenerator(num)
        cg.comment([f'Включение МШУ {self.num}'])
        cg.call_('763_БСК1_МШУ_ВКЛ', [self.num])
        cg.pause(1)
        return [cg.all_data, cg.idx.get_value()]

    def getCGStrOff(self, num) -> []:

        cg = CycleGramGenerator(num)
        cg.comment([f'Отключение МШУ {self.num}'])
        cg.call_('763_БСК1_МШУ_ОТКЛ', [self.num])
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

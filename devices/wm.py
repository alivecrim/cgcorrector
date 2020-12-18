import utils.splitters as u
from cg_creator.cg_form import CycleGramGenerator


class WM:
    def __init__(self, definition: list):
        self.num: int = 0
        self._definition = definition
        self._type: str = 'WM'
        self._fillData()
        self.name = 'WM' + str(self.num)

    def _setNum(self):
        self.num = 1

    def getNum(self):
        return self.num

    def _fillData(self):
        self._setNum()

    def __repr__(self):
        return f'{self._type}{self.num}'

    def getCGStrOn(self, num) -> []:

        cg = CycleGramGenerator(num)
        cg.comment([f'Включение маяка {self.num}'])
        cg.call_('763_БСК1_МАЯК_ВКЛ', [])
        cg.pause(1)
        return [cg.all_data, cg.idx.get_value()]

    def getCGStrOff(self, num) -> []:

        cg = CycleGramGenerator(num)
        cg.comment([f'Отключение маяка {self.num}'])
        cg.call_('763_БСК1_МАЯК_ОТКЛ', [])
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

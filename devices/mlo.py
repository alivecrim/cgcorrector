from cg_creator.cg_form import CycleGramGenerator


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
        if not (self._num == 0):
            cg_name = '763_БСК1_MLO_ВКЛ'
            cg = CycleGramGenerator(num)
            cg.comment(f'Включение MLO {self._num}')
            cg.call_('763_БСК1_MLO_ВКЛ', [self._num])
            cg.pause(1)
            return [cg.all_data, cg.idx.get_value()]
        return ['', num]

    def getCGStrConfig(self, num) -> []:
        row = ''
        return [row, num]

    def isConfigurable(self):
        return False

    def isDevice(self):
        if not (self._num == 0):
            return True
        return False

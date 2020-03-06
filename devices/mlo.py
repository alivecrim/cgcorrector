from cg_creator.cg_form import CycleGramGenerator


class MLO:
    def __init__(self, config: list):
        self.num: int = 0
        self._config = config
        self._fill_data()
        if self.num == 0:
            self.name = '___'
        else:
            self.name = 'ML' + str(self.num)

    def _fill_data(self):
        self._setNum()

    def _setNum(self):
        if self._config['N'] == 1:
            self.num = 1
        if self._config['R'] == 1:
            self.num = 2

    def getNum(self):
        return self.num

    def _getSwitchDef(self):
        if self.num == 1:
            return [['WSCT1', 'J1', 'J2'], ['WSCT2', 'J1', 'J4']]
        if self.num == 2:
            return [['WSCT1', 'J1', 'J4'], ['WSCT2', 'J1', 'J2']]
        return []

    def getCGStrSwitch(self, num) -> []:
        return ['', num]

    def getCGStrOn(self, num) -> []:
        if not (self.num == 0):
            cg = CycleGramGenerator(num)
            cg.comment(f'Включение MLO {self.num}')
            cg.call_('763_БСК1_MLO_ВКЛ', [self.num])
            cg.pause(1)
            return [cg.all_data, cg.idx.get_value()]
        return ['', num]

    def getCGStrOff(self, num) -> []:
        if not (self.num == 0):
            cg = CycleGramGenerator(num)
            cg.comment(f'Отключение MLO {self.num}')
            cg.call_('763_БСК1_MLO_ОТКЛ', [self.num])
            cg.pause(1)
            return [cg.all_data, cg.idx.get_value()]
        return ['', num]

    def getCGStrConfig(self, num) -> []:
        row = ''
        return [row, num]

    def isConfigurable(self):
        return False

    def isDevice(self):
        if not (self.num == 0):
            return True
        return False

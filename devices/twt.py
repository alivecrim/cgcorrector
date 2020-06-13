from cg_creator.cg_form import CycleGramGenerator


class TWT:
    def __init__(self, definition: list, config: list):
        self.num: int = 0
        self._definition = definition
        self._sca = 41
        self._gca = 35
        self._fca = 31
        self._alc = False
        self.type = ''
        self._ab = ''

        self._config = config
        self._fill_data()
        self.name = 'WTW' + str(self.num)

    def _fill_data(self):
        self.extract_steps_from_json()
        self._setNum()

    def getNum(self):
        return self.num

    def _setNum(self):
        if self.type == 'mda':
            self.num = int(self._definition[0][3:4])
            self._ab = ''
        if self.type == 'tas':
            self.num = int(self._definition[0][3:len(self._definition[0]) - 1])
            self._ab = self._definition[0][-1:]

    def extract_steps_from_json(self):
        if (self._config['twta_tas'] != 0 and self._config['twta_mda'] == 0):
            self.type = 'tas'
            try:
                self._fca = self._config['twta_tas']["FCA"]
                self._gca = self._config['twta_tas']["GCA"]
                self._sca = self._config['twta_tas']["SCA"]
                self._alc = self._config['twta_tas']["FGM"]
            except:
                print("Шаги для ТАС указаны, ставим стандартные 15,15,15")
        else:
            self.type = 'mda'
            try:
                self._fca = self._config['twta_mda']["FCA"]
                self._sca = self._config['twta_mda']["SCA"]
                self._alc = self._config['twta_mda']["FGM"]
            except:
                print("Шаги для МДА не указаны, ставим стандартные 15,15,15")
                self._fca = 10
                self._sca = 15

    def __repr__(self):
        return f'{self.type} WTWTA{self.num}'

    # метод ниже для совместимости, используется для переключателей!
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

    def getCGRfOnOff(self, num) -> []:
        row = ''
        setRfOnOffStr = self._setRf(num, 2)
        row += setRfOnOffStr[0]
        num = setRfOnOffStr[1]
        setRfOnOffStr = self._setRf(num, 1)
        row += setRfOnOffStr[0]
        num = setRfOnOffStr[1]

        return [row, num]

    def getCGStrConfig(self, num) -> []:
        row = ''
        par = 0
        if self._alc == 1:
            par = 0
        if self._alc == 0:
            par = 1
        setAlcFgmStr = self._setAlcFgm(num, par)

        row += setAlcFgmStr[0]
        num = setAlcFgmStr[1]

        setFCAStr = self._setStep(num, 1)
        row += setFCAStr[0]
        num = setFCAStr[1]

        if (self.type == 'tas'):
            setGcaStr = self._setStep(num, 2)
            row += setGcaStr[0]
            num = setGcaStr[1]

        setScaStr = self._setStep(num, 3)
        row += setScaStr[0]
        num = setScaStr[1]

        return [row, num]

    def _setStep(self, num, param):
        cg = CycleGramGenerator(num)
        stepName = {
            1: "FCA",
            2: "GCA",
            3: "SCA",
        }
        stepValue = {
            1: self._fca,
            2: self._gca,
            3: self._sca,
        }
        if (self.type == 'tas'):
            sw_on = 0
            if self._ab == 'A':
                sw_on = 1
            if self._ab == 'B':
                sw_on = 2
            cg.comment(f'Установка шага {stepName[param]} {stepValue[param]}')
            cg.call_('763_БСК1_УЛБВ_K_УСТ_ШАГА', [self.num, sw_on, param, stepValue[param]])
            cg.pause(1)
        if (self.type == 'mda'):
            cg.comment(f'Установка шага {stepName[param]} {stepValue[param]}')
            if (param == 1):
                cg.call_('763_БСК1_УЛБВ_Ka_УСТ_ШАГА_АВТО', [self.num, stepValue[param]])
            if (param == 3):
                cg.call_('763_БСК1_УЛБВ_Ka_УСТ_АТТ_АВТО', [self.num, stepValue[param]])
            cg.pause(1)

        return [cg.all_data, cg.idx.get_value()]

    def _setRf(self, num, param):
        cg = CycleGramGenerator(num)
        if param == 1:
            rf_message = 'Запрет ВЧ'
        if param == 2:
            rf_message = 'Разрешение ВЧ'
        cg.message(f'Для включение режима "{rf_message}" нажмите "Да"')
        if (self.type == 'tas'):
            sw_on = 0
            if self._ab == 'A':
                sw_on = 1
            if self._ab == 'B':
                sw_on = 2
            cg.comment(f'Установка {rf_message} WTWTA{self.num} {self._ab}')
            cg.call_('763_БСК1_УЛБВ_K_ВЧ', [self.num, sw_on, param])

        if (self.type == 'mda'):
            cg.comment(f'Установка {rf_message} WTWTA{self.num}M')
            cg.call_('763_БСК1_УЛБВ_Ka_ВЧ', [self.num, param])
        cg.pause(1)

        return [cg.all_data, cg.idx.get_value()]

    def _setAlcFgm(self, num, param):
        cg = CycleGramGenerator(num)
        if (self.type == 'tas'):
            sw_on = 0
            if self._ab == 'A':
                sw_on = 1
            if self._ab == 'B':
                sw_on = 2
            alc_fgm_message = {
                0: "ФРУ",
                1: "АРУ"
            }
            cg.comment(f'Установка режима {alc_fgm_message[param]} WTWTA{self.num} {self._ab}')
            cg.call_('763_БСК1_УЛБВ_K_ФРУ_АРУ', [self.num, sw_on, param])

        if (self.type == 'mda'):
            cg.comment(f'Установка режима ФРУ/АРУ WTWTA{self.num}M')
            cg.call_('763_БСК1_УЛБВ_Ka_ФРУ_АРУ', [self.num, param])
        cg.pause(1)

        return [cg.all_data, cg.idx.get_value()]

    def _switchOn(self, num):
        row = ''
        if self.type == 'mda':
            cg = CycleGramGenerator(num)
            cg.comment(f'Включение УЛБВ WTWTA{self.num}M')
            cg.call_('763_БСК1_УЛБВ_Ka_ВКЛ', [self.num])
            cg.pause(1)
            return [cg.all_data, cg.idx.get_value()]

        if self.type == 'tas':
            cg = CycleGramGenerator(num)
            cg.comment(f'Включение ВИП WTWTA{self.num}')
            cg.call_('763_БСК1_УЛБВ_K_ВКЛ_ВИП', [self.num])
            cg.pause(1)

            sw_on = 0
            cg.comment(f'Включение УЛБВ WTWTA{self.num}{self._ab}')
            if (self._ab == 'A'): sw_on = 1
            if (self._ab == 'B'): sw_on = 2
            cg.call_('763_БСК1_УЛБВ_K_ВКЛ_ОТКЛ', [self.num, sw_on, 0])
            cg.pause(1)
            return [cg.all_data, cg.idx.get_value()]
        return [row, num]

    def _switchOff(self, num):
        row = ''
        if self.type == 'mda':
            cg = CycleGramGenerator(num)
            cg.comment(f'Отключение УЛБВ WTWTA{self.num}M')
            cg.call_('763_БСК1_УЛБВ_Ka_ОТКЛ', [self.num])
            cg.pause(1)
            return [cg.all_data, cg.idx.get_value()]

        if self.type == 'tas':
            cg = CycleGramGenerator(num)

            cg.comment(f'Отключение УЛБВ WTWTA{self.num}{self._ab}')
            cg.call_('763_БСК1_УЛБВ_K_ВКЛ_ОТКЛ', [self.num, 0, 0])
            cg.pause(1)
            cg.comment(f'Отключение ВИП WTWTA{self.num}')
            cg.call_('763_БСК1_УЛБВ_K_ОТКЛ_ВИП', [self.num])
            cg.pause(1)

            return [cg.all_data, cg.idx.get_value()]
        return [row, num]

    def isConfigurable(self):
        return True

    def _isDevice(self):
        return True

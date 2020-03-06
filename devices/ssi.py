import re

import devices.cn as cn
import devices.dtp as dp
import devices.lna as ln
import devices.mlo as ml
import devices.switch as sw
import utils.splitters as u
from cg_creator.cg_form import CycleGramGenerator
from measure.measure import Measure


class SSI:
    def __init__(self, config):
        self.device_list_dict = {
            'conf_num': '',
            'in': '',
            'LNA': '_' * 5,
            'BSK2_CL': '_' * 6,
            'CN_KuC': '_' * 6,
            'CN_CIF': '_' * 6,
            'DTP': '_' * 5,
            'CN_IFS': '_' * 6,
            'CN_SKa': '_' * 6,
            'KKa': '_' * 6,
            'TWT': '_' * 5,
            'out': '_' * 5,
        }
        self.config = config
        self.config_id = self.config['id']
        self.LNA_list = []
        self.CN_list = []
        self.switch_List = []
        self.fullDeviceList = []
        self._fillData()
        self.isInverted = self.config['dtp']['INV'] == 1

        self.nameForSwitch = '763_БСК1_ПРК_' + self.config['route_short_name']
        self.nameForDevice = '763_БСК1_ПРБ_' + self.config['route_short_name']
        self.nameForDeviceOff = '763_БСК1_ПРБ_ОТКЛ_' + self.config['route_short_name']
        self.nameForAll = "763_БСК1_ВХ" + str(self.config_id)
        self.nameForConfigDevice = "763_БСК1_КНФ_" + str(self.config_id)

        num_prefix = {
            len(str(self.config_id)) == 1: '00',
            len(str(self.config_id)) == 2: '0',
            len(str(self.config_id)) == 3: '',
        }[True]
        get_num = num_prefix + str(self.config_id)

        route_name = self._short_name_modify(self.config['route_short_name'])
        # -----------------------------------------
        self.device_list_dict['conf_num'] = get_num
        self.device_list_dict['conf_num'] = get_num

        self.nameForMeasure = "763_БСК1_ИЗМЕР_" + get_num
        self.measure = Measure(self.config, self.nameForMeasure, self)

    def _short_name_modify(self, sh_name: str):

        if re.findall(r'WLNA\d-J\d', sh_name):
            sh_name = sh_name.replace(re.findall(r'WLNA\d-J\d', sh_name)[0], self.device_list_dict['LNA'])

        if re.findall(r'W1CN\d', sh_name):
            sh_name = sh_name.replace(re.findall(r'W1CN\d', sh_name)[0], self.device_list_dict['CN_KuC'])
        if re.findall(r'W2CN\d', sh_name):
            sh_name = sh_name.replace(re.findall(r'W2CN\d', sh_name)[0], self.device_list_dict['CN_LC'])
        if re.findall(r'W3CN\d', sh_name):
            sh_name = sh_name.replace(re.findall(r'W3CN\d', sh_name)[0], self.device_list_dict['CN_CIF'])
        if re.findall(r'W4CN\d', sh_name):
            sh_name = sh_name.replace(re.findall(r'W4CN\d', sh_name)[0], self.device_list_dict['CN_IFS'])
        if re.findall(r'W5CN\d', sh_name):
            sh_name = sh_name.replace(re.findall(r'W5CN\d', sh_name)[0], self.device_list_dict['CN_SKa'])
        if re.findall(r'W6CN\d', sh_name):
            sh_name = sh_name.replace(re.findall(r'W6CN\d', sh_name)[0], self.device_list_dict['CN_KKa'])
        if re.findall(r'WDTP1-J\d{2,3}_WDTP1-J\d\d', sh_name):
            sh_name = sh_name.replace(re.findall(r'WDTP1-J\d{2,3}_WDTP1-J\d\d', sh_name)[0],
                                      self.device_list_dict['DTP'])

        if re.findall(r'-J\d{1,3}', sh_name):
            sh_name = sh_name.replace(re.findall(r'-J\d{1,3}', sh_name)[0], '')

        return sh_name

    def get_outFreq(self):
        full_lo = 0
        for cn in self.CN_list:
            full_lo += cn._lo
        if self.dtp is not None:
            full_lo += -320

        return full_lo

    def _fillData(self):
        self.Mlo = ml.MLO(self.config['mlo'])
        self.dtp = None
        for r in self.config['route']:
            if u.splitByDigit(r[0])[0] in ['WSC', 'WSA', 'WSCT', 'WST', 'WSR']:
                self._fill_switch(r)
            if u.splitByDigit(r[0])[0] in ['WLNA']:
                self._fill_lna(r)
            if re.findall(r'W\dCN\d', r[0]):
                self._fill_cn(r, self.config)
            if re.findall(r'WDTP1', r[0]):
                self._fill_dtp(r, self.config)

        self._makeFullDeviceList()
        self._config_parse()

    def _config_parse(self):
        pass

    def _fill_switch(self, r):
        self.switch_List.append(sw.Switch(r))

    def _fill_lna(self, r):
        self.LNA_list.append(ln.LNA(r))

    def _fill_cn(self, r, config):
        self.CN_list.append(cn.CN(r, config))

    def _fill_dtp(self, r, config):
        self.dtp = dp.DTP(r, config)

    def _fill_twt(self, r, config):
        # TODO
        raise NotImplementedError

    def getFullCGStrSwitch(self) -> str:
        cg = CycleGramGenerator(0)
        cg.program(self.nameForSwitch)

        for item in self.fullDeviceList:
            res = item.getCGStrSwitch(cg.idx.get_value())
            if res != '':
                cg.add_to_all_data(res[0])
                cg.idx.set_value(res[1])

        cg.message('Оператору проверить установку переключателей переключатели')
        cg.program_end()
        return cg.all_data

    def getFullCGStrDEV(self) -> str:
        cg = CycleGramGenerator(0)
        if self._isDevice():
            cg.program(self.nameForDevice)
            for item in self.fullDeviceList:
                res = item.getCGStrOn(cg.idx.get_value())
                if res != '':
                    cg.add_to_all_data(res[0])
                    cg.idx.set_value(res[1])

            cg.message('Оператору проверить включенное оборудование')
            cg.program_end()
            return cg.all_data
        return None

    def getFullCGStrDEV_off(self) -> str:
        cg = CycleGramGenerator(0)
        if self._isDevice():
            cg.program(self.nameForDevice)
            cg.repeat(1, 32000)
            cg.menu([
                'Отключить включенное оборудование',
                'Отключить включенное оборудование кроме DTP и MLO',
                'Не отключать включенное оборудование',
            ])
            cg.select_()
            cg.select_var(1)

            for item in self.fullDeviceList:
                res = item.getCGStrOff(cg.idx.get_value())
                if res != '':
                    cg.add_to_all_data(res[0])
                    cg.idx.set_value(res[1])

            cg.message('Оператору проверить отключение оборудование')
            cg.select_var(2)
            for item in self.fullDeviceList:
                if not isinstance(item, (dp.DTP, ml.MLO)):
                    res = item.getCGStrOff(cg.idx.get_value())
                    if res != '':
                        cg.add_to_all_data(res[0])
                        cg.idx.set_value(res[1])
            cg.message('Оператору проверить отключение оборудование')
            cg.select_var(3)
            cg.exit()
            cg.select_end()
            cg.repeat_end()
            cg.program_end()
            return cg.all_data
        return None

    def getFullCGStrConfigDevice(self) -> str:
        cg = CycleGramGenerator(0)
        if self._isExistConfigDevice():
            cg.program(self.nameForConfigDevice)
            for item in self.fullDeviceList:
                res = item.getCGStrConfig(cg.idx.get_value())
                if res != '':
                    cg.add_to_all_data(res[0])
                    cg.idx.set_value(res[1])
            cg.message('Оператору проверить установленную конфигурацию оборудования')
            cg.program_end()
            return cg.all_data
        return None

    def getFullCGStrMeasure(self) -> str:

        return self.measure.getCGStr()

    def getFullCGStr(self) -> str:
        cg = CycleGramGenerator(0)
        cg.program(self.nameForAll)

        # Call CG for switch
        cg.call_(self.nameForSwitch)

        # Call CG for device On
        if self._isDevice():
            cg.call_(self.nameForDevice)

        # Call CG for device config
        if self._isExistConfigDevice():
            cg.call_(self.nameForConfigDevice)

        # Call CG for measures
        cg.call_(self.nameForMeasure)

        # Call CG for device On
        if self._isDevice():
            cg.call_(self.nameForDeviceOff)
        cg.program_end()
        return cg.all_data

    def _makeFullDeviceList(self):
        self.fullDeviceList.extend(self.switch_List)
        self.fullDeviceList.extend(self.LNA_list)
        self.fullDeviceList.extend(self.CN_list)
        self.fullDeviceList.append(self.Mlo)
        if self.dtp is not None:
            self.fullDeviceList.append(self.dtp)

        self.fill_ssi_dict()

    def fill_ssi_dict(self):
        for item in self.fullDeviceList:
            if isinstance(item, ml.MLO):
                self.device_list_dict['MLO'] = 'M' + item.name
            if isinstance(item, dp.DTP):
                self.device_list_dict['DTP'] = item.name + str(item._inputPort) + str(item._outputPort)
            if isinstance(item, cn.CN):
                if item.type == 'KuC':
                    self.device_list_dict['CN_KuC'] = 'CN' + str(item.num)
                if item.type == 'LC':
                    self.device_list_dict['CN_LC'] = 'CN' + str(item.num)
                if item.type == 'CIF':
                    self.device_list_dict['CN_CIF'] = 'CN' + str(item.num)
                if item.type == 'IFS':
                    self.device_list_dict['CN_IFS'] = 'CN' + str(item.num)
                if item.type == 'SKa':
                    self.device_list_dict['CN_SKa'] = 'CN' + str(item.num)
                if item.type == 'KKa':
                    self.device_list_dict['CN_KKa'] = 'CN' + str(item.num)
            if isinstance(item, ln.LNA):
                self.device_list_dict['LNA'] = 'LN' + str(item.num)

    def _isExistConfigDevice(self) -> bool:
        for device in self.fullDeviceList:
            if device.isConfigurable():
                return True
        return False

    def _isDevice(self) -> bool:
        for device in self.fullDeviceList:
            if device.isDevice():
                return True
        return False

    def getPlan(self) -> str:
        if self.config['id'] < 71:
            filename = '763_ВХСЕК1'
        elif self.config['id'] < 162:
            filename = '763_ВХСЕК2'
        elif self.config['id'] < 172:
            filename = '763_ВХСЕК3'
        elif self.config['id'] < 187:
            filename = '763_ВХСЕК4'
        elif self.config['id'] >= 187:
            filename = '763_ВХСЕК5'
        else:
            filename = '763_ВХСЕКXXXXX'
        return {'filename': filename,
                'planstr': f'Конфигурация {self.config_id}={self.nameForAll}.ci'
                }

    def __str__(self):
        return str(self.config_id) + ' ' + self.config['route_short_name']

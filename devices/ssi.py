import re

import devices.cn as cn
import devices.dtp as dp
import devices.lna as ln
import devices.mlo as ml
import devices.switch as sw
import utils.splitters as u
from measure.measure import Measure


class SSI:
    def __init__(self, config, id_config):
        self.config = config
        self.config_id = id_config
        self.LNA_list = []
        self.CN_list = []
        self.switch_List = []
        self.fullDeviceList = []
        self.nameForSwitch = '763_БСК1_ПРК_' + self.config['route_short_name']
        self.nameForDevice = '763_БСК1_ПРБ_' + self.config['route_short_name']
        self.configurationNameFormat()

        self.nameForAll = "763_БСК1_ВХ_" + str(id_config)
        self._fillData()
        self.isInverted = self.config['dtp']['INV'] == 1
        self.nameForMeasure = "763_БСК1_ИЗМЕР_" + str(id_config)
        self.measure = Measure(self.config, self.nameForMeasure, self)

    def configurationNameFormat(self):
        self.nameForConfigDevice = "763_БСК1_КНФ_" + ('CIF' + self.config['config_name'].split('CIF')[1]).replace('@',
                                                                                                                  '_')
        self.nameForConfigDevice = self.nameForConfigDevice.replace('CIF_-', '')
        self.nameForConfigDevice = self.nameForConfigDevice.replace('_SKA_', '_')
        self.nameForConfigDevice = self.nameForConfigDevice.replace('_KKA_', '_')
        self.nameForConfigDevice = self.nameForConfigDevice.replace('_MLO_00_', '_M0')
        self.nameForConfigDevice = self.nameForConfigDevice.replace('_MLO_10_', '_M1')
        self.nameForConfigDevice = self.nameForConfigDevice.replace('_MLO_01_', '_M2')
        self.nameForConfigDevice = self.nameForConfigDevice.replace('DTP_', '_D')
        self.nameForConfigDevice = self.nameForConfigDevice.replace('.0', '')
        self.nameForConfigDevice = self.nameForConfigDevice[:len(self.nameForConfigDevice) - 10] + str(
            int(self.nameForConfigDevice[-10:], 2))

    def _fillData(self):
        self.Mlo = ml.MLO(self.config['mlo'])
        if self.Mlo._num != 0:
            self.config['route'].extend(self.Mlo._getSwitchDef())
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
        current_num = 0
        fullStr: str = f'О|   {current_num + 1}|          |     ПРОГРАМ|     |{self.nameForSwitch}|               |        |               ||READY\n'
        current_num += 1
        for item in self.fullDeviceList:
            res = item.getCGStrSwitch(current_num)
            if res != '':
                fullStr += res[0]
                current_num = res[1]

        current_num += 1
        fullStr += \
            f'О|  {current_num}|          |      ДИРЕКТ|     |               |               |        |               ||\n' + \
            f'Ф| Оператору проверить установку переключателей переключатели\n'

        fullStr += f'О|   {current_num + 1}|          |    КПРОГРАМ|     |               |               |        |               ||\n'
        return fullStr

    def getFullCGStrDEV(self) -> str:
        current_num = 0
        if self._isDevice():
            fullStr: str = f'О|   {current_num + 1}|          |     ПРОГРАМ|     |{self.nameForDevice}|               |        |               ||READY\n'
            current_num += 1
            for item in self.fullDeviceList:
                res = item.getCGStrOn(current_num)
                if res != '':
                    fullStr += res[0]
                    current_num = res[1]

            current_num += 1
            fullStr += \
                f'О|  {current_num}|          |      ДИРЕКТ|     |               |               |        |               ||\n' + \
                f'Ф| Оператору проверить включенное оборудование\n'
            fullStr += f'О|   {current_num + 1}|          |    КПРОГРАМ|     |               |               |        |               ||\n'
            return fullStr
        return None

    def getFullCGStrConfigDevice(self) -> str:
        current_num = 0
        if self._isExistConfigDevice():
            fullStr: str = f'О|   {current_num + 1}|          |     ПРОГРАМ|     |{self.nameForConfigDevice}|               |        |               ||READY\n'
            current_num += 1
            for item in self.fullDeviceList:
                res = item.getCGStrConfig(current_num)
                if res != '':
                    fullStr += res[0]
                    current_num = res[1]

            current_num += 1
            fullStr += \
                f'О|  {current_num}|          |      ДИРЕКТ|     |               |               |        |               ||\n' + \
                f'Ф| Оператору проверить установленную конфигурацию оборудования\n'
            fullStr += f'О|   {current_num + 1}|          |    КПРОГРАМ|     |               |               |        |               ||\n'
            return fullStr
        return None

    def getFullCGStrMeasure(self) -> str:

        return self.measure.getCGStr()

    def getFullCGStr(self) -> str:
        current_num = 1
        fullStr: str = f'О|   {current_num}|          |     ПРОГРАМ|     |{self.nameForAll}|               |        |               ||READY\n'

        # Call CG for switch
        cg_name = self.nameForSwitch
        current_num += 1
        fullStr += f'О|   {current_num}|          |     ВЫЗВАТЬ|     |               |{cg_name}|        |               ||\n'

        # Call CG for device On
        if self._isDevice():
            cg_name = self.nameForDevice
            current_num += 1
            fullStr += f'О|   {current_num}|          |     ВЫЗВАТЬ|     |               |{cg_name}|        |               ||\n'

        # Call CG for device config
        if self._isExistConfigDevice():
            cg_name = self.nameForConfigDevice
            current_num += 1
            fullStr += f'О|   {current_num}|          |     ВЫЗВАТЬ|     |               |{cg_name}|        |               ||\n'
        # Call CG for measures

        cg_name = self.nameForMeasure
        current_num += 1
        fullStr += f'О|   {current_num}|          |     ВЫЗВАТЬ|     |               |{cg_name}|        |               ||\n'

        current_num += 1
        fullStr += f'О|   {current_num}|          |    КПРОГРАМ|     |               |               |        |               ||\n'
        return fullStr

    def _makeFullDeviceList(self):
        self.fullDeviceList.extend(self.switch_List)
        self.fullDeviceList.extend(self.LNA_list)
        self.fullDeviceList.extend(self.CN_list)
        self.fullDeviceList.append(self.Mlo)
        if self.dtp is not None:
            self.fullDeviceList.append(self.dtp)

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
        if self.config['id'] < 126:
            filename = '763_ВХСЕК1'
        elif self.config['id'] < 162:
            filename = '763_ВХСЕК2'
        elif self.config['id'] < 172:
            filename = '763_ВХСЕК3'
        elif self.config['id'] < 187:
            filename = '763_ВХСЕК4'
        elif self.config['id'] < 243:
            filename = '763_ВХСЕК5'
        else:
            filename = '763_ВХСЕКXXXXX'
        return {'filename': filename,
                'planstr': f'Конфигурация {self.config_id}={self.nameForAll}.ci'
                }

    def __str__(self):
        return str(self.config_id) + ' ' + self.config['route_short_name']

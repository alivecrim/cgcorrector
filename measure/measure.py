import re
from typing import Dict

from cg_creator.cg_form import CycleGramGenerator
from measure.csa_dict import CSA_dict


def cable_maker(s: str):
    if s[0].isdigit():
        return 'C' + s
    return s


def get_im3_keys(CSANAME=None, AVERNUMPNA=None, FIXDELF=None, IFBMMT=None, IFBWIM=None, IFBWPNA=None, IM3OR5=None,
                 POINTNUMPNA=None, SMOOTHNUM=None, ISQRANGE=None, SPANPNA=None):
    return {
        'CSANAME': CSANAME,
        'AVERNUMPNA': AVERNUMPNA,
        'FIXDELF': FIXDELF,
        'IFBMMT': IFBMMT,
        'IFBWIM': IFBWIM,
        'IFBWPNA': IFBWPNA,
        'IM3OR5': IM3OR5,
        'POINTNUMPNA': POINTNUMPNA,
        'SMOOTHNUM': SMOOTHNUM,
        'SPANPNA': SPANPNA,
    }


def get_pn_keys(CSANAME=None):
    return {
        'CSANAME': CSANAME,
    }


def get_afc_gd_keys(CSANAME=None, AVERNUMPNA=None, IFBWPNA=None, MDELAY=None, POINTNUMPNA=None, SMOOTHNUM=None,
                    SPANPNA=None):
    return {
        'CSANAME': CSANAME,
        'AVERNUMPNA': AVERNUMPNA,
        'IFBWPNA': IFBWPNA,
        'MDELAY': MDELAY,
        'POINTNUMPNA': POINTNUMPNA,
        'SMOOTHNUM': SMOOTHNUM,
        'SPANPNA': SPANPNA,
    }


def get_sp_keys(CSANAME, AVERNUMPNA, IFBWPNA, MDELAY, POINTNUMPNA, SMOOTHNUM, SPANPNA, POWOFFSET, STARPOW, STOPPOW,
                COMPEXCEED):
    return {
        'CSANAME': CSANAME,
        'AVERNUMPNA': AVERNUMPNA,
        'IFBWPNA': IFBWPNA,
        'MDELAY': MDELAY,
        'POINTNUMPNA': POINTNUMPNA,
        'SMOOTHNUM': SMOOTHNUM,
        'SPANPNA': SPANPNA,
        'POWOFFSET': POWOFFSET,
        'COMPEXCEED': COMPEXCEED,
        'STARPOW': STARPOW,
        'STOPPOW': STOPPOW
    }


def get_amam_keys(CSANAME, AVERNUMPNA, IFBWPNA, MDELAY, POINTNUMPNA, SMOOTHNUM, SPANPNA):
    return {
        'CSANAME': CSANAME,
        'AVERNUMPNA': AVERNUMPNA,
        'IFBWPNA': IFBWPNA,
        'MDELAY': MDELAY,
        'POINTNUMPNA': POINTNUMPNA,
        'SMOOTHNUM': SMOOTHNUM,
        'SPANPNA': SPANPNA,
    }


def get_dpm_keys(CSANAME, IFBW100HZ, IFBW1KHZ, IFBW10KHZ, IFBW100KHZ, IFBW1MHZ, IFBW10MHZ):
    return {
        'CSANAME': CSANAME,
        'IFBW100HZ': IFBW100HZ,
        'IFBW1KHZ': IFBW1KHZ,
        'IFBW10KHZ': IFBW10KHZ,
        'IFBW100KHZ': IFBW100KHZ,
        'IFBW1MHZ': IFBW1MHZ,
        'IFBW10MHZ': IFBW10MHZ,
    }


def get_lo_keys(CSANAME):
    return {
        'CSANAME': CSANAME,
    }


class Measure:
    def __init__(self, config, nameOfCg, ssi):
        self.ssi = ssi
        self.config = config
        self._numberOfMeasurePoints = 801
        self._isConverted = self._getIsConverted()
        self._powerIn = self.config['power_in']
        self._powerIn_coma = str(self._powerIn).replace('.', ',')
        self.bw = int(self.config['bw'])
        # self.frequencyInCenter = int(self.config['calc_set_config']['frequency_start'] + (self.bw / 2))
        self.frequencyInCenter = int(self.config['frequency_start']) + (self.bw / 2)
        # self.frequencyOutCenter = abs((self.frequencyInCenter - ssi.get_outFreq()))
        self.frequencyOutCenter = config["frequency_out"] + self.bw / 2 if not (
                    config["frequency_out"] is None) else abs((self.frequencyInCenter - ssi.get_outFreq()))
        self.powerLevel = self.config['power_level']
        self.calibrationFileNameMain = self._getCalibrationFileName()
        self.nameOfCg = nameOfCg

    def _getIsConverted(self) -> bool:
        if re.findall(r'W\dCN\d', self.config['route_long_name']):
            return True
        else:
            return False

    def _getCalibrationFileName(self) -> str:

        stage = {
            self.config['id'] < 72: "Input_section_1\\",
            72 <= self.config['id'] < 162: "Input_section_2\\",
            162 <= self.config['id'] < 172: "Input_section_3\\",
            172 <= self.config['id'] < 187: "Input_section_4\\",
            self.config['id'] >= 187: "Input_section_5\\",
            self.config['id'] >= 300: "RSRE_1\\",
            self.config['id'] >= 500: "ETE\\",
            self.config['id'] >= 1000: "ETE_X\\",
        }
        cm = cable_maker
        if self.config['id'] == 171:
            print('test')
        try:
            if not self._isConverted:
                return f"{stage[True]}{cm(self.config['route'][0][0])}_" \
                       f"{int(self.config['calc_set_config']['frequency_start'])}_" \
                       f"{int(self.config['calc_set_config']['frequency_start'] + self.bw)}_" \
                       f"@MEAS@_{self.config['power_level']}"
            else:
                return f"{stage[True]}{cm(self.config['route'][0][0])}_" \
                       f"{int(self.frequencyInCenter)}_" \
                       f"{int(self.frequencyOutCenter)}_" \
                       f"{int(self.config['bw'])}_@MEAS@_{self.powerLevel}"
        except Exception:
            print("Dont_work" + self.config['id'])

    def _get_calibration_file_name_measure(self, measureName) -> str:
        suf: str = ''
        if self.config['dtp']['INV'] == 1:
            suf = '_inv'

        config_id = self.config['id']
        try:
            CSA_dict[config_id]
        except:
            return self.calibrationFileNameMain.replace('@MEAS@', measureName) + suf
        return 'ETE_X\\' + CSA_dict[config_id] + measureName

    def _get_dtp_config_string(self):
        dtp_config = self.config["dtp"]
        on_dtp = {
            dtp_config['TC_N'] == 1 and dtp_config['TC_R'] == 0: 'DTP: GEST_N ВКЛЮЧЕН',
            dtp_config['TC_N'] == 0 and dtp_config['TC_R'] == 1: 'DTP: GEST_R ВКЛЮЧЕН',
            dtp_config['TC_R'] == 0 and dtp_config['TC_N'] == 0: 'DTP: GEST_N ОТКЛЮЧЕН, GEST_R ОТКЛЮЧЕН',
        }[True]
        BIBO1 = {
            dtp_config['B1'] == 0: 'BIBO1: ОТКЛЮЧЕН',
            dtp_config['B1'] == 1: 'BIBO1: ВКЛЮЧЕН',
        }[True]
        BIBO2 = {
            dtp_config['B2'] == 0: 'BIBO2: ОТКЛЮЧЕН',
            dtp_config['B2'] == 1: 'BIBO2: ВКЛЮЧЕН',
        }[True]
        BIBO3 = {
            dtp_config['B3'] == 0: 'BIBO3: ОТКЛЮЧЕН',
            dtp_config['B3'] == 1: 'BIBO3: ВКЛЮЧЕН',
        }[True]
        BIBO4 = {
            dtp_config['B4'] == 0: 'BIBO4: ОТКЛЮЧЕН',
            dtp_config['B4'] == 1: 'BIBO4: ВКЛЮЧЕН',
        }[True]

        return on_dtp + '|' + BIBO1 + '|' + BIBO2 + '|' + BIBO3 + '|' + BIBO4

    def _get_config_long_name_list(self):
        counter = 0
        list_long_config = []
        item = ''
        for i in 'ПУТЬ: ' + self.config["route_long_name"]:
            if counter < 100:
                item += i
                counter += 1
            else:
                list_long_config.append(item)
                counter = 0
                item = i
        return list_long_config

    def getCGStr(self, ssi):
        cg = CycleGramGenerator(0)
        cg.program(self.nameOfCg)

        path_config = self._get_config_long_name_list()
        dtp_config = self._get_dtp_config_string().split('|')
        config_config = f'{self.config["config_name"]}'
        main_comment = []
        main_comment.extend(path_config)
        main_comment.append('КОНФИГУРАЦИЯ: ' + config_config)
        main_comment.extend(dtp_config)

        cg.comment(main_comment)
        AB_test = {'A': 1, 'B': 2, '': 3}
        cg.call_('763_БСК1_ОПРЕД_УЛБВ', [self.ssi.TWT_list[0].num, AB_test[self.ssi.TWT_list[0]._ab]])
        cg.compute([
            ['SSI', '=', f'"{self.nameOfCg}"']
        ])
        cg.repeat(1, 32000)
        cg.comment('Общие для всех измерений ключи')
        cg.compute([
            ['FRINCENT', '=', self.frequencyInCenter],
            ['POWIN', '=', self._powerIn_coma],
            ['FROUTCENT', '=', self.frequencyOutCenter],
            ['POWOUT', '=', -20],
        ])

        cg.comment('Выбор измерения')

        cg.menu([
            'Измерение ТН_НУ',
            'Измерение АМАМ',
            'Измерение АЧХ',
            'Измерение АЧХ_Н',
            'Измерение НГВЗ',
            'Измерение ИМ_3',
            'Измерение ФШ',
            'Измерение ЧП',
            'Измерение ДПМ',
            'Измерение АРУ',
            'Выход',
        ])
        cg.select_()
        self._measure_insert(cycl_gen=cg, num_of_meas=1, name_of_meas='ТН_НУ', keys_of_measure=get_sp_keys(
            CSANAME=f'"{self._get_calibration_file_name_measure("AFC")}"',
            AVERNUMPNA=5,
            IFBWPNA=1000,
            MDELAY=0,
            POINTNUMPNA=self._numberOfMeasurePoints,
            SMOOTHNUM=2,
            SPANPNA=10,
            POWOFFSET=0.01,
            STARPOW=self._powerIn - 3,
            STOPPOW=self._powerIn + 2,
            COMPEXCEED=3,
        ), ssi=ssi)
        self._measure_insert(cycl_gen=cg, num_of_meas=2, name_of_meas='ТН_ВУ', keys_of_measure=get_amam_keys(
            CSANAME=f'"{self._get_calibration_file_name_measure("AFC")}"',
            AVERNUMPNA=5,
            IFBWPNA=1000,
            MDELAY=0,
            POINTNUMPNA=self._numberOfMeasurePoints,
            SMOOTHNUM=2,
            SPANPNA=10,
        ), ssi=ssi)
        self._measure_insert(cycl_gen=cg, num_of_meas=3, name_of_meas='АЧХ', keys_of_measure=get_afc_gd_keys(
            CSANAME=f'"{self._get_calibration_file_name_measure("AFC")}"',
            AVERNUMPNA=5,
            IFBWPNA=1000,
            MDELAY=0,
            POINTNUMPNA=self._numberOfMeasurePoints,
            SMOOTHNUM=2,
            SPANPNA=self.bw,
        ), ssi=ssi)
        self._measure_insert(cycl_gen=cg, num_of_meas=4, name_of_meas='АЧХ_Н', keys_of_measure=get_afc_gd_keys(
            CSANAME=f'"{self._get_calibration_file_name_measure("AFC")}"',
            AVERNUMPNA=5,
            IFBWPNA=1000,
            MDELAY=0,
            POINTNUMPNA=self._numberOfMeasurePoints,
            SMOOTHNUM=2,
            SPANPNA=round(self.bw * 0.27),
        ), ssi=ssi)
        self._measure_insert(cycl_gen=cg, num_of_meas=5, name_of_meas='НГВЗ', keys_of_measure=get_afc_gd_keys(
            CSANAME=f'"{self._get_calibration_file_name_measure("GD")}"',
            AVERNUMPNA=30,
            IFBWPNA=1000,
            MDELAY=0,
            POINTNUMPNA=self._numberOfMeasurePoints - 400,
            SMOOTHNUM=5,
            SPANPNA=self.bw,
        ), ssi=ssi)

        self._measure_insert(cycl_gen=cg, num_of_meas=6, name_of_meas='ИМ_3', keys_of_measure=get_im3_keys(
            CSANAME=f'"{self._get_calibration_file_name_measure("IMD")}"',
            AVERNUMPNA=5,
            FIXDELF=1,
            IFBMMT=10000,
            IFBWIM=10000,
            IFBWPNA=1000,
            IM3OR5=0,
            POINTNUMPNA=41,
            SMOOTHNUM=5,
            SPANPNA=24,
        ), ssi=ssi)
        self._measure_insert(cycl_gen=cg, num_of_meas=7, name_of_meas='Ф_Ш', keys_of_measure=get_pn_keys(
            CSANAME=f'"{self._get_calibration_file_name_measure("PN")}"',
        ), ssi=ssi)
        self._measure_insert(cycl_gen=cg, num_of_meas=8, name_of_meas='ЧП', keys_of_measure=get_lo_keys(
            CSANAME=f'"{self._get_calibration_file_name_measure("PN")}"',
        ), ssi=ssi)
        self._measure_insert(cycl_gen=cg, num_of_meas=9, name_of_meas='ДПМ', keys_of_measure=get_dpm_keys(
            CSANAME=f'"{self._get_calibration_file_name_measure("PN")}"',
            IFBW100HZ=5,
            IFBW1KHZ=15,
            IFBW10KHZ=100,
            IFBW100KHZ=100,
            IFBW1MHZ=2000,
            IFBW10MHZ=10000,
        ), ssi=ssi)
        self._measure_insert(cycl_gen=cg, num_of_meas=10, name_of_meas='АРУ', keys_of_measure=get_afc_gd_keys(
            CSANAME=f'"{self._get_calibration_file_name_measure("AFC")}"',
            AVERNUMPNA=5,
            IFBWPNA=1000,
            MDELAY=0,
            POINTNUMPNA=self._numberOfMeasurePoints,
            SMOOTHNUM=2,
            SPANPNA=self.bw,
        ), ssi=ssi)
        cg.select_var(11)

        cg.exit()
        cg.select_end()
        cg.repeat_end()
        cg.program_end()

        return cg.all_data

    # @staticmethod
    def _measure_insert(self, cycl_gen: CycleGramGenerator, num_of_meas: int, name_of_meas: str, keys_of_measure: Dict,
                        ssi):
        keys_list = []
        for k in keys_of_measure:
            if not (keys_of_measure[k] is None):
                keys_list.append([k, '=', keys_of_measure[k]])
        cycl_gen.select_var(num_of_meas)
        self.rf_setMode(cycl_gen, ssi)
        self.rf_on(cycl_gen, ssi)
        cycl_gen.comment(f'персональные ключи для {name_of_meas}')
        cycl_gen.compute(keys_list)
        cycl_gen.call_(name_of_meas)
        self.rf_off(cycl_gen, ssi)

    def rf_on(self, cg, ssi):
        cg.comment("Включение ВЧ на текущей лампе")
        try:
            if ssi.TWT_list[0].type == 'mda':
                cg.call_("763_БСК1_УЛБВ_Ka_ВЧ", [ssi.TWT_list[0].num, 2])
            elif ssi.TWT_list[0].type == 'tas':
                cg.call_("763_БСК1_УЛБВ_K_ВЧ", [ssi.TWT_list[0].num, ssi.TWT_list[0].getAB(), 2])
        except:
            print('stop')

    def rf_off(self, cg, ssi):
        cg.comment("Отключение ВЧ на текущей лампе")
        if ssi.TWT_list[0].type == 'mda':
            cg.call_("763_БСК1_УЛБВ_Ka_ВЧ", [ssi.TWT_list[0].num, 1])
        elif ssi.TWT_list[0].type == 'tas':
            cg.call_("763_БСК1_УЛБВ_K_ВЧ", [ssi.TWT_list[0].num, ssi.TWT_list[0].getAB(), 1])

    def rf_setMode(self, cg, ssi):
        cg.call_("763_БСК1_УЛБВ_ЗАПРОС_ШАГА")

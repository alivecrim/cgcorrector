from cg_creator.cg_form import CycleGramGenerator
from devices.twt import TWT


class Outgas:
    def __init__(self, nameForDegas):
        self.cgName = nameForDegas

    def _rf_on(self, cg, ssi):
        cg.comment("Включение ВЧ на текущей лампе")
        try:
            if ssi.TWT_list[0].type == 'mda':
                cg.call_("763_БСК1_УЛБВ_Ka_ВЧ", [ssi.TWT_list[0].num, 2])
            elif ssi.TWT_list[0].type == 'tas':
                cg.call_("763_БСК1_УЛБВ_K_ВЧ", [ssi.TWT_list[0].num, ssi.TWT_list[0].getAB(), 2])
        except:
            print('stop')

    def _rf_off(self, cg, ssi):
        cg.comment("Отключение ВЧ на текущей лампе")
        if ssi.TWT_list[0].type == 'mda':
            cg.call_("763_БСК1_УЛБВ_Ka_ВЧ", [ssi.TWT_list[0].num, 1])
        elif ssi.TWT_list[0].type == 'tas':
            cg.call_("763_БСК1_УЛБВ_K_ВЧ", [ssi.TWT_list[0].num, ssi.TWT_list[0].getAB(), 1])

    def _rf_setMode(self, cg, ssi):
        cg.call_("763_БСК1_УЛБВ_ЗАПРОС_ШАГА")

    def _setStep(self, twt: TWT, step: int, step_type: int, cgg=None):
        cg = cgg
        step_name = {
            1: "FCA",
            2: "GCA",
            3: "SCA",
        }
        if (twt.type == 'tas'):
            twt_ab = 0
            if twt._ab == 'A':
                twt_ab = 1
            if twt._ab == 'B':
                twt_ab = 2
            cg.comment(f'Установка шага {step_name[step_type]} {step}')
            cg.call_('763_БСК1_УЛБВ_K_УСТ_ШАГА', [twt.num, twt_ab, step_type, step])
            cg.pause(1)

        if (twt.type == 'mda'):
            cg.comment(f'Установка шага {step_name[step_type]} {step}')
            if (step_type == 1):
                cg.call_('763_БСК1_УЛБВ_Ka_УСТ_ШАГА_АВТО', [twt.num, step])
            if (step_type == 3):
                cg.call_('763_БСК1_УЛБВ_Ka_УСТ_АТТ_АВТО', [twt.num, step])
            cg.pause(1)

    def getOutgasItem(self, ssi):
        minutes = [5 * 60, 5 * 60, 20 * 60, 20 * 60, 30 * 60, 30 * 60]
        AB_test = {'A': 1, 'B': 2, '': 3}
        twt = ssi.TWT_list[0]
        cg = CycleGramGenerator(0)
        cg.program(self.cgName)
        cg.call_('763_БСК1_ОПРЕД_УЛБВ', [ssi.TWT_list[0].num, AB_test[ssi.TWT_list[0]._ab]])
        cg.comment("Программа дегазации конфигурации " + str(ssi.config_id))
        cg.message("Оператор! Проверь, что лампа в режиме АРУ!")
        self._setStep(twt, 80, 1, cg)

        self._rf_on(cg, ssi)
        for (idx, m) in enumerate(minutes):
            cg.message("Приступить к шагу дегазации " + str(idx + 1) + "?")
            # self._setStep(twt, step_type=2, step=1, cgg=cg)
            cg.call_("763_БСК1_УЛБВ_ЗАПРОС_ШАГА")
            cg.pause(m)
            cg.message("Перейти на следующий шаг?")
        cg.message("Дегазация завершена! Режим OVERDRIVE")
        cg.call_("763_БСК1_УЛБВ_ЗАПРОС_ШАГА")

        cg.message("Отключить ВЧ на УЛБВ?")
        self._rf_off(cg, ssi)
        cg.program_end()

        return cg.all_data

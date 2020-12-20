import os
from typing import List

from cg_creator.cg_form import CycleGramGenerator
from devices import ssi


def clear_output():
    output_path = './servicedata/output/'
    switch_path = 'ПРК/'
    device_path = 'ОБОРУД/'
    config_path = 'КОНФИГУРАЦИЯ/'
    plan_path = 'ПЛАНЫ/'
    measure_path = 'ИЗМЕРЕНИЯ/'
    outgas_path = 'ДЕГАЗАЦИЯ/'
    try:
        for i in os.listdir(output_path):
            try:
                for dir_file in os.listdir(output_path + '/' + i):
                    os.remove(output_path + i + '/' + dir_file)
                    print('Объект - внутренний файл: удаляем')
            except:
                print('Объект - файл: удаляем')
                os.remove(output_path + i)
        for d in os.listdir(output_path):
            os.rmdir(output_path + '/' + d)
        os.rmdir(output_path)
    except:
        print('Папки output не существует')


def createDirs():
    output_path = './servicedata/output/'
    switch_path = 'ПРК/'
    device_path = 'ОБОРУД/'
    config_path = 'КОНФИГУРАЦИЯ/'
    outgas_path = 'ДЕГАЗАЦИЯ/'
    plan_path = 'ПЛАНЫ/'
    measure_path = 'ИЗМЕРЕНИЯ/'
    device_path_off = 'ОБОРУД/ОТКЛ/'
    device_path_rf_onoff = 'ОБОРУД/ВЧ/'
    try:
        os.mkdir(output_path)
        os.mkdir(output_path + switch_path)
        os.mkdir(output_path + outgas_path)
        os.mkdir(output_path + device_path)
        os.mkdir(output_path + config_path)
        os.mkdir(output_path + plan_path)
        os.mkdir(output_path + measure_path)
        os.mkdir(output_path + device_path_off)
        os.mkdir(output_path + device_path_rf_onoff)
        print('Папки созданы')
    except FileExistsError:
        pass


def _rf_on(cg, ssi):
    cg.comment("Включение ВЧ на текущей лампе")
    try:
        if ssi.TWT_list[0].type == 'mda':
            cg.call_("763_БСК1_УЛБВ_Ka_ВЧ", [ssi.TWT_list[0].num, 2])
        elif ssi.TWT_list[0].type == 'tas':
            cg.call_("763_БСК1_УЛБВ_K_ВЧ", [ssi.TWT_list[0].num, ssi.TWT_list[0].getAB(), 2])
    except:
        print('stop')


def _rf_off(cg, ssi):
    try:
        cg.comment("Отключение ВЧ на текущей лампе")
        if ssi.TWT_list[0].type == 'mda':
            cg.call_("763_БСК1_УЛБВ_Ka_ВЧ", [ssi.TWT_list[0].num, 1])
        elif ssi.TWT_list[0].type == 'tas':
            cg.call_("763_БСК1_УЛБВ_K_ВЧ", [ssi.TWT_list[0].num, ssi.TWT_list[0].getAB(), 1])
    except:
        print('stop')


def writeTransitionCG(ssi_objects: List[ssi.SSI], name: str, isUnicode=True):
    output_path = './servicedata/output/'
    cg = CycleGramGenerator(0)
    cg.program(name)
    menuList = []
    for s in ssi_objects:
        menuList.append("Включить конфигурацию " + str(s.config_id))
    for s in ssi_objects:
        menuList.append("Отключить конфигурацию " + str(s.config_id))
    cg.repeat(1, 32000)
    cg.menu(menuList)
    cg.select_()
    idx = 0
    for s in ssi_objects:
        idx += 1
        cg.select_var(idx)
        cg.call_(s.nameForAll)
        cg.message("Включить ВЧ на УЛБВ?")
        _rf_on(cg, s)
    for s in ssi_objects:
        idx += 1
        cg.select_var(idx)
        _rf_off(cg, s)
        cg.call_(s.nameForDeviceOff)
    cg.select_end()
    cg.program_end()

    strToWrite = cg.all_data
    if strToWrite is not None:
        with open(output_path + name + '.ci', 'wb') as writeFile:
            if isUnicode:
                strToWrite = strToWrite.encode()
                writeFile.write(strToWrite)
            else:
                ss = strToWrite.encode(encoding='cp1251')
                ss = ss.replace(b'READY', b'\x00')
                # ss = ss.replace(b'READY', b'')
                ss = ss.replace(b'\n', b'\r\n')
                writeFile.write(ss)


def writeCG(ssi_object: ssi.SSI, CGType: str, isUnicode=True):
    output_path = './servicedata/output/'
    switch_path = 'ПРК/'
    device_path = 'ОБОРУД/'
    config_path = 'КОНФИГУРАЦИЯ/'
    measure_path = 'ИЗМЕРЕНИЯ/'
    outgas_path = 'ДЕГАЗАЦИЯ/'
    device_path_off = 'ОБОРУД/ОТКЛ/'
    device_path_rf_onoff = 'ОБОРУД/ВЧ/'
    createDirs()
    if CGType == 'sw':
        name = ssi_object.nameForSwitch
        output_path += switch_path
        strToWrite = ssi_object.getFullCGStrSwitch()

    if CGType == 'outgas_all':
        name = ssi_object.nameForAll
        strToWrite = ssi_object.getDegasStr()

    if CGType == 'outgas':
        name = ssi_object.nameForDegas
        output_path += outgas_path
        strToWrite = ssi_object.getDegasItemStr()

    if CGType == 'dev':
        name = ssi_object.nameForDevice
        output_path += device_path
        strToWrite = ssi_object.getFullCGStrDEV()

    if CGType == 'dev_off':
        name = ssi_object.nameForDeviceOff
        output_path += device_path_off
        strToWrite = ssi_object.getFullCGStrDEV_off()

    if CGType == 'conf':
        name = ssi_object.nameForConfigDevice
        output_path += config_path
        strToWrite = ssi_object.getFullCGStrConfigDevice()
    if CGType == 'all':
        name = ssi_object.nameForAll
        strToWrite = ssi_object.getFullCGStr()

    if CGType == 'singleTransition':
        name = ssi_object.nameForAll
        strToWrite = ssi_object.getSigleTransitionStr()

    if CGType == 'meas':
        name = ssi_object.nameForMeasure
        output_path += measure_path
        strToWrite = ssi_object.getFullCGStrMeasure()

    if CGType == 'rf_on_off':
        name = ssi_object.nameForRfOnOff
        output_path += device_path_rf_onoff
        strToWrite = ssi_object.getCGStrRfOnOff()

    if strToWrite is not None:
        with open(output_path + name + '.ci', 'wb') as writeFile:
            if isUnicode:
                strToWrite = strToWrite.encode()
                writeFile.write(strToWrite)
            else:
                ss = strToWrite.encode(encoding='cp1251')
                ss = ss.replace(b'READY', b'\x00')
                # ss = ss.replace(b'READY', b'')
                ss = ss.replace(b'\n', b'\r\n')
                writeFile.write(ss)


def writePlan(planString):
    plan_path = 'ПЛАНЫ/'
    createDirs()
    path = './servicedata/output/' + plan_path
    if planString['planstr'] is not None:
        planString['planstr'] += '\n'
        with open(path + planString['filename'] + '.pla', 'ab') as writeFile:
            try:
                line = planString['planstr'].encode(encoding='cp1251')
                line = line.replace(b'\n', b'\r\n')
                writeFile.write(line)
            finally:
                pass

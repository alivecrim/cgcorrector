import os

from devices import ssi


def clear_output():
    output_path = './servicedata/output/'
    switch_path = 'ПРК/'
    device_path = 'ОБОРУД/'
    config_path = 'КОНФИГУРАЦИЯ/'
    plan_path = 'ПЛАНЫ/'
    measure_path = 'ИЗМЕРЕНИЯ/'
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
    plan_path = 'ПЛАНЫ/'
    measure_path = 'ИЗМЕРЕНИЯ/'
    device_path_off = 'ОБОРУД/ОТКЛ/'
    try:
        os.mkdir(output_path)
        os.mkdir(output_path + switch_path)
        os.mkdir(output_path + device_path)
        os.mkdir(output_path + config_path)
        os.mkdir(output_path + plan_path)
        os.mkdir(output_path + measure_path)
        os.mkdir(output_path + device_path_off)
        print('Папки созданы')
    except FileExistsError:
        pass


def writeCG(s: ssi.SSI, CGType: str, isUnicode=True):
    output_path = './servicedata/output/'
    switch_path = 'ПРК/'
    device_path = 'ОБОРУД/'
    config_path = 'КОНФИГУРАЦИЯ/'
    measure_path = 'ИЗМЕРЕНИЯ/'
    device_path_off = 'ОБОРУД/ОТКЛ/'
    createDirs()
    if CGType == 'sw':
        name = s.nameForSwitch
        output_path += switch_path
        strToWrite = s.getFullCGStrSwitch()
    if CGType == 'dev':
        name = s.nameForDevice
        output_path += device_path
        strToWrite = s.getFullCGStrDEV()

    if CGType == 'dev_off':
        name = s.nameForDeviceOff
        output_path += device_path_off
        strToWrite = s.getFullCGStrDEV_off()

    if CGType == 'conf':
        name = s.nameForConfigDevice
        output_path += config_path
        strToWrite = s.getFullCGStrConfigDevice()
    if CGType == 'all':
        name = s.nameForAll
        strToWrite = s.getFullCGStr()
    if CGType == 'meas':
        name = s.nameForMeasure
        output_path += measure_path
        strToWrite = s.getFullCGStrMeasure()

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

import os

from devices import ssi


def createDirs():
    path = './servicedata/output/'
    try:
        os.mkdir(path)
        os.mkdir(path + 'switch/')
        os.mkdir(path + 'device/')
        os.mkdir(path + 'config/')
        os.mkdir(path + 'plan/')
        os.mkdir(path + 'measure/')
    except FileExistsError:
        pass


def writeCG(s: ssi.SSI, CGType: str, isUnicode=True):
    createDirs()
    path = './servicedata/output/'
    if CGType == 'sw':
        name = s.nameForSwitch
        path += 'switch/'
        strToWrite = s.getFullCGStrSwitch()
    if CGType == 'dev':
        name = s.nameForDevice
        path += 'device/'
        strToWrite = s.getFullCGStrDEV()
    if CGType == 'conf':
        name = s.nameForConfigDevice
        path += 'config/'
        strToWrite = s.getFullCGStrConfigDevice()
    if CGType == 'all':
        name = s.nameForAll
        strToWrite = s.getFullCGStr()
    if CGType == 'meas':
        name = s.nameForMeasure
        path += 'measure/'
        strToWrite = s.getFullCGStrMeasure()

    if strToWrite is not None:
        with open(path + name + '.ci', 'wb') as writeFile:
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
    createDirs()
    path = './servicedata/output/plan/'
    if planString['planstr'] is not None:
        planString['planstr'] += '\n'
        with open(path + planString['filename'] + '.pla', 'ab') as writeFile:
            try:
                line = planString['planstr'].encode(encoding='cp1251')
                line = line.replace(b'\n', b'\r\n')
                writeFile.write(line)
            finally:
                pass

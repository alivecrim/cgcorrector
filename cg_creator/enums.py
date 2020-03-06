from enum import Enum


class Op(Enum):
    O = 'О'
    K = 'К'
    F = 'Ф'
    E = 'Н'


class CMD(Enum):
    CALL = 'ВЫЗВАТЬ'
    SEND = 'ВЫДАТЬ'
    PAUSE = 'ПАУЗА'
    MESSAGE = 'ДИРЕКТ'
    REPEAT = 'ПОВТ'
    REPEAT_END = 'КПОВТ'
    PROGRAM = 'ПРОГРАМ'
    PROGRAM_END = 'КПРОГРАМ'
    COMPUTE = 'ВЫЧИСЛ'
    WAIT = 'ЖДАТЬ'
    IF = 'ЕСЛИТО'
    IF_END = 'КЕСЛИТО'
    COMMENT = ''
    MENU = 'МЕНЮ'
    SELECT = 'ВЫБОР'
    SELECT_VAR = 'ВАРИАНТ'
    SELECT_END = 'КВЫБОР'
    EXIT = 'ВЫХОД'
    PRINT = 'ПЕЧАТЬ'


class KPI(Enum):
    PAR = 'КПИ_ИД_ПАР'
    VAL = 'КПИ_ЗНАЧЕНИЕ'
    KPI_CMD = 'M_KPI_PAR'


class DtpCmd(Enum):
    CreateInMemory = 'R15170'
    CreateWithDelete = 'R15171'
    CreateWithoutDelete = 'R15172'
    ALC = 'R15173'
    FGM = 'R15174'
    CreateChannel = 'R15167'


class DtpKPI(Enum):
    chNum = '"НОМКАНАЛ"'
    inputPort = '"ВХПОРТ"'
    outputPort = '"ВЫХПОРТ"'
    bandwidth = '"ПОЛОСА"'
    input_frequency = '"ВХЧАСТ"'
    output_frequency = '"ВЫХЧАСТ"'
    gain = '"УРУСИЛ"'


class Align(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2

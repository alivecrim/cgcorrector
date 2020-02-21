from enum import Enum


class Op(Enum):
    O = 'О'
    K = 'К'
    F = 'Ф'
    E = 'Н'
    o = 'О'
    k = 'К'
    f = 'Ф'
    e = 'Н'


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

    SELECT = 'ВЫБОР'
    SELECT_END = 'КВЫБОР'


class KPI(Enum):
    PAR = 'КПИ_ИД_ПАР'
    VAL = 'КПИ_ЗНАЧЕНИЕ'
    KPI_CMD = 'M_KPI_PAR'

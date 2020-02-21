from abc import ABC, abstractmethod
from typing import List, Dict

from cg_creator.enums import Op, CMD, KPI


def getCGStrFormat(operation=None,
                   numOrComment=None,
                   command=None,
                   sign=None,
                   value=None,
                   nameOfCg=None):
    col = []
    for c in range(0, 9):
        col.append(None)
    col[0] = operation
    col[1] = numOrComment
    col[3] = command
    col[4] = sign
    col[5] = value
    col[6] = nameOfCg

    full_str = ''

    col_len = [1,
               4,
               10,
               12,
               5,
               15,
               15,
               8,
               15]

    for idx, c in enumerate(col):
        full_str += extender(c, col_len[idx], idx)

    full_str += '|\n'
    return full_str


def extender(s, needed_width, idx):
    if s is None:
        s = ' ' * needed_width
        s += '|'
        return s

    if isinstance(s, (int, float)):
        s = str(s)
    if isinstance(s, (Op, CMD, KPI)):
        s = s.value
    if idx in [4, 5, 6]:
        diff = needed_width - len(s)
        if diff > 0:
            left_space = round(diff / 2)
            right_space = diff - left_space
            for i in range(0, left_space):
                s = ' ' + s
            for i in range(0, right_space):
                s = s + ' '
    else:
        for i in range(len(s), needed_width):
            s = ' ' + s
    s += '|'
    return s


class Counter:
    _value: int

    def __init__(self, id_start=0):
        self._value = id_start

    def inc(self):
        self._value += 1

    def get_value(self):
        return self._value

    def set_value(self, val):
        self._value = val


class Translator(ABC):
    @abstractmethod
    def get_str(self, idx: 'Counter', params: Dict) -> str:
        pass


class PauseCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        idx.inc()
        full_line = getCGStrFormat(operation=Op.O, numOrComment=idx.get_value(), command=CMD.PAUSE,
                                   value=params['pause'])
        return full_line


class CallCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        idx.inc()
        full_line = getCGStrFormat(operation=Op.O, numOrComment=idx.get_value(), command=CMD.CALL,
                                   nameOfCg=params['call'])
        for i, p in enumerate(params['call_params']):
            full_line += getCGStrFormat(sign=f'&{i + 1}', value=p)
        return full_line


class SendCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        idx.inc()
        full_line = getCGStrFormat(operation=Op.O, numOrComment=idx.get_value(), command=CMD.SEND, value=params['send'])
        for i, p in enumerate(params['send_params']):
            full_line += getCGStrFormat(command=p[0], value=p[1])
        return full_line


class WaitCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        idx.inc()
        full_line = getCGStrFormat(operation=Op.O, numOrComment=idx.get_value(), command=CMD.WAIT, value=params['wait'])
        for i, p in enumerate(params['wait_params']):
            full_line += getCGStrFormat(command=p[0], value=p[1])
        return full_line


class MessageCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        idx.inc()
        full_line = getCGStrFormat(operation=Op.O, numOrComment=idx.get_value(), command=CMD.MESSAGE)
        for p in params['message_params']:
            full_line += getCGStrFormat(operation=Op.F, numOrComment=p)
        return full_line


class RepeatCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        pass


class RepeatEndCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        idx.inc()
        full_line = getCGStrFormat(operation=Op.O, numOrComment=idx.get_value(), command=CMD.REPEAT_END)
        return full_line


class IfCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        idx.inc()
        full_line = getCGStrFormat(operation=Op.O, numOrComment=idx.get_value(), command=CMD.IF)
        for i, p in enumerate(params['if_params']):
            full_line += getCGStrFormat(command=p[0], value=p[1])
        return full_line


class IfEndCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        idx.inc()
        full_line = getCGStrFormat(operation=Op.O, numOrComment=idx.get_value(), command=CMD.IF_END)
        return full_line


class CommentCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        full_line = ''
        for c in params['comment']:
            full_line += getCGStrFormat(operation=Op.K, numOrComment=c)
        return full_line


class ComputeCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        idx.inc()
        full_line = getCGStrFormat(operation=Op.O, numOrComment=idx.get_value(), command=CMD.COMPUTE)
        for compute_value in params['compute_params']:
            full_line += getCGStrFormat(command=compute_value[0], sign=compute_value[1], value=compute_value[2])
        return full_line


class ProgramCreate(Translator, ABC):
    def get_str(self, idx: 'Counter', params: Dict) -> str:
        idx.inc()
        full_line = getCGStrFormat(operation=Op.O, numOrComment=idx.get_value(), command=CMD.PROGRAM,
                                   value=params['program'])
        full_line.replace('\n', 'READY\n')
        return full_line


class ProgramEndCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        idx.inc()
        full_line = getCGStrFormat(operation=Op.O, numOrComment=idx.get_value(), command=CMD.PROGRAM_END)
        return full_line


class SelectCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        pass


class SelectEndCreate(Translator, ABC):

    def get_str(self, idx: 'Counter', params: Dict) -> str:
        pass


class CycleGramGenerator:
    strategy: 'Translator'
    idx: 'Counter'

    all_data: str

    def __init__(self, id_start):
        self.idx = Counter(id_start)
        self.all_data = ''

    def wait(self, time_to_wait, wait_params):
        return self.create_cg_block(CMD.WAIT, {'wait': time_to_wait, 'wait_params': wait_params})

    def comment(self, comment_list):
        if isinstance(comment_list, str):
            comment_list = [comment_list]
        return self.create_cg_block(CMD.COMMENT, {'comment': comment_list})

    def pause(self, pause_value: int):
        return self.create_cg_block(CMD.PAUSE, {'pause': pause_value})

    def message(self, message_params):
        return self.create_cg_block(CMD.MESSAGE, {'message_params': [message_params]})

    def send(self, send_str: str, send_params: List = {}):
        return self.create_cg_block(CMD.SEND, {'send': send_str,
                                               'send_params': send_params})

    def call_(self, call_str: str, call_params: List = {}):
        return self.create_cg_block(CMD.CALL, {'call': call_str,
                                               'call_params': call_params})

    def compute(self, compute_params: List):
        return self.create_cg_block(CMD.COMPUTE, {'compute_params': compute_params})

    def if_(self, if_params: List):
        return self.create_cg_block(CMD.IF, {'if_params': if_params})

    def if_end(self):
        return self.create_cg_block(CMD.IF_END, {})

    def repeat(self, repeat_params: List):
        return self.create_cg_block(CMD.REPEAT, {'repeat_params': repeat_params})

    def repeat_end(self):
        return self.create_cg_block(CMD.REPEAT_END, {})

    def program(self, program):
        return self.create_cg_block(CMD.PROGRAM, {'program': program})

    def program_end(self):
        return self.create_cg_block(CMD.PROGRAM_END, {})

    def create_cg_block(self, cmd_type: CMD, params: Dict) -> str:
        strategy_class = {
            CMD.CALL: CallCreate(),
            CMD.SEND: SendCreate(),
            CMD.PAUSE: PauseCreate(),
            CMD.MESSAGE: MessageCreate(),
            CMD.REPEAT: RepeatCreate(),
            CMD.REPEAT_END: RepeatEndCreate(),
            CMD.PROGRAM: ProgramCreate(),
            CMD.PROGRAM_END: ProgramEndCreate(),
            CMD.COMPUTE: ComputeCreate(),
            CMD.WAIT: WaitCreate(),
            CMD.IF: IfCreate(),
            CMD.IF_END: IfEndCreate(),
            CMD.COMMENT: CommentCreate(),
            CMD.SELECT: SelectCreate(),
            CMD.SELECT_END: SelectEndCreate(),
        }

        self.strategy = strategy_class[cmd_type]

        current_block = self.strategy.get_str(self.idx, params)
        self.all_data += current_block
        return current_block

    def add_to_all_data(self, d: str):
        self.all_data += d

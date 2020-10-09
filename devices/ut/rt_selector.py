from enum import Enum
from typing import List


class Red(Enum):
    RED1 = 1
    RED2 = 2
    NOMINAL = 0


class RT:

    def __init__(self, number) -> None:
        self._number = number
        self._forRed = None
        self._already_use = False

    def set_role(self, red_type: Red):
        if not self.get_already_use():
            self._forRed = red_type
            self.set_already_use()
            return True
        return False

    def get_already_use(self):
        return self._already_use

    def set_already_use(self):
        self._already_use = True

    def __repr__(self) -> str:
        return f'RT{self._number}=>{str(self._forRed)[4:]}'


class Rt_selector_service:

    @classmethod
    def select_rt(cls, needed_ports: List):
        rt_list = []
        for i in range(0, 8):
            rt_list.append(RT(i))
        output_rt = []
        needed_ports = set(needed_ports)
        nom_red = [
            list(filter(lambda x: x != 1 and x != 9, needed_ports)),
            list(filter(lambda x: x == 1 or x == 9, needed_ports))
        ]
        for ports_list in nom_red:
            for j in ports_list:
                cls._process_rt(output_rt, j, rt_list)
        return output_rt

    @classmethod
    def _process_rt(cls, output_rt, port, rt_list):
        if cls.get_rt_num(port) >= 0:
            rt = rt_list[cls.get_rt_num(port)]
            can_to_add = rt.set_role(Red.NOMINAL)
            if can_to_add:
                output_rt.append(rt)
        if cls.get_rt_num(port) == -1:
            for i in range(0, 8):
                rt = rt_list[i]
                can_to_add = rt.set_role(Red.RED1)
                if can_to_add:
                    output_rt.append(rt)
                    break
        if cls.get_rt_num(port) == -2:
            for i in range(7, -1, -1):
                rt = rt_list[i]
                can_to_add = rt.set_role(Red.RED2)
                if can_to_add:
                    output_rt.append(rt)
                    break

    @classmethod
    def get_rt_num(cls, port: int):
        rt_map = {
            1: -1,
            2: 0,
            3: 1,
            4: 2,
            5: 3,
            6: 4,
            7: 5,
            8: 6,
            9: -2,
            10: 7
        }
        return rt_map[port]

from unittest import TestCase

from cg_creator.cg_form import getCGStrFormat, extender


class Test(TestCase):
    def test_get_cgstr(self):
        _N = None
        print(getCGStrFormat(['О', 12, _N, 'ВЫДАТЬ', _N, 'M_KPI_PAR', _N, _N, _N]))
        print(getCGStrFormat(['', _N, _N, 'КПИ_ИД_ПАР', _N, '"ВЫХПОРT"', _N, _N, _N]))

    def test_extender(self):
        print(extender(10, 4, 1))
        print(extender(15.03, 15, 6))

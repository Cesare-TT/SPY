from pprint import pprint

from src import SvtPyVif

class Cfg(SvtPyVif):
    def __init__(self, value=None, name="") -> None:
        super().__init__(value=value, name=name)
        self.attr0 = 0
        self.attr1 = "1"
        self.attr2 = 0.1
        self.subcfg = SubCfg()
        self.subcfg_array = [SubCfg(), SubCfg()]

class SubCfg(SvtPyVif):
    def __init__(self, value=None, name="") -> None:
        super().__init__(value=value, name=name)
        self.attr3 = ["2", "3"]
        self.attr4 = {4: "4", 5: "5"}
        self.attr5 = {'6': 6, '7': 7}

if __name__ == '__main__':
    sv = Cfg(name='cfg')
    sv.gen_var_list('cfg.cfg')
    sv.gen_sv_class('cfg.sv')
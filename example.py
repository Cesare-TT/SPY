from pprint import pprint

from svt_py_vif import SvtPyVif

class Cfg(SvtPyVif):
    def __init__(self, value=None, name="") -> None:
        super().__init__(value=value, name=name)
        self.v_int = 0
        self.v_str = "1"
        self.v_real = 0.1
        self.subcfg = SubCfg()
        self.subcfg_array = [SubCfg(), SubCfg()]

class SubCfg(SvtPyVif):
    def __init__(self, value=None, name="") -> None:
        super().__init__(value=value, name=name)
        self.int_list = [0, 1]
        self.str_list = ["2", "3"]
        self.str_dict = {4: "4", 5: "5"}
        self.array_array = [[0,1], [2,3]]

if __name__ == '__main__':
    sv = Cfg(name='cfg')
    sv.gen_var_list('cfg.cfg')
    sv.gen_sv_class('cfg.sv')
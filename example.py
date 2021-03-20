from pprint import pprint

from svt_py_vif import SvtPyVif

class Cfg(SvtPyVif):
    def __init__(self, value=None, name='') -> None:
        super().__init__(value=value, name=name)
        self.v_int = 1
        self.v_str = '2'
        self.v_real = 0.3
        self.subcfg = SubCfg()
        self.subcfg_array = [[SubCfg()], [SubCfg()], [SubCfg()]]

class SubCfg(SvtPyVif):
    def __init__(self, value=None, name='') -> None:
        super().__init__(value=value, name=name)
        self.int_list = [1, 2, 3]
        self.str_list = ['2', '3', '4']
        self.str_dict = {4: '4', 5: '5', 6: '6'}
        self.array_array = [[1,2,3], [4,5,6], [7,8,9]]
        self.str_array_array = [['4', '5', '6'], ['6', '7', '8'], ['7', '8', '9']]

if __name__ == '__main__':
    sv = Cfg(name='cfg')
    sv.gen_sv_class('cfg.sv')
    sv.subcfg_array = [[SubCfg()], [SubCfg()], [SubCfg()], [SubCfg()], [SubCfg()], [SubCfg()]] 
    # for l in sv.subcfg_array:
    #     for item in l:
    #         print(item.parent.get_full_name())
    #         print(item.get_full_name())
    sv.gen_var_list('cfg.cfg')



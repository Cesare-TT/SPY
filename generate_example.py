from Spy import SpyStreamHelper,generate_python
from Spy.SpyProto import *


class SubDemo(SpyClass):

    def __init__(self,name=''):
        super().__init__(name=name)
        self.register(SpyInt('a'),1)
        self.register(SpyFloat('b'),2)



class Demo(SpyClass):

    def __init__(self,name=''):
        super().__init__(name=name)
        self.register(SpyInt('a'),1)
        self.register(SpyFloat('b'),2)
        self.register(SpyString('c',"asdf"),3)
        self.register(SpyBits(16,'d',0),4)
        self.register(SubDemo('e'),5)
        self.register(SpyDArray('f',[SpyFloat('',2.4)]),6)

generate_python('example.py',SubDemo,Demo)
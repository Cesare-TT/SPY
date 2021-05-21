from Spy import *
class SpyAXIPayload(SpyClass):

    def __init__(self,name=''):
        super().__init__(name=name)
        self.register(SpyInt('a'),1)
        self.register(SpyFloat('b'),2)
from .SpyStreamHelper import DArrayStreamHelper


class SpyDArrayInst(object):

    def __init__(self,stream_helper,*value):
        super().__init__()
        self._stream_helper = stream_helper
        self._value = value

    def pack(self,field=0,unuse=None):
        stream = b''
        for i in self._value:
            stream = stream + self._stream_helper(self._value[0]).pack(0,i)
        return stream

    def unpack(self,dat):
        stream_list = DArrayStreamHelper().stream_splitter(dat)
        self._value = [self._stream_helper(self._value[0]).unpack(s) for s in stream_list]
        return self._value

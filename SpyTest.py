from Spy import SpyStreamHelper,SpyInst


class SubDemo(object):

    def __init__(self):
        super().__init__()
        self.a = 0
        self.b = 0

    def pack(self,field=0,unuse=None):
        stream_a = SpyStreamHelper.IntStreamHelper().pack(1,self.a)
        stream_b = SpyStreamHelper.FloatStreamHelper().pack(2,self.b)
        stream = stream_a + stream_b + b''
        return SpyStreamHelper.ClassStreamHelper().stream_assembler(field,stream)

    def unpack(self,dat):
        stream = SpyStreamHelper.ClassStreamHelper()
        stream_dict = stream.stream_splitter(dat)
        for k,v in stream_dict.items():
            if k==1: self.a = SpyStreamHelper.IntStreamHelper().unpack(v)
            if k==2: self.b = SpyStreamHelper.FloatStreamHelper().unpack(v)
        return self

if __name__ == '__main__':
    obj1_SubDemo = SubDemo()
    stream_SubDemo = obj1_SubDemo.pack()
    obj2_SubDemo = SubDemo()
    obj2_SubDemo.unpack(stream_SubDemo)





class Demo(object):

    def __init__(self):
        super().__init__()
        self.a = 0
        self.b = 0
        self.c = "asdf"
        self.d = 0
        self.e = SubDemo()
        self.f = SpyInst.SpyDArrayInst(SpyStreamHelper.FloatStreamHelper,2.4)

    def pack(self,field=0,unuse=None):
        stream_a = SpyStreamHelper.IntStreamHelper().pack(1,self.a)
        stream_b = SpyStreamHelper.FloatStreamHelper().pack(2,self.b)
        stream_c = SpyStreamHelper.StringStreamHelper().pack(3,self.c)
        stream_d = SpyStreamHelper.BitsStreamHelper(17).pack(4,self.d)
        stream_e = SpyStreamHelper.ClassStreamHelper(self.e).pack(5,self.e)
        stream_f = SpyStreamHelper.DArrayStreamHelper(self.f).pack(6,self.f)
        stream = stream_a + stream_b + stream_c + stream_d + stream_e + stream_f + b''
        return SpyStreamHelper.ClassStreamHelper().stream_assembler(field,stream)

    def unpack(self,dat):
        stream = SpyStreamHelper.ClassStreamHelper()
        stream_dict = stream.stream_splitter(dat)
        for k,v in stream_dict.items():
            if k==1: self.a = SpyStreamHelper.IntStreamHelper().unpack(v)
            if k==2: self.b = SpyStreamHelper.FloatStreamHelper().unpack(v)
            if k==3: self.c = SpyStreamHelper.StringStreamHelper().unpack(v)
            if k==4: self.d = SpyStreamHelper.BitsStreamHelper(17).unpack(v)
            if k==5: self.e = SpyStreamHelper.ClassStreamHelper(self.e).unpack(v)
            if k==6: self.f = SpyStreamHelper.DArrayStreamHelper(self.f).unpack(v)
        return self

if __name__ == '__main__':
    obj1_Demo = Demo()
    stream_Demo = obj1_Demo.pack()
    obj2_Demo = Demo()
    obj2_Demo.unpack(stream_Demo)
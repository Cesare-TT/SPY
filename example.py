from Spy import StreamHelper,SpyInst


class SubDemo(object):

    def __init__(self):
        super().__init__()
        self.a = 0
        self.b = 0

    def pack(self,field=0,unuse=None):
        stream_a = StreamHelper.IntStreamHelper().pack(1,self.a)
        stream_b = StreamHelper.FloatStreamHelper().pack(2,self.b)
        stream = stream_a + stream_b + b''
        return StreamHelper.ClassStreamHelper().stream_assembler(field,stream)

    def unpack(self,dat):
        stream = StreamHelper.ClassStreamHelper()
        stream_dict = stream.stream_splitter(dat)
        for k,v in stream_dict.items():
            if k==1: self.a = StreamHelper.IntStreamHelper().unpack(v)
            if k==2: self.b = StreamHelper.FloatStreamHelper().unpack(v)
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
        self.f = SpyInst.SpyDArrayInst(StreamHelper.FloatStreamHelper,2.4)

    def pack(self,field=0,unuse=None):
        stream_a = StreamHelper.IntStreamHelper().pack(1,self.a)
        stream_b = StreamHelper.FloatStreamHelper().pack(2,self.b)
        stream_c = StreamHelper.StringStreamHelper().pack(3,self.c)
        stream_d = StreamHelper.BitsStreamHelper(16).pack(4,self.d)
        stream_e = StreamHelper.ClassStreamHelper(self.e).pack(5,self.e)
        stream_f = StreamHelper.DArrayStreamHelper(self.f).pack(6,self.f)
        stream = stream_a + stream_b + stream_c + stream_d + stream_e + stream_f + b''
        return StreamHelper.ClassStreamHelper().stream_assembler(field,stream)

    def unpack(self,dat):
        stream = StreamHelper.ClassStreamHelper()
        stream_dict = stream.stream_splitter(dat)
        for k,v in stream_dict.items():
            if k==1: self.a = StreamHelper.IntStreamHelper().unpack(v)
            if k==2: self.b = StreamHelper.FloatStreamHelper().unpack(v)
            if k==3: self.c = StreamHelper.StringStreamHelper().unpack(v)
            if k==4: self.d = StreamHelper.BitsStreamHelper(16).unpack(v)
            if k==5: self.e = StreamHelper.ClassStreamHelper(self.e).unpack(v)
            if k==6: self.f = StreamHelper.DArrayStreamHelper(self.f).unpack(v)
        return self

if __name__ == '__main__':
    obj1_Demo = Demo()
    stream_Demo = obj1_Demo.pack()
    obj2_Demo = Demo()
    obj2_Demo.unpack(stream_Demo)
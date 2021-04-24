
import unittest
import random

import Spy.SpyStreamHelper as StreamHelper
import Spy.SpyInst      as SpyInst

from Spy.SpyStreamHelper import IntStreamHelper,\
                                FloatStreamHelper,\
                                StringStreamHelper,\
                                BitsStreamHelper,\
                                DArrayStreamHelper,\
                                ClassStreamHelper

from Spy.SpyInst        import  SpyDArrayInst



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
        stream_e = StreamHelper.ClassStreamHelper().pack(5,self.e)
        stream_f = StreamHelper.DArrayStreamHelper().pack(6,self.f)
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


class TestStreamHelper(unittest.TestCase):

    def run_once(self,helper,src):
        stream = helper().pack(0,src)
        des = helper().unpack(stream)
        self.assertEqual(src,des)


class TestIntStreamHelper(TestStreamHelper):
    Helper = IntStreamHelper

    def test_base(self):
        self.run_once(self.Helper,3)

    def test_random(self):
        repeat = 100
        for _ in range(repeat):
            self.run_once(self.Helper,random.randint(0,100000))

class TestFloatStreamHelper(TestStreamHelper):
    Helper = FloatStreamHelper

    def test_base(self):
        self.run_once(self.Helper,3.2)

    def test_random(self):
        repeat = 100
        for _ in range(repeat):
            self.run_once(self.Helper,random.uniform(0,100000))

class TestStringStreamHelper(TestStreamHelper):
    Helper = StringStreamHelper

    def test_base(self):
        self.run_once(self.Helper,"test")

    def test_random(self):
        repeat = 100
        sets = [chr(i) for i in range(0,127)]
        for _ in range(repeat):
            string = "".join([random.choice(sets) for x in range(random.randint(0,1000))])
            self.run_once(self.Helper,string)

class TestBistStreamHelper(TestStreamHelper):
    Helper = BitsStreamHelper

    def run_once(self,helper,width,src):
        stream = helper(width).pack(0,src)
        des = helper(width).unpack(stream)
        self.assertEqual(src,des)

    def test_base(self):
        self.run_once(self.Helper,4,200+100*256)

    def test_random(self):
        repeat = 100
        width = random.randint(0,511)
        value = random.randint(0,2**width-1)
        for _ in range(repeat):
            self.run_once(self.Helper,width,value)

class TestDArrayStreamHelper(TestStreamHelper):
    Helper = DArrayStreamHelper

    # def run_once(self,helper,src):
    #     print(src)
    #     stream = helper().pack(0,src)
    #     des = helper().unpack(stream)
    #     self.assertEqual(src,des)

    def test_base(self):
        src = SpyDArrayInst(IntStreamHelper,1,2)
        stream = self.Helper().pack(0,src)
        des = SpyDArrayInst(IntStreamHelper,1)
        des.unpack(stream)
        self.assertEqual(self.Helper().pack(0,src), self.Helper().pack(0,des))

    def test_base_with_class(self):
        src = SpyDArrayInst(ClassStreamHelper,SubDemo(),SubDemo())
        stream = self.Helper().pack(0,src)
        des = SpyDArrayInst(ClassStreamHelper,SubDemo())
        des.unpack(stream)
        self.assertEqual(self.Helper().pack(0,src), self.Helper().pack(0,des))



class TestClassStreamHelper(TestStreamHelper):
    Helper = ClassStreamHelper

    def test_base(self):
        src = SubDemo()
        src.a = 3
        stream = src.pack(0)
        des = SubDemo()
        des.unpack(stream)
        self.assertEqual(src.pack(0),des.pack(0))

    def test_base_level2(self):
        src = Demo()
        src.a = 3
        src.e.a = 10
        stream = src.pack(0)
        des = Demo()
        des.unpack(stream)
        #print(src,des)
        src.pack(0)
        des.pack(0)
        self.assertEqual(src.pack(0),des.pack(0))

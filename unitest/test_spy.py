from math import ceil
import unittest
import random
import string
import os,subprocess

from Spy import SpyStreamHelper
from Spy import SpyInst
from Spy import generate_sv
from Spy import generate_python

from Spy.SpyStreamHelper import IntStreamHelper
from Spy.SpyStreamHelper import FloatStreamHelper
from Spy.SpyStreamHelper import StringStreamHelper
from Spy.SpyStreamHelper import BitsStreamHelper
from Spy.SpyStreamHelper import DArrayStreamHelper
from Spy.SpyStreamHelper import ClassStreamHelper

from Spy.SpyInst import SpyDArrayInst
from Spy.SpyProto import *

SPY_TYPE_BIT    = SpyStreamHelper.SpyStreamHelper.SPY_TYPE_BIT
SPY_TYPE_INT    = SpyStreamHelper.SpyStreamHelper.SPY_TYPE_INT
SPY_TYPE_FLOAT  = SpyStreamHelper.SpyStreamHelper.SPY_TYPE_FLOAT
SPY_TYPE_CLASS  = SpyStreamHelper.SpyStreamHelper.SPY_TYPE_CLASS
SPY_TYPE_STRING = SpyStreamHelper.SpyStreamHelper.SPY_TYPE_STRING
SPY_TYPE_LIST   = SpyStreamHelper.SpyStreamHelper.SPY_TYPE_LIST

# class TestDemo(SpyClass):
#     def __init__(self, name=''):
#         super().__init__(name=name)

#     def get_rand_spytype(self):
#         rand_type = random.randint([SPY_TYPE_BIT, SPY_TYPE_LIST])
#         if rand_type == SPY_TYPE_BIT:
#             return SpyInt
#         elif rand_type == SPY_TYPE_INT:
#             return SpyInt
#         elif rand_type == SPY_TYPE_FLOAT:
#             return SpyFloat
#         elif rand_type == SPY_TYPE_CLASS:
#             return SpyClass
#         elif rand_type == SPY_TYPE_STRING:
#             return SpyString
#         elif rand_type == SPY_TYPE_LIST:
#             return SpyList

#     def rand_register(self, num_attr):
#         for i in range(0, num_attr):
#             pass

# class SpyMetaclass(type):
#     def __new__(cls, name, bases, attrs):
#         # attrs['add'] = lambda self, value: self.append(value)


#         return type.__new__(cls, name, bases, attrs)

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
        self.register(SpyBits(17,'d',0),4)
        self.register(SubDemo('e'),5)
        self.register(SpyDArray('f',[SpyFloat('',2.4)]),6)

class SpyTestBase(unittest.TestCase):
    def run_once(self):
        pass

class SpyTest(SpyTestBase):
    def pre_test(self):
        generate_python('SpyTest.py', SubDemo, Demo)
        generate_sv('SpyTest.sv', SubDemo, Demo, one_file=False)

    def run_once(self, helper, sv_test, src):
        self.pre_test()
        from SpyTest import Demo as SpyDemo
        from SpyTest import SubDemo as SpySubDemo
        stream = helper().pack(0, src)
        f_stream = open('SpyStreamPy2Sv', 'w')
        for B in stream:
            f_stream.write('{:0>2x}\n'.format(B))
        f_stream.close()
        subprocess.Popen('echo $0;echo $SHELL;echo $PATH;module list', shell=True, executable='/bin/zsh')
        # source /usr/share/modules/init/bash;module list;module load vcs;
        os.system(f'make OPT=+{sv_test}')
        stream = b''
        f_stream = open('SpyStreamSv2Py', 'r')
        for line in f_stream.readlines():
            if line is not None:
                stream = b''.join([stream, bytes.fromhex(line.strip())])
        des = helper().unpack(stream)
        print(f'{src=}')
        print(f'{des=}')
        self.assertEqual(src, des)

class SpyIntTest(SpyTest):
    Helper = IntStreamHelper

    def test_base(self):
        self.run_once(self.Helper, 'SPY_INT_TEST', 3)

    def test_random(self):
        repeat = 1
        for _ in range(repeat):
            self.run_once(self.Helper, 'SPY_INT_TEST', random.randint(-2**31, 2**31-1))

class SpyFloatTest(SpyTest):
    Helper = FloatStreamHelper

    def test_base(self):
        self.run_once(self.Helper, 'SPY_FLOAT_TEST', 5.677879)

    def test_random(self):
        repeat = 1
        for _ in range(repeat):
            self.run_once(self.Helper, 'SPY_FLOAT_TEST', random.uniform(-2**63, 2**63-1))

class SpyStringTest(SpyTest):
    Helper = StringStreamHelper

    def test_base(self):
        self.run_once(self.Helper, 'SPY_STRING_TEST', 'Hello SPY!')

    def test_random(self):
        repeat = 1
        for _ in range(repeat):
            len = random.randint(1, 1000)
            self.run_once(self.Helper, 'SPY_STRING_TEST',  ''.join(random.sample(ceil(len/62)*(string.ascii_letters + string.digits), len)))

class SpyBitTest(SpyTest):
    Helper = BitsStreamHelper

    def run_once(self, helper, width, sv_test, src):
        self.pre_test()
        from SpyTest import Demo as SpyDemo
        from SpyTest import SubDemo as SpySubDemo
        stream = helper(width).pack(0, src)
        f_stream = open('SpyStreamPy2Sv', 'w')
        for B in stream:
            f_stream.write('{:0>2x}\n'.format(B))
        f_stream.close()
        os.system(f'make OPT="+{sv_test} +define+BIT_WIDTH={width}"')
        stream = b''
        f_stream = open('SpyStreamSv2Py', 'r')
        for line in f_stream.readlines():
            if line is not None:
                stream = b''.join([stream, bytes.fromhex(line.strip())])
        des = helper(width).unpack(stream)
        print(f'{src=}')
        print(f'{des=}')
        self.assertEqual(src, des)

    def test_base(self):
        self.run_once(self.Helper, 2, 'SPY_BIT_TEST', 2)
    
    def test_random(self):
        repeat = 1
        for _ in range(repeat):
            width = random.randint(1, 64)
            self.run_once(self.Helper, width, 'SPY_BIT_TEST', random.randint(0, 2**width-1))

class SpyDArrayTest(SpyTest):
    Helper = DArrayStreamHelper

    def test_base(self):
        self.pre_test()
        from SpyTest import Demo as SpyDemo
        from SpyTest import SubDemo as SpySubDemo
        src = SpyDArrayInst(StringStreamHelper, "Hello", "Spy")
        stream = self.Helper().pack(0, src)
        f_stream = open('SpyStreamPy2Sv', 'w')
        for B in stream:
            f_stream.write('{:0>2x}\n'.format(B))
        f_stream.close()
        os.system(f'make OPT=+SPY_LIST_TEST')
        print(src._value)
        stream = b''
        des = SpyDArrayInst(StringStreamHelper, '')
        f_stream = open('SpyStreamSv2Py', 'r')
        for line in f_stream.readlines():
            if line is not None:
                stream = b''.join([stream, bytes.fromhex(line.strip())])
        des.unpack(stream)
        # print(src.a)
        # print(des.a)
        # self.assertEqual(src.a, des.a)
        self.assertEqual(self.Helper().pack(0, src), self.Helper().pack(0, des))

class SpyClassTest(SpyTest):
    def test_base(self):
        self.pre_test()
        from SpyTest import Demo as SpyDemo
        from SpyTest import SubDemo as SpySubDemo
        src = SpyDemo()
        src.a = 3
        stream = src.pack(0)
        f_stream = open('SpyStreamPy2Sv', 'w')
        for B in stream:
            f_stream.write('{:0>2x}\n'.format(B))
        f_stream.close()
        os.system(f'make OPT=+SPY_CLASS_TEST')
        stream = b''
        des = SpyDemo()
        f_stream = open('SpyStreamSv2Py', 'r')
        for line in f_stream.readlines():
            if line is not None:
                stream = b''.join([stream, bytes.fromhex(line.strip())])
        des.unpack(stream)
        # print(src.a)
        # print(des.a)
        # self.assertEqual(src.a, des.a)
        self.assertEqual(src.pack(0), des.pack(0))
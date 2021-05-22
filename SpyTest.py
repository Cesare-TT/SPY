from functools  import reduce
from operator   import concat
import math
import struct
#
#
#
#
#
class SpyStreamHelper(object):
    # line 1-10 for import
    ############################################################################################
    # SpyStreamHelper
    ############################################################################################
    class SpyStreamHelper(object):
    
        def __init__(self,*args):
            super().__init__()
    
        SPY_TYPE_BIT    = 1
        SPY_TYPE_INT    = 2
        SPY_TYPE_FLOAT  = 3
        SPY_TYPE_CLASS  = 4
        SPY_TYPE_STRING = 5
        SPY_TYPE_LIST   = 6
    
        def _get_len(self,dat):
            types = self._get_type_from_key(dat)
            if types == self.SPY_TYPE_INT:   return 8
            if types == self.SPY_TYPE_FLOAT: return 12
            else:                       return 8 + struct.unpack('i',dat[4:8])[0]
    
        def _get_field_from_key(self,key):
            return struct.unpack('i',key[1:4] + b'\x00')[0]
    
        def _get_type_from_key(self,key):
            return struct.unpack('i',key[0:1] + b'\x00\x00\x00')[0]
    
        def _tag_pack(self,field,types):
            field_byte = struct.pack('i',int(field))[:-1]
            types_byte = struct.pack('i',int(types))[0:1]
            return types_byte + field_byte
    
        def _pack_splitter(self,dat):
            sub_pack_list = []
            ptr = 0
            ptr_limit = len(dat)
            while ptr < ptr_limit:
                length = self._get_len(dat[ptr:ptr+8])
                sub_pack_list.append(dat[ptr:ptr+length])
                ptr += length
            return sub_pack_list
    
    
        def report_string(self,val):
            return str(val)
    
    
    ############################################################################################
    # BitsStreamHelper
    ############################################################################################
    class BitsStreamHelper(SpyStreamHelper):
    
        def __init__(self,width):
            super().__init__()
            self.width = width
    
        @property
        def types(self):
            return self.SPY_TYPE_BIT
    
        def _value_pack(self,value):
            char_list =[]
            tmp = value
            #print(self.width)
            #print(math.ceil(self.width/8))
            for _ in range(math.ceil(self.width/8)):
                char = int(tmp - ((tmp>>8)<<8)) #- 128
                tmp = tmp >> 8 
                char_list.append(char)
            #print(char_list)
            return struct.pack('%dB' % len(char_list),*char_list)
        
        def _value_unpack(self,dat):
            res = 0
            offset = 0
            #print(dat)
            for d in dat:
                #print(d)
                #res = res + ((d+128)%256 << offset)
                res = res + (d%256<<offset)
                offset = offset + 8
            return res
    
        def pack(self,field=None,value=None):
            tag_byte   = self._tag_pack(field,self.types)
            value_byte  = self._value_pack(value)
            length_byte = struct.pack('i',int(len(value_byte)))
            return tag_byte + length_byte + value_byte
    
        def unpack(self,dat):
            self.length = struct.unpack('i',dat[4:8])[0]
            self.value = self._value_unpack(dat[8:8+self.length])
            return self.value
    
    
    
    ############################################################################################
    # StringStreamHelper
    ############################################################################################
    class StringStreamHelper(SpyStreamHelper):
    
        @property
        def types(self):
            return self.SPY_TYPE_STRING
    
        def pack(self,field=None,value=None):
            tag_byte   = self._tag_pack(field,self.types)
            value_byte  = struct.pack('%ds' % len(value) ,bytes(value,'ascii'))
            length_byte = struct.pack('i',int(len(value_byte)))
            return tag_byte + length_byte + value_byte
    
        def unpack(self,dat):
            length = struct.unpack('i',dat[4:8])[0]
            return str(struct.unpack('%ds' % length,dat[8:8+length])[0],'ascii')
    
        def report_string(self,val):
            return "\"%s\"" % str(val)
    
    ############################################################################################
    # IntStreamHelper
    ############################################################################################
    class IntStreamHelper(SpyStreamHelper):
    
        @property
        def types(self):
            return self.SPY_TYPE_INT
    
        def pack(self,field=None,value=None):
            tag_byte   = self._tag_pack(field,self.types)
            value_byte = struct.pack('i',int(value))
            return tag_byte + value_byte
    
        def unpack(self,dat):
            return struct.unpack('i',dat[4:8])[0]
    
    
    
    ############################################################################################
    # FloatStreamHelper
    ############################################################################################
    class FloatStreamHelper(SpyStreamHelper):
    
        @property
        def types(self):
            return self.SPY_TYPE_FLOAT
    
        def pack(self,field=None,value=None):
            tag_byte   = self._tag_pack(field,self.types)
            value_byte = struct.pack('d',float(value))
            return tag_byte + value_byte
    
        def unpack(self,dat):
            self.value = struct.unpack('d',dat[4:12])[0]
            return self.value
    
    
    
    ############################################################################################
    # ListStreamHelper
    ############################################################################################
    class ListStreamHelper(SpyStreamHelper):
    
        def __init__(self,inst=None):
            super().__init__()
            self.inst = inst
    
        @property
        def types(self):
            return self.SPY_TYPE_LIST
    
        def pack(self,field=None,value=None):
            tag_byte    = self._tag_pack(field,self.types)
            value_byte  = value.pack(field)
            length_byte = struct.pack('i',int(len(value_byte)))
            return tag_byte + length_byte + value_byte
            
        def stream_splitter(self,dat):
            return self._pack_splitter(dat[8:])
    
        def unpack(self,dat):
    
            return self.inst
    
    class DArrayStreamHelper(ListStreamHelper):
        pass
    
    
    
    ############################################################################################
    # ClassStreamHelper
    ############################################################################################
    class ClassStreamHelper(SpyStreamHelper):
    
        def __init__(self,inst=None):
            super().__init__()
            self.inst = inst
    
        @property
        def types(self):
            return self.SPY_TYPE_CLASS
    
        def pack(self,field=None,value=None):
            return value.pack(field)
    
        def unpack(self,dat):
            return self.inst.unpack(dat)
    
        def stream_splitter(self,dat):
            dat_list = self._pack_splitter(dat[8:])
            stream_dict = {}
            for i in dat_list:
                stream_dict[self._get_field_from_key(i)] = i
            return stream_dict
    
        def stream_assembler(self,field,stream):
            tag_byte    = self._tag_pack(field,self.types)
            value_byte  = stream
            length_byte = struct.pack('i',int(len(value_byte)))
            return tag_byte + length_byte + value_byte
class SpyInst(object):
    # line 1-10 for import
    class SpyDArrayInst(object):
    
        def __init__(self,stream_helper,*value):
            super().__init__()
            self._stream_helper = stream_helper
            self._value = value
    
        def pack(self,field=0,unuse=None):
            stream = b''
            for index,i in enumerate(self._value):
                stream = stream + self._stream_helper(self._value[0]).pack(index,i)
            return stream
    
        def unpack(self,dat):
            stream_list = SpyStreamHelper.DArrayStreamHelper().stream_splitter(dat)
            self._value = [self._stream_helper(self._value[0]).unpack(s) for s in stream_list]
            return self._value



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

    def report_string(self):
        res = ""
        res += "a = %s\n" % SpyStreamHelper.IntStreamHelper().report_string(self.a)
        res += "b = %s\n" % SpyStreamHelper.FloatStreamHelper().report_string(self.b)
        return res

if __name__ == '__main__':
    obj1_SubDemo = SubDemo()
    print(obj1_SubDemo.report_string())
    stream_SubDemo = obj1_SubDemo.pack()
    obj2_SubDemo = SubDemo()
    obj2_SubDemo.unpack(stream_SubDemo)
    print(obj2_SubDemo.report_string())





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

    def report_string(self):
        res = ""
        res += "a = %s\n" % SpyStreamHelper.IntStreamHelper().report_string(self.a)
        res += "b = %s\n" % SpyStreamHelper.FloatStreamHelper().report_string(self.b)
        res += "c = %s\n" % SpyStreamHelper.StringStreamHelper().report_string(self.c)
        res += "d = %s\n" % SpyStreamHelper.BitsStreamHelper(17).report_string(self.d)
        res += "e = %s\n" % SpyStreamHelper.ClassStreamHelper(self.e).report_string(self.e)
        res += "f = %s\n" % SpyStreamHelper.DArrayStreamHelper(self.f).report_string(self.f)
        return res

if __name__ == '__main__':
    obj1_Demo = Demo()
    print(obj1_Demo.report_string())
    stream_Demo = obj1_Demo.pack()
    obj2_Demo = Demo()
    obj2_Demo.unpack(stream_Demo)
    print(obj2_Demo.report_string())
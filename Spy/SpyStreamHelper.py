from functools  import reduce
from operator   import concat
import math
import struct

############################################################################################
# StreamHelper
############################################################################################
class StreamHelper(object):

    def __init__(self,*args):
        super().__init__()

    SPY_TYPE_BIT    = 1
    SPY_TYPE_INT    = 2
    SPY_TYPE_FLOAT  = 3
    SPY_TYPE_CLASS  = 4
    SPY_TYPE_STRING = 5
    SPY_TYPE_LIST   = 6

    def _get_len(self,dat):
        types = struct.unpack('i',dat[3:4] + b'\x00\x00\x00')[0]
        if types == self.SPY_TYPE_INT:   return 8
        if types == self.SPY_TYPE_FLOAT: return 12
        else:                       return 8 + struct.unpack('i',dat[4:8])[0]

    def _tag_pack(self,field,types):
        field_byte = struct.pack('i',int(field))[:-1]
        types_byte = struct.pack('i',int(types))[0:1]
        return field_byte + types_byte

    def _pack_splitter(self,dat):
        sub_pack_list = []
        ptr = 0
        ptr_limit = len(dat)
        while ptr < ptr_limit:
            length = self._get_len(dat[ptr:ptr+8])
            sub_pack_list.append(dat[ptr:ptr+length])
            ptr += length
        return sub_pack_list



############################################################################################
# BitsStreamHelper
############################################################################################
class BitsStreamHelper(StreamHelper):

    def __init__(self,width):
        super().__init__()
        self.width = width

    @property
    def types(self):
        return self.SPY_TYPE_BIT

    def _value_pack(self,value):
        char_list =[]
        tmp = value
        for _ in range(self.width):
            char = int(tmp - ((tmp>>8)<<8)) - 128
            tmp = tmp >> 8 
            char_list.append(char)
        return struct.pack('%db' % len(char_list),*char_list)
    
    def _value_unpack(self,dat):
        res = 0
        offset = 0
        for d in dat:
            res = res + ((d+128)%256 << offset)
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
class StringStreamHelper(StreamHelper):

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



############################################################################################
# IntStreamHelper
############################################################################################
class IntStreamHelper(StreamHelper):

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
class FloatStreamHelper(StreamHelper):

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
class ListStreamHelper(StreamHelper):

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
class ClassStreamHelper(StreamHelper):

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
            stream_dict[struct.unpack('i',i[0:3] + b'\x00')[0]] = i
        return stream_dict

    def stream_assembler(self,field,stream):
        tag_byte    = self._tag_pack(field,self.types)
        value_byte  = stream
        length_byte = struct.pack('i',int(len(value_byte)))
        return tag_byte + length_byte + value_byte

from jinja2     import PackageLoader,Environment
import builtins

############################################################################################
# SpyProtoRoot
############################################################################################
class SpyProtoRoot(object):

    def __init__(self,name,default):
        super().__init__()
        self._name = name
        self._default = default

    @property
    def default_value(self):
        return self._default

    @property
    def name(self):
        return self._name

    @property
    def helper_param(self):
        return ""

    @property
    def sv_default_value(self):
        return self._default if self._default is not None else ''

    @property
    def sv_type_string(self):
        return ''

    @property
    def sv_spy_type(self):
        return self.__class__.__name__


    @property
    def sv_var_declr(self):
        return '{:<16s}    {}'.format(self.sv_type_string, self.name)

    @property
    def sv_format_symbol(self):
        return ''

    def sv_report_string(self, name=None):
        if name is None:
            name = self.name
        return f'$display("{name}: {self.sv_format_symbol}", {name});'

############################################################################################
# SpyBits
############################################################################################
class SpyBits(SpyProtoRoot):

    def __init__(self,width,name,default=0):
        super().__init__(name,default)
        self._width = width

    @property
    def type_string(self):
        return 'Bits'

    @property
    def helper_param(self):
        return self._width

    @property
    def sv_default_value(self):
        return f'{self._width}\'h{self._default}' if self._default is not None else f'{self._width}\'h0'

    @property
    def sv_type_string(self):
        # return 'bit [{:>2d}:0]'.format(self._width-1)
        return f'bit [{self._width-1}:0]'

    @property
    def sv_spy_type(self):
        return f'SpyBit#({self._width})'

    @property
    def sv_format_symbol(self):
        return '%h'

    def sv_report_string(self, name=None):
        if name is None:
            name = self.name
        return f'$display("{name}: {self._width}\'h{self.sv_format_symbol}", {name});'


############################################################################################
# SpyString
############################################################################################
class SpyString(SpyProtoRoot):

    def __init__(self,name,default=""):
        super().__init__(name,default)

    @property
    def type_string(self):
        return 'String'

    @property
    def default_value(self):
        return "\"%s\"" % self._default

    @property
    def sv_default_value(self):
        return f'"{self._default}"' if self._default is not None else '""'

    @property
    def sv_type_string(self):
        return 'string'

    @property
    def sv_spy_type(self):
        return 'SpyString'

    @property
    def sv_format_symbol(self):
        return '%s'

    def sv_report_string(self, name=None):
        if name is None:
            name = self.name
        return f'$display("{name}: \\"{self.sv_format_symbol}\\"", {name});'



############################################################################################
# SpyInt
############################################################################################
class SpyInt(SpyProtoRoot):

    def __init__(self,name,default=0):
        super().__init__(name,default)

    @property
    def type_string(self):
        return 'Int'

    @property
    def sv_default_value(self):
        return f'\'h{self._default}' if self._default is not None else f'\'h0'

    @property
    def sv_type_string(self):
        return 'int'

    @property
    def sv_spy_type(self):
        return 'SpyInt'

    @property
    def sv_format_symbol(self):
        return '%h'



############################################################################################
# SpyFloat
############################################################################################
class SpyFloat(SpyProtoRoot):

    def __init__(self,name,default=0):
        super().__init__(name,default)

    @property
    def type_string(self):
        return 'Float'

    @property
    def sv_default_value(self):
        return self._default if self._default is not None else f'0.0'

    @property
    def sv_type_string(self):
        return 'real'

    @property
    def sv_spy_type(self):
        return 'SpyFloat'

    @property
    def sv_format_symbol(self):
        return '%f'



############################################################################################
# SpyList
############################################################################################
class SpyList(SpyProtoRoot):

    def __init__(self,name,default=[SpyInt("")]):
        super().__init__(name,default)
        self._type = default[0].__class__

    @property
    def type_string(self):
        return 'DArray'

    @property
    def default_value(self):
        return '[%s]' % (','.join([str(x.default_value) for x in self._default]))

    @property
    def helper_param(self):
        return "self.%s" % self.name

    @property
    def sv_default_value(self):
        if self._default is not None:
            return f'{{{",".join([str(x.default_value) for x in self._default])}}}'
        else:
            return f'{{{self._type.sv_default_value}}}'

    @property
    def sv_type_string(self):
        return self._type("").sv_type_string

    @property
    def sv_spy_type(self):
        return f'SpyList#({self._type("").sv_type_string}, {self._type("").sv_spy_type})'

    @property
    def sv_var_declr(self):
        return '{:<16s}    {}[]'.format(self.sv_type_string, self.name)

    def sv_report_string(self, name=None):
        if name is None:
            name = self.name
        return f'foreach({name}[i]) $display("{self.name}[%0d]: {self._type("").sv_format_symbol}", i, {name}[i]);'

class SpyDArray(SpyList):

    @property
    def default_value(self):
        return 'SpyInst.SpyDArrayInst(StreamHelper.%sStreamHelper,%s)' % (self._type("").type_string,','.join([str(x.default_value) for x in self._default]))



############################################################################################
# SpyClass
############################################################################################
class SpyClass(SpyProtoRoot):

    def __init__(self,name):
        super().__init__(name,None)
        self._content_dict = {}

    @property
    def type_string(self):
        return 'Class'

    @property
    def default_value(self):
        return "%s()" % self.__class__.__name__

    def register(self,value,field):
        self._content_dict[field] = value

    @property
    def content_as_list(self):
        return list(self._content_dict.values())

    @property
    def content_as_dict(self):
        return list(self._content_dict.items())

    def python_class(self):
        env = Environment(loader=PackageLoader('Spy','template'))
        template = env.get_template('class_template.jinja2')
        text = template.render(ast=self)
        return text

    @property
    def helper_param(self):
        return "self.%s" % self.name

    def sv_class(self):
        env = Environment(loader=PackageLoader('Spy', 'template'))
        template = env.get_template('class_template.sv')
        text = template.render(ast=self, builtins=builtins)
        return text

    @property
    def sv_type_string(self):
        return self.__class__.__name__

    @property
    def sv_default_value(self):
        # return f'new({",".join([str(x.default_value) for x in self.content_as_list])})'
        return 'new()'

    def sv_report_string(self, name=None):
        content = []
        if name is None:
            return [var.sv_report_string(var.name) for var in self.content_as_list]
        else:
            return f'{self.name}.report();'
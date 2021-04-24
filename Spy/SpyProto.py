from jinja2     import PackageLoader,Environment


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



############################################################################################
# SpyInt
############################################################################################
class SpyInt(SpyProtoRoot):

    def __init__(self,name,default=0):
        super().__init__(name,default)

    @property
    def type_string(self):
        return 'Int'



############################################################################################
# SpyFloat
############################################################################################
class SpyFloat(SpyProtoRoot):

    def __init__(self,name,default=0):
        super().__init__(name,default)

    @property
    def type_string(self):
        return 'Float'


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

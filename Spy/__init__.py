
from . import SpyStreamHelper
from . import SpyProto
from . import SpyProto

def generate_python(path,*templates):
    head = 'from Spy import StreamHelper,SpyInst'
    template_string = '\n\n\n'.join([template().python_class() for template in templates])
    with open(path,'w') as f:
        f.write(head + template_string)




from . import SpyStreamHelper
from . import SpyProto
from . import SpyProto

from .SpyPipe.SpyPipeServer import RemoteStorage,SpyPipeServer

def generate_python(path,*templates):
    head = 'from Spy import StreamHelper,SpyInst'
    template_string = '\n\n\n'.join([template().python_class() for template in templates])
    with open(path,'w') as f:
        f.write(head + template_string)

def generate_sv(path,*templates):
    head = 'import SpyLib::*;\n'
    template_string = '\n\n\n'.join([template().sv_class() for template in templates])
    with open(path,'w') as f:
        f.write(head + template_string)



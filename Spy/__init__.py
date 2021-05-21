
from . import SpyStreamHelper
from . import SpyProto
from . import SpyProto

from .SpyPipe.SpyPipeServer import RemoteStorage,SpyPipeServer

def generate_python(path,*templates,one_file=True):
    if one_file == True:
        import os

        line = ['']
        with open('%s/SpyStreamHelper.py' % os.path.dirname(__file__),'r') as f:
            content_in_line = f.readlines()
            line += content_in_line[0:9]
            line += ['class SpyStreamHelper(object):\n']
            line += ['    %s' % x for x in content_in_line[10:]]
            #print(content_in_line)
        line += ['class SpyInst(object):\n']
        with open('%s/SpyInst.py' % os.path.dirname(__file__),'r') as f:
            content_in_line = f.readlines()
            line += ['    %s' % x  for x in content_in_line[10:]]

        head = ''.join(line)
        
    else:
        head = 'from Spy import SpyStreamHelper,SpyInst'
    template_string = '\n\n\n'.join([template().python_class() for template in templates])
    with open(path,'w') as f:
        f.write(head + template_string)

def generate_sv(path,*templates,one_file=True):
    head = 'import SpyLib::*;\n'
    template_string = '\n\n\n'.join([template().sv_class() for template in templates])
    with open(path,'w') as f:
        f.write(head + template_string)



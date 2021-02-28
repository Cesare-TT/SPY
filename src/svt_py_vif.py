import builtins
from pprint import pprint
from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import FileSystemLoader

from .sv_type import *

class SvtPyVif(sv_type):
    def __init__(self, value=None, name="") -> None:
        super().__init__(value=value, name=name)
        object.__setattr__(self, 'var_dict', dict())


    def __setattr__(self, name: str, value) -> None:
        value_wrap = self._type_mapping(value)
        if isinstance(value_wrap, (sv_type,)):
            value_wrap = self._type_mapping(value)
            object.__setattr__(value_wrap, 'name', name)
            object.__setattr__(value_wrap, 'parent', self)
            self.var_dict[name] = value_wrap
        return super().__setattr__(name, value)

    def get_sv_type(self):
        return self.__class__.__name__

    def show_var_list(self):
        for item in self.var_dict.values():
            item.show_var_list()

    def render_value(self):
        render_content = list()
        for item in self.var_dict.values():
            render_content.append(item.render_value())
        return '\n'.join(render_content)

    def render_instantiate(self, inst=None):
        render_content = list()
        if inst is None:
            inst = self
        else:
            render_content.append(f'{self.get_relative_name(inst)} = new();')
        for item in self.var_dict.values():
            content = item.render_instantiate(inst)
            if content:
                render_content.extend(content)
        return render_content

    def render_load_value(self, sv_name=None, inst=None):
        render_content = list()
        if inst is None:
            inst = self
        else:
            return [f'{self.get_relative_name(inst)}.load_value(path, "{self.get_full_name()}")']
        for var in self.var_dict.values():
            content = var.render_load_value(inst=inst)
            if content:
                render_content.extend(content)
        return render_content

    def render_sv_class(self):
        render_content = dict()
        env = Environment(loader=PackageLoader('src', 'template'))
        template = env.get_template('template.sv')
        template.globals['builtins'] = builtins
        template.globals['sv_type'] = sv_type
        template.globals['sv_int'] = sv_int
        template.globals['sv_str'] = sv_int
        template.globals['sv_real'] = sv_real
        template.globals['sv_array'] = sv_array
        render_content[self.get_sv_type()] = template.render(sv_class=self)
        for item in self.var_dict.values():
            content = item.render_sv_class()
            if content:
                for class_name, class_content in content.items():
                    render_content[class_name] = class_content
        return render_content

    def gen_var_list(self, file_name):
        f = open(file_name, 'w')
        f.write(self.render_value())
        f.close()

    def gen_sv_class(self, file_name):
        f = open(file_name, 'w')
        f.write('\n\n'.join(reversed(self.render_sv_class().values())))
        f.close()

if __name__ == '__main__':
    sv = SvtPyVif()
    sv.attr0 = 0
    sv.attr1 = "1"
    sv.attr2 = [2, 3]
    sv.attr3 = 0.1
    sv.get_cfg()
    sv.gen_cfg('test.cfg')
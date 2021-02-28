import re
from pprint import pprint

# __available_type__ = (int, float, str, list, dict, tuple)

class sv_type(object):
    def __init__(self, value=None, name='') -> None:
        super().__init__()
        object.__setattr__(self, 'parent', None)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'value', value)

    def _type_mapping(self, value):
        if isinstance(value, int):
            value_wrap = sv_int(value)
        elif isinstance(value, str):
            value_wrap = sv_str(value)
        elif isinstance(value, float):
            value_wrap = sv_real(value)
        elif isinstance(value, (list, dict, tuple)):
            value_wrap = sv_array(value)
        else:
            value_wrap = value
        return value_wrap

    def show_var_list(self):
        pprint(f'{self.get_full_name()}: {self.value}')

    def get_full_name(self):
        if self.parent is None:
            return self.name
        else:
            joint_mark = '' if re.match(r'^\[\S+\]$', self.name) else '.'
            return f'{self.parent.get_full_name()}{joint_mark}{self.name}'

    def get_relative_name(self, inst):
        if isinstance(inst, sv_type):
            return self.get_full_name().replace(f'{inst.get_full_name()}.', '')
        else:
            raise TypeError('inst should be sv_type or extend from sv_type!')

    def get_sv_type(self):
        return None

    def render_instantiate(self, inst=None):
        return None

    def render_declare(self):
        return '{:<12s}{};'.format(self.get_sv_type(), self.name)

    def render_value(self):
        return f'{self.get_full_name()}={self.value}'

    def render_sv_class(self):
        return None

    def render_load_value(self):
        return None

class sv_int(sv_type):
    def __init__(self, value=None, name='') -> None:
        super().__init__(value=value, name=name)
        if not isinstance(value, int):  raise TypeError('value of sv_int must be int type!')

    def get_sv_type(self):
        return 'int'

    def render_load_value(self, sv_name=None, inst=None):
        if sv_name is None:
            sv_name = self.name
        return ['$sscanf(content, $sformatf("%s.{}=%%d", hierarchy), {})'.format(self.get_relative_name(inst).replace('"', r'\"'), sv_name)]

class sv_real(sv_type):
    def __init__(self, value=None, name='') -> None:
        super().__init__(value=value, name=name)
        if not isinstance(value, float):    raise TypeError('value of sv_real must be float type!')

    def get_sv_type(self):
        return 'real'

    def render_load_value(self, sv_name=None, inst=None):
        if sv_name is None:
            sv_name = self.name
        return ['$sscanf(content, $sformatf("%s.{}=%%f", hierarchy), {})'.format(self.get_relative_name(inst).replace('"', r'\"'), sv_name)]

class sv_str(sv_type):
    def __init__(self, value=None, name='') -> None:
        super().__init__(value=value, name=name)
        if not isinstance(value, str):  raise TypeError('value of sv_str must be str type!')
        self.value = f'"{self.value}"'

    def get_sv_type(self):
        return 'string'

    def render_load_value(self, sv_name=None, inst=None):
        if sv_name is None:
            sv_name = self.name
        return ['$sscanf(content, $sformatf("%s.{}=%%s", hierarchy), {})'.format(self.get_relative_name(inst).replace('"', r'\"'), sv_name)]

class sv_array(sv_type):
    def __init__(self, value=None, name='') -> None:
        super().__init__(value=value, name=name)
        if not isinstance(value,(list,tuple,dict)): raise TypeError('value of sv_array must be list or dict or tuple!')
        self.value = dict()

        # TODO type check to do

        if isinstance(value, (list, tuple)):
            for index,element in enumerate(value):
                index_wrap = self._type_mapping(index)
                element_wrap = self._type_mapping(element)
                object.__setattr__(element_wrap, 'name', f'[{index_wrap.value}]')
                object.__setattr__(element_wrap, 'parent', self)
                self.value[index_wrap] = element_wrap

        elif isinstance(value, dict):
            for index,element in value.items():
                index_wrap = self._type_mapping(index)
                element_wrap = self._type_mapping(element)
                object.__setattr__(element_wrap, 'name', f'[{index_wrap.value}]')
                object.__setattr__(element_wrap, 'parent', self)
                self.value[index_wrap] = element_wrap

    def get_sv_type(self):
        return list(self.value.values())[0].get_sv_type()

    def show_var_list(self):
        for k,v  in self.value.items():
            v.show_var_list()

    def render_value(self):
        render_content = list()
        for k,v  in self.value.items():
            render_content.append(v.render_value())
        return '\n'.join(render_content)

    def render_declare(self):
        for k, v in self.value.items():
            return '{:<12s}{}[{}];'.format(v.get_sv_type(), self.name, k.get_sv_type())

    def render_instantiate(self, inst=None):
        render_content = list()
        for k, v  in self.value.items():
            content = v.render_instantiate(inst)
            if content:
                render_content.extend(content)
        return render_content

    def render_load_value(self, inst=None):
        render_content = list()
        for k, v in self.value.items():
            content = v.render_load_value(f'{self.name}{v.name}', inst)
            if content:
                render_content.extend(content)
        return render_content

    def render_sv_class(self):
        for k, v in self.value.items():
            content = v.render_sv_class()
            if content:
                for class_name, class_content in content.items():
                    return {class_name: class_content}
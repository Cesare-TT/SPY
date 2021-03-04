import re
import builtins
from pprint import pprint
from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import FileSystemLoader

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
        relative_name = list()
        node = self
        while (node.parent is not inst):
            relative_name.append(node.name)
            relative_name.append('' if re.match(r'^\[\S+\]$', node.name) else '.')
            node = node.parent
        relative_name.append(node.name)
        relative_name.reverse()
        return ''.join(relative_name)

    def get_sv_type(self):
        return None

    def get_sv_string_field(self, inst_type):
        if inst_type == 'int':
            return r'%d'
        elif inst_type == 'real':
            return r'%f'
        elif inst_type == 'string':
            return r'%s'

    def render_instantiate(self, root=None, inst=None):
        return None

    def render_declare(self, sv_name=None, inst=None):
        return ['{:<12s}    {};'.format(self.get_sv_type(), self.name)]

    def render_declare_index(self, inst=None, tag=0):
        return None

    def render_value(self):
        return f'{self.get_full_name()}={self.value}'

    def render_sv_class(self):
        return None

    def render_scan_value(self, root=None, inst=None):
        return None

    def render_load_value(self, root=None, inst=None):
        return None
    
    def render_print_value(self, root=None, inst=None):
        if isinstance(inst, (SvtPyVif,)):
            quote = r'\"' if isinstance(self, sv_str) else ''
            return ['$display("%s.{} = {}{}{}", hierarchy, {});'.format(self.get_relative_name(inst).replace('"', r'\"'), quote, self.get_sv_string_field(self.get_sv_type()).replace("%", "%0"), quote, self.name)]
        elif isinstance(inst, (sv_array,)):
            attr_name = inst.get_relative_name(root).replace('"', r'\"')
            key_filed = inst.get_key_field()
            scan_string_index = ''.join(f'[{i.replace("%", "%0")}]' for i in key_filed)
            string_index = ''.join(f'[{i}]' for i in inst.sv_index_list)
            content = list()
            load_content = '$display("%s.{}{} = {}", hierarchy, {}, {}{});'.format(attr_name, scan_string_index, self.get_sv_string_field(self.get_sv_type()).replace("%", "%0"), ', '.join(inst.sv_index_list), attr_name, string_index)
            intent = ''
            for index in [f'[{i}]' for i in inst.sv_index_list]:
                content.append(f'{intent}foreach ({attr_name}{index})')
                intent = f'    {intent}'
                attr_name = f'{attr_name}{index}'
            content.append(f'{intent}{load_content}')
            return content

class sv_int(sv_type):
    def __init__(self, value=None, name='') -> None:
        super().__init__(value=value, name=name)
        if not isinstance(value, int):  raise TypeError('value of sv_int must be int type!')

    def get_sv_type(self):
        return 'int'

    def render_scan_value(self, root=None, inst=None):
        if isinstance(inst, (SvtPyVif,)):
            return ['if ($sscanf(content, $sformatf("%s.{}=%%d", hierarchy), {})) continue;'.format(self.get_relative_name(inst).replace('"', r'\"'), self.name)]
        elif isinstance(inst, (sv_array,)):
            attr_name = inst.get_relative_name(root).replace('"', r'\"')
            key_filed = inst.get_key_field()
            scan_string_index = ''.join(f'[%{i}]' for i in key_filed)
            string_index = ''.join(f'[{i}]' for i in inst.sv_index_list)
            return ['if ($sscanf(content, $sformatf("%s.{}{}=%%d", hierarchy), {}, {})) continue;'.format(attr_name, scan_string_index, ', '.join(inst.sv_index_list), f'{attr_name}{string_index}')]

class sv_real(sv_type):
    def __init__(self, value=None, name='') -> None:
        super().__init__(value=value, name=name)
        if not isinstance(value, float):    raise TypeError('value of sv_real must be float type!')

    def get_sv_type(self):
        return 'real'

    def render_scan_value(self, root=None, inst=None):
        if isinstance(inst, (SvtPyVif,)):
            return ['if ($sscanf(content, $sformatf("%s.{}=%%f", hierarchy), {})) continue;'.format(self.get_relative_name(inst).replace('"', r'\"'), self.name)]
        elif isinstance(inst, (sv_array,)):
            attr_name = inst.get_relative_name(root).replace('"', r'\"')
            key_filed = inst.get_key_field()
            scan_string_index = ''.join(f'[%{i}]' for i in key_filed)
            string_index = ''.join(f'[{i}]' for i in inst.sv_index_list)
            return ['if ($sscanf(content, $sformatf("%s.{}{}=%%f", hierarchy), {}, {})) continue;'.format(attr_name, scan_string_index, ', '.join(inst.sv_index_list), f'{attr_name}{string_index}')]

class sv_str(sv_type):
    def __init__(self, value=None, name='') -> None:
        super().__init__(value=value, name=name)
        if not isinstance(value, str):  raise TypeError('value of sv_str must be str type!')
        object.__setattr__(self, 'value', f'$${len(value)}$$"{value}"')

    @property
    def len(self):
        return len(self.value)

    def get_sv_type(self):
        return 'string'

    def render_declare(self, sv_name=None, inst=None):
        return ['{:<12s}    {};'.format(self.get_sv_type(), self.name)]

    def render_scan_value(self, root=None, inst=None):
        if isinstance(inst, (SvtPyVif,)):
            return ['if ($sscanf(content, $sformatf("%s.{}=$$%%d$$%%s", hierarchy), len, tmp)) begin'.format(self.get_relative_name(inst).replace('"', r'\"')),
                    '    if ($sscanf(content, $sformatf("%s.{}=$$%d$$\\\"%%%0ds\\\"", hierarchy, len, len), {})) begin'.format(self.get_relative_name(inst).replace('"', r'\"'), self.name),
                    '        continue;',
                    '    end',
                    'end']
        elif isinstance(inst, (sv_array,)):
            attr_name = inst.get_relative_name(root).replace('"', r'\"')
            key_filed = inst.get_key_field()
            scan_string_index = ''.join(f'[%{i}]' for i in key_filed)
            string_index_field = ''.join(f'[{i}]' for i in key_filed)
            # sformat_string_index = ''.join(f'[{i}]' for i in inst.sv_index_list)
            string_index = ''.join(f'[{i}]' for i in inst.sv_index_list)
            return ['if ($sscanf(content, $sformatf("%s.{}{}=$$%%d$$%%s", hierarchy), {}, len, tmp)) begin'.format(attr_name, scan_string_index, ', '.join(inst.sv_index_list)),
                    '    if ($sscanf(content, $sformatf("%s.{}{}=$$%d$$\\\"%%%0ds\\\"", hierarchy, {}, len, len), {})) begin'.format(attr_name, string_index_field, ', '.join(inst.sv_index_list), f'{attr_name}{string_index}'),
                    '        continue;',
                    '    end',
                    'end']

class sv_array(sv_type):
    def __init__(self, value=None, name='') -> None:
        super().__init__(value=value, name=name)
        if not isinstance(value,(list,tuple,dict)): raise TypeError('value of sv_array must be list or dict or tuple!')
        # self.value = dict()
        object.__setattr__(self, 'value', dict())
        object.__setattr__(self, 'sv_index_list', list())

        # TODO type check to do

        if isinstance(value, (list, tuple)):
            for index, element in enumerate(value):
                index_wrap = self._type_mapping(index)
                element_wrap = self._type_mapping(element)
                object.__setattr__(element_wrap, 'name', f'[{index_wrap.value}]')
                object.__setattr__(element_wrap, 'parent', self)
                self.value[index_wrap] = element_wrap

        elif isinstance(value, dict):
            for index, element in value.items():
                if isinstance(index, (int, float)):
                    index_wrap = self._type_mapping(index)
                    element_wrap = self._type_mapping(element)
                    object.__setattr__(element_wrap, 'name', f'[{index_wrap.value}]')
                    object.__setattr__(element_wrap, 'parent', self)
                    self.value[index_wrap] = element_wrap
                else:
                    raise TypeError(f'{index.__class__.__name__} key is not supported. key of associate array should be int or real type!')

    def get_sv_type(self):
        return list(self.value.values())[0].get_sv_type()

    def get_key_type(self):
        key_type = list()
        for k,v  in self.value.items():
            key_type.append(k.get_sv_type())
            if isinstance(v, (sv_array,)):
                key_type.extend(v.get_key_type())
            for i in range(len(key_type)):
                if f'index_{self.name}_{i}' not in self.sv_index_list:
                    self.sv_index_list.append(f'index_{self.name}_{i}')
            return key_type

    def get_key_field(self):
        key_type = self.get_key_type()
        key_field = list()
        for key in key_type:
            key_field.append(self.get_sv_string_field(key))
        return key_field

    def show_var_list(self):
        for k,v  in self.value.items():
            v.show_var_list()

    def render_value(self):
        render_content = list()
        for k,v  in self.value.items():
            render_content.append(v.render_value())
        return '\n'.join(render_content)

    def render_declare(self, sv_name=None, inst=None):
        render_content = list()
        if inst is None:
            for k, v in self.value.items():
                if isinstance(v, (sv_int, sv_real, sv_str, SvtPyVif)):
                    render_content.append('{:<12s}    {}[{}];'.format(v.get_sv_type(), self.name, k.get_sv_type()))
                elif isinstance(v, (sv_array,)):
                    render_content.extend(v.render_declare(sv_name=f'{self.name}[{k.get_sv_type()}]', inst=self))
                render_content.extend(self.render_declare_index())
                return render_content
        else:
            for k, v in self.value.items():
                render_content.append('{:<12s}    {}[{}];'.format(v.get_sv_type(), sv_name, k.get_sv_type()))
                return render_content

    def render_declare_index(self, inst=None, tag=0):
        if inst is None:
            inst = self
        render_content = list()
        for k, v in self.value.items():
            render_content.append('{:<12s}    index_{}_{};'.format(k.get_sv_type(), inst.name, tag))
            # inst.sv_index_list.append('index_{}_{}'.format(inst.name, tag))
            content = v.render_declare_index(inst, tag+1)
            if content:
                render_content.extend(content)
            return render_content

    def render_instantiate(self, root=None, inst=None):
        render_content = list()
        for k, v  in self.value.items():
            content = v.render_instantiate(root, inst)
            if content:
                render_content.extend(content)
        return render_content

    def render_scan_value(self, root=None, inst=None):
        if not isinstance(inst, sv_array):
            inst = self
        render_content = list()
        for k, v in self.value.items():
            content = v.render_scan_value(root, inst)
            if content:
                render_content.extend(content)
            return render_content

    def render_load_value(self, root=None, inst=None):
        if not isinstance(inst, sv_array):
            inst = self
        render_content = list()
        for k, v in self.value.items():
            content = v.render_load_value(root, inst)
            if content:
                render_content.extend(content)
            return render_content

    def render_print_value(self, root=None, inst=None):
        if not isinstance(inst, sv_array):
            inst = self
        render_content = list()
        for k, v in self.value.items():
            content = v.render_print_value(root, inst)
            if content:
                render_content.extend(content)
            return render_content

    def render_sv_class(self, inst=None):
        for k, v in self.value.items():
            content = v.render_sv_class()
            if content:
                for class_name, class_content in content.items():
                    return {class_name: class_content}

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

    def render_instantiate(self, root=None, inst=None):
        if root is None:
            root = self
            inst = self
        else:
            if isinstance(inst, (SvtPyVif,)):
                return ['{} = new();'.format(self.get_relative_name(root).replace('"', r'\"'))]
            elif isinstance(inst, (sv_array,)):
                return ['{}{} = new();'.format(inst.get_relative_name(root).replace('"', r'\"'), ''.join(f'[{i}]' for i in inst.sv_index_list))]
        render_content = list()
        for var in self.var_dict.values():
            content = var.render_instantiate(root, inst)
            if content:
                render_content.extend(content)
        return render_content

    def render_scan_value(self, root=None, inst=None):
        if root is None:
            root = self
            inst = self
        else:
            if isinstance(inst, (SvtPyVif,)):
                return ['if ($sscanf(content, $sformatf("%s.{}%%s", hierarchy), tmp)) {}'.format(self.get_relative_name(root).replace('"', r'\"'), ''.join(['{}'.format(item) for item in self.render_instantiate(root, inst)]))]
            elif isinstance(inst, (sv_array,)):
                attr_name = inst.get_relative_name(root).replace('"', r'\"')
                key_filed = inst.get_key_field()
                scan_string_index = ''.join(f'[%{i}]' for i in key_filed)
                string_index = ''.join(f'[{i}]' for i in inst.sv_index_list)
                return ['if ($sscanf(content, $sformatf("%s.{}{}%%s", hierarchy), {}, tmp)) begin'.format(attr_name, scan_string_index, ', '.join(inst.sv_index_list)),
                        '    if (!{}{}) begin'.format(attr_name, string_index),
                        ''.join(['        {}'.format(item) for item in self.render_instantiate(root, inst)]),
                        '    end',
                        'end']
        render_content = list()
        for var in self.var_dict.values():
            content = var.render_scan_value(root, inst)
            if content:
                render_content.extend(content)
        return render_content

    def render_load_value(self, root=None, inst=None):
        render_content = list()
        if root is None:
            root = self
            inst = self
        else:
            if isinstance(inst, (SvtPyVif,)):
                return [f'{self.get_relative_name(root)}.load_value(path, "{self.get_full_name()}");']
            elif isinstance(inst, (sv_array,)):
                attr_name = inst.get_relative_name(root).replace('"', r'\"')
                key_filed = inst.get_key_field()
                scan_string_index = ''.join(f'[{i.replace("%", "%0")}]' for i in key_filed)
                string_index = ''.join(f'[{i}]' for i in inst.sv_index_list)
                content = list()
                load_content = '{}{}.load_value(path, $sformatf("%s.{}{}", hierarchy, {}));'.format(attr_name, string_index, attr_name, scan_string_index, ', '.join(inst.sv_index_list))
                intent = ''
                for index in [f'[{i}]' for i in inst.sv_index_list]:
                    content.append(f'{intent}foreach ({attr_name}{index})')
                    intent = f'    {intent}'
                    attr_name = f'{attr_name}{index}'
                content.append(f'{intent}{load_content}')
                return content
        for var in self.var_dict.values():
            content = var.render_load_value(root, inst)
            if content:
                render_content.extend(content)
        return render_content

    def render_print_value(self, root=None, inst=None):
        render_content = list()
        if root is None:
            root = self
            inst = self
        else:
            if isinstance(inst, (SvtPyVif,)):
                return [f'{self.get_relative_name(root)}.print_value("{self.get_full_name()}");']
            elif isinstance(inst, (sv_array,)):
                attr_name = inst.get_relative_name(root).replace('"', r'\"')
                key_filed = inst.get_key_field()
                scan_string_index = ''.join(f'[{i.replace("%", "%0")}]' for i in key_filed)
                string_index = ''.join(f'[{i}]' for i in inst.sv_index_list)
                content = list()
                load_content = '{}{}.print_value($sformatf("%s.{}{}", hierarchy, {}));'.format(attr_name, string_index, attr_name, scan_string_index, ', '.join(inst.sv_index_list))
                intent = ''
                for index in [f'[{i}]' for i in inst.sv_index_list]:
                    content.append(f'{intent}foreach ({attr_name}{index})')
                    intent = f'    {intent}'
                    attr_name = f'{attr_name}{index}'
                content.append(f'{intent}{load_content}')
                return content
        for var in self.var_dict.values():
            content = var.render_print_value(root, inst)
            if content:
                render_content.extend(content)
        return render_content

    def render_sv_class(self):
        render_content = dict()
        env = Environment(loader=PackageLoader('svt_py_vif', 'template'))
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
        f.write('\n\n'.join(reversed(list(self.render_sv_class().values()))))
        f.close()
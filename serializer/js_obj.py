from typing import Mapping, Sequence

from serializer.utils import Empty


class JsObj(Mapping):
    '''
    一个类似于JavaScript中的对象
    实现了collections.abc.Mapping的所有接口,同时也是一个类字典对象
    '''

    def __init__(self, dictionary: Mapping = None, default=Empty):
        '''
        json_dict:dict：原生json字典
        default:获取不到时指定的默认值
        '''
        if isinstance(dictionary, JsObj):
            dictionary = dictionary.dictionary
        self.__dict__['dictionary'] = dictionary if dictionary is not None else {}
        self.__dict__['default'] = default

    def __getattr__(self, attr):
        '''
        重写了该方法，当属性不存在的时候如果有default则返回default
        :param attr:
        :return:
        '''
        value = self.dictionary.get(attr, None)
        if isinstance(value, Mapping):
            value = JsObj(value, default=self.default)
        if value is None and self.default != Empty:
            return self.default
        return value

    def __setattr__(self, key, value):
        if isinstance(value, JsObj):
            value = value.dictionary
        self.dictionary[key] = value

    def __bool__(self):
        return bool(self.dictionary)

    def __getitem__(self, value):
        return self.__getattr__(value)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __delitem__(self, key):
        return self.dictionary.__delitem__(key)

    def __len__(self):
        return len(self.dictionary)

    def __iter__(self):
        return iter(self.dictionary)

    def __contains__(self, item):
        return self.dictionary.__contains__(item)

    def __eq__(self, other):
        return self.dictionary.__eq__(other)

    def __str__(self):
        return self.dictionary.__str__()

    def get(self, key: str, default=None):
        try:
            return self.dictionary[key]
        except KeyError:
            return default

    def set(self, key, value):
        return self.__setattr__(key, value)

    def keys(self):
        return self.dictionary.keys()

    def items(self):
        return self.dictionary.items()

    def values(self):
        return self.dictionary.values()

    def pop(self, key: str, default=None):
        '''
        default设为None，确保默认不出错
        '''
        return self.dictionary.pop(key, default)

    def update(self, kwargs: Mapping):
        if isinstance(kwargs, JsObj):
            kwargs = kwargs.dictionary
        self.dictionary.update(**kwargs)

    def to_json(self):
        result = {}
        for key, value in self.dictionary.items():
            if isinstance(value, JsObj):
                result[key] = value.to_json()
            elif isinstance(value, Sequence):
                result[key] = [item if not isinstance(item, JsObj) else item.to_json() for item in value]
            else:
                result[key] = value
        return result
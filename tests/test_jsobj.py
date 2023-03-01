import random

import pytest

from serializer.js_obj import JsObj


@pytest.fixture
def random_dict(faker, random_key, random_value):
    data = faker.pydict()
    data[random_key] = random_value
    return data


@pytest.fixture
def random_key(faker):
    return faker.pystr()


@pytest.fixture
def random_key2(faker):
    return faker.pystr()


@pytest.fixture
def random_list(faker):
    return [
        faker.pydict(),
        faker.pybool(),
        faker.pydecimal(),
        faker.pyfloat(),
        faker.pyint(),
        faker.pystr(),
        faker.pylist(),
    ]


@pytest.fixture
def random_value(random_list):
    return random.choice(random_list)


def test_empty_init():
    obj = JsObj()
    assert obj == {}


def test_init_use_dict(random_dict):
    obj = JsObj(random_dict.copy())
    for key, value in random_dict.items():
        assert getattr(obj, key) == value


def test_init_use_js_obj(random_dict):
    obj = JsObj(JsObj(random_dict))
    assert obj.dictionary == random_dict


def test_get_not_exist_field(random_key):
    obj = JsObj()
    assert getattr(obj, random_key) is None


def test_get_not_exist_has_default(random_key):
    obj = JsObj(default=1)
    assert getattr(obj, random_key) == 1


def test_get_exist_field(random_dict, random_key):
    obj = JsObj(random_dict.copy())
    assert getattr(obj, random_key) == random_dict[random_key]


def test_get_dict_change_to_js_obj(random_dict, random_key):
    obj = JsObj()
    setattr(obj, random_key, random_dict)
    assert isinstance(getattr(obj, random_key), JsObj)


def test_set_field(random_key, random_value):
    obj = JsObj()
    setattr(obj, random_key, random_value)
    assert getattr(obj, random_key) == random_value


def test_set_js_obj(random_key):
    obj = JsObj()
    setattr(obj, random_key, JsObj())
    assert obj.dictionary == {random_key: {}}


def test_bool(random_dict):
    assert bool(JsObj({})) is False
    assert bool(JsObj(random_dict)) is True


def test_getitem(random_dict, random_key, random_value):
    assert JsObj(random_dict)[random_key] == random_value


def test_delitem(random_dict, random_key, random_value):
    obj = JsObj(random_dict)
    del obj[random_key]
    assert random_key not in obj


def test_len(random_dict):
    assert len(JsObj(random_dict)) == len(random_dict)


def test_iter(random_dict):
    assert list(iter(JsObj(random_dict.copy()))) == list(iter(random_dict))


def test_str(random_dict):
    obj = JsObj(random_dict)
    assert str(obj) == str(random_dict)


def test_get_method(random_key, random_value):
    obj = JsObj({random_key: random_value})
    assert obj[random_key] == getattr(obj, random_key)


def test_get_dict(random_key, random_dict):
    obj = JsObj({random_key: random_dict})
    assert obj[random_key] == getattr(obj, random_key)


def test_set_method(random_key, random_value):
    obj = JsObj()
    setattr(obj, random_key, random_value)
    assert obj[random_key] == getattr(obj, random_key)


def test_keys(random_dict):
    keys = random_dict.keys()
    obj = JsObj(random_dict)
    assert obj.keys() == keys


def test_items(random_dict):
    items = random_dict.items()
    obj = JsObj(random_dict)
    assert obj.items() == items


def test_values(random_dict):
    values = random_dict.values()
    obj = JsObj(random_dict)
    # dict_values __eq__ NotImplemented
    assert list(values) == list(obj.values())


def test_pop(random_key, random_value):
    obj = JsObj({random_key: random_value})
    obj.pop(random_key)
    assert random_key not in obj


def test_to_json(random_key, random_key2, random_value, random_dict):
    data = {
        random_key: random_value,
        random_key2: random_dict
    }
    obj = JsObj(data)
    assert obj.to_json() == data


def test_to_json_value_is_list(random_list, random_key):
    data = {random_key: random_list}
    obj = JsObj(data)
    return obj.to_json() == data

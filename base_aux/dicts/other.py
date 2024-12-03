


# =====================================================================================================================
class DictDotAttrAccess(dict):  # STARICHENKO
    """dot.notation access to dictionary attributes.
    first variant!
    CANT CREATE SINGLETON!

    cant create singleton!!! i was trying!!! even by typical def __***

    typical usage:
        my_dict = {'param1': 'GOOD'}
        nested_dict = {'param1': 'nested GOOD too'}
        print(my_dict)  # {'param1': 'GOOD'}

        # EXECUTE
        my_dict = DictDotAttrAccess(my_dict)

        # READING
        print(my_dict)  # {'param1': 'GOOD'}
        print(my_dict.param1)  # 'GOOD'
        print(my_dict["param1"])  # 'GOOD'

        # CHANGE
        my_dict.param1 = 123
        print(my_dict)  # {'param1': 123}
        print(my_dict.param1)  # 123
        my_dict["param1"] = 1000
        print(my_dict)  # {'param1': 1000}
        print(my_dict.param1)  # 1000

        # NESTED
        my_dict.nested = nested_dict
        print(my_dict)  # {'param1': 1000, 'nested': {'param1': 'nested GOOD too'}}
        # print(my_dict.nested.param1)  # AttributeError: 'dict' object has no attribute 'param1'

        my_dict.nested = DictDotAttrAccess(nested_dict)
        print(my_dict)  # {'param1': 1000, 'nested': {'param1': 'nested GOOD too'}}
        print(my_dict.nested.param1)  # 'nested GOOD too'

    ОСОБЕННОСТИ:
        +++И ТАК РАБОТАЛО
            1. +BLANK
                my_dict = DictDotAttrAccess()
                print(my_dict)  # {}

            2. +BOOL
                my_dict = DictDotAttrAccess()
                print(bool(my_dict))  # False

                my_dict = DictDotAttrAccess({'p1': '111'})
                print(my_dict)  # {'p1': '111'}
                print(bool(my_dict))  # True

            3. +IN LIST
                my_dict = {'p1': '111'}
                my_dict = DictDotAttrAccess(my_dict)
                print(my_dict)  # {'p1': '111'}

                print("p1" in my_dict)  # True

            5. +при обращении к НЕCУЩЕСТВУЮЩЕМУ - выдает None! без добавления параметра, а после присвоения - параметр создается
                my_dict = {'p1': '111'}
                my_dict = DictDotAttrAccess(my_dict)
                print(my_dict)  # {'p1': '111'}

                print(my_dict.p2)  #None
                print(my_dict)  #{'p1': '111'}
                my_dict.p2 = 222
                print(my_dict)  #{'p1': '111', 'p2': 222}

            6. +UPDATE
                my_dict= DictDotAttrAccess()
                print(my_dict)  # {}

                my_dict.update({1:1})
                print(my_dict)  # {1: 1}

            6. +POP
                my_dict = DictDotAttrAccess({1:1})

                my_dict.pop(1)
                print(my_dict)  # {}

            8. +ITEMS()
                my_dict = DictDotAttrAccess({'p1': '111'})
                print(my_dict.items())  #dict_items([('p1', '111')])

        +++ПРИШЛОСЬ ДОБАВИТЬ
            10. +ИТЕРИРОВАТЬ
                my_dict = {'p1': '111'}
                my_dict = DictDotAttrAccess(my_dict)
                print(my_dict)  # {'p1': '111'}

                for i in my_dict:
                    print(i, my_dict.get(i))    # p1 111

            11. +КОПИЮ
                my_dict = {'p1': '111'}
                my_dict = DictDotAttrAccess(my_dict)
                print(my_dict)  # {'p1': '111'}

                my_dict2 = copy.copy(my_dict)
                print(my_dict2)  # {'p1': '111'}


        ---НЕ ПОЛУЧИЛОСЬ РЕАЛИЗОВАТЬ
            20. замену для __MISSING__
                def __missing__(self, key):
                    return "HELLO"

                __missing__ = lambda: "HELLO"
                __missing__ = FUNC_LINK_LAMBDA_REPEATER
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __iter__ = dict.__iter__
    __copy__ = dict.copy

    # __repr__ = dict.__repr__  # и так работает!
    # __str__ = dict.__str__    # и так работает!
    # __len__ = dict.__len__    # и так работает!


# dict-FIND
def dict_find_pattern(
        source,
        pattern,
        find_in_1keys_2values=1,
        nested=False,
        get_flatten=False,
        return_first_found=False,
        return_first_found_path_list=False
):       # starichenko
    """из исходного словаря выбрать только те ключи которые удовлетворяют FullMatch паттерну.

    :param find_in_1keys_2values:
    :param nested: если нужно проверить все вложенные словари - собственно без этого нет особой необходимости
    :param get_flatten: если хотим все привести к одноуровневому словарю

    :param pattern:
        пример r".*\[(.+?)(#[^\]]+)?\].*"
        простой пример r".*_hello_.*"
    """
    result_dict = {}

    for key, value in source.items():
        if nested and isinstance(value, dict):
            result_down_level = dict_find_pattern(
                source=value,
                pattern=pattern,
                find_in_1keys_2values=find_in_1keys_2values,
                nested=nested,
                return_first_found=return_first_found,
                return_first_found_path_list=return_first_found_path_list)

            if return_first_found and result_down_level:
                return {key: result_down_level}
            elif return_first_found_path_list and result_down_level:
                return [key, *result_down_level]
            else:
                result_dict[key] = result_down_level
        else:
            key_str = str(key)
            value_str = str(value)

            if find_in_1keys_2values == 1:
                source_str = value_str
            else:
                source_str = key_str

            match = re.fullmatch(pattern, source_str)
            if match:
                if return_first_found:
                    return value
                elif return_first_found_path_list:
                    return [key, ]
                else:
                    logging_and_print_debug(f"найден подходящий ключ=[{key}] со значением=[{value}] идем дальше")
                    if key not in result_dict or value == result_dict[key]:
                        result_dict.update({key: value})

    # использовать только в конце!!! чтобы можно было использовать словари с одинаковыми ключами в разных глубинах и разными значениями!
    if get_flatten:
        result_dict = dict_flatten(result_dict)

    return result_dict


# dict-SORT ORDER
def dict_order_by_key_list(
        source,
        keys_list=None,
        raise_if_not_exists=True,
        delete_keys_not_listed=False
):        # starichenko
    """reorder dict by keys_list
    typically transform keys in other func and use this funс to order original dict keys!!!"""
    result_dict = dict()
    for key in keys_list:
        if key in source:
            result_dict.update({key: source.pop(key)})
        elif raise_if_not_exists:
            raise Exception(f"not exists key={key}")
    if not delete_keys_not_listed:
        result_dict.update(source)
    return result_dict


def dict_sort_by_num_keys(source):        # starichenko
    """"""
    sorted_keys_list = sorted(source)
    sorted_dict = dict_order_by_key_list(source, keys_list=sorted_keys_list)
    return sorted_dict


# dict-KEYS
def dict_keys_delete_by_name(source, keys_list_or_func_link=None, reverse_decision=False, nested=True):  # starichenko
    """удалить ключи из словаря.

    применяется когда нужно очистить словарь от лишних данных,
    например если мы хотим сделать Flatten словарь в котором есть Title - то там будут ошибки наличия ключей с разными значениями!!

    :param source: source
    :param keys_list_or_func_link: list of keys to delete? to delete None - use [None]!
    :param reverse_decision: if True - delete all keys except listed in keys_list/funk link
    :param nested: if False - walk only root level of source
    """
    # INPUT -----------------------------------------------------------------------------------------------------------
    if not isinstance(source, dict):
        return source

    if not keys_list_or_func_link:
        return source

    result_dict = copy.deepcopy(source)

    # WORK ------------------------------------------------------------------------------------------------------------
    for key in source:
        if keys_list_or_func_link:
            if callable(keys_list_or_func_link):
                decide = keys_list_or_func_link(key)
            elif isinstance(keys_list_or_func_link, (list, tuple, set)):
                decide = key in keys_list_or_func_link
            else:
                decide = key == keys_list_or_func_link
        else:
            decide = False

        if reverse_decision:
            decide = not decide

        if decide:
            result_dict.pop(key)
            continue

    # NESTED ----------------------------------------------------------------------------------------------------------
    if nested:
        for key, value in result_dict.items():
            if isinstance(value, dict):
                result_dict[key] = dict_keys_delete_by_name(
                    source=value,
                    keys_list_or_func_link=keys_list_or_func_link,
                    reverse_decision=reverse_decision,
                    nested=nested
                )

    print(f"{result_dict=}")
    return result_dict


def dict_keys_delete_by_values(**kwargs):        # starichenko
    # raise Exception("use directly dict_values_replace with param DeleteKeys=True")
    return dict_values_replace(**kwargs, delete_found_keys=True)

def dict_key_rename__by_name(source: dict, key: tp.Any, new_key: tp.Any) -> dict:  # starichenko
    result = {}
    for _key, value in source.items():
        if key == _key:
            _key = new_key
        result.update({_key: value})
    return result


def dict_keys_rename__by_func(source: dict, func: tp.Callable[[tp.Any], tp.Any]) -> dict:  # starichenko
    result = {}
    for key, value in source.items():
        key = func(key)
        result.update({key: value})
    return result


def dict_key_get_short_name(key_fullname, subkeys_list=[]):  # starichenko
    """return short name for source key name
    """
    short_name_pattern = r".*\[(.+?)(#[^\]]+)?\].*"

    if isinstance(subkeys_list, (list, dict, tuple, set)):
        subkeys_list = [str(i) for i in subkeys_list]
    else:
        raise Exception(f"неверное значение параметров subkeys_list={subkeys_list}")

    name_short = None

    match = re.fullmatch(short_name_pattern, key_fullname)
    if match:
        name_short_temp = match.group(1)
        subkeys_string_actual = match.group(2)
        if subkeys_string_actual:
            subkeys_list_actual = sequence_delete_items_blank(subkeys_string_actual.replace(' ', '').split("#"))
            logging_and_print_debug(f"-требуется совпадение ключей subkeys_list_actual={subkeys_list_actual}")

            if sequence_check_included_in_supersequence(subkeys_list_actual, subkeys_list):
                logging_and_print_debug(
                    f"+все ключи {subkeys_list_actual} имеются в subkeys_list={subkeys_list} key_fullname=[{key_fullname}]")
                name_short = name_short_temp
            else:
                logging_and_print_debug(
                    f"-НЕ ДОСТАТОЧНО исходных ключей subkeys_list={subkeys_list} в key_fullname=[{key_fullname}] идем дальше")
        else:
            logging_and_print_debug(f"+НЕ требуется совпадения ключей")
            name_short = name_short_temp

    return name_short


def dict_keys_short_names(source, subkeys_list=[], get_flatten=True):   # starichenko
    """выдает словарь с короткими именами ключей (именованными параметрами) если они имеются.
    если параметр не имеет короткого имени - ключ игнорируется!
    все настройки имеющие ключи, если имеют хотябы один ключ не из списка subkeys_list - игнорируются!

    если значения одинаковы - спокойно пропускаем!

    :param source: исходный словарь
    :param subkeys_list: дополнительные параемтры для фильтра,
        фильтр не обязывающий! а позволяющий.
        суть фильтра - если исходный ключ имеет какието подключи, то ключ будет принят, только если ВСЕ они находятся в списке разрешенных!
    :param get_flatten: выдать результат в виде словаря одного уровня

    Пример:
        из словаря  = {"[ps_power_load_psi#1200] Требуемая нагрузка, Вт": 900}
        для subkeys_list=[1200, DC] => {"ps_power_load_psi": 900}
        для subkeys_list=[1600, DC] => {}
    """
    result_dict = dict()

    if get_flatten:
        source = dict_flatten(source)

    for key_fullname, value in source.items():
        key_fullname = str(key_fullname)
        logging_and_print_debug(f"смотрим [{key_fullname}]")

        key_short_name = dict_key_get_short_name(key_fullname, subkeys_list)
        if key_short_name is not None:
            if key_short_name not in result_dict:
                logging_and_print_debug(f"+найдено первое значение [{key_fullname}] идем дальше")
                result_dict.update({key_short_name: value})
            elif result_dict[key_short_name] == value:
                pass    # same value - pass silent!
            else:
                logging_and_print_debug(f"result_dict+key_short_name=[{key_short_name}]=", result_dict[key_short_name])
                logging_and_print_debug(f"source+key_fullname=[{key_fullname}]=", value)
                logging_and_print_warning(f"-в словаре имеется НЕСКОЛЬКО СООТВЕТСТВУЮЩИХ нам параметров с именем {key_short_name} - выходим")
                raise Exception(f"-в словаре имеется НЕСКОЛЬКО СООТВЕТСТВУЮЩИХ нам параметров с именем {key_short_name} - выходим")
        else:
            logging_and_print_debug(f"в словаре найден элемент без именованного значения (неподходящего для subkeys_list={subkeys_list})! [{key_fullname}]")

    if result_dict == dict():
        logging_and_print_warning(f"---в словаре НЕ НАЙДЕНО именованных параметров с ключами subkeys_list={subkeys_list}")
    else:
        logging_and_print_debug(f"+в словаре НАЙДЕНЫ ИМЕНОВАННЫЕ параметры с subkeys_list={subkeys_list} result_dict={result_dict}")

    return result_dict


# COMPARE ----------------------------
def dicts_compare_full(
        target: dict,
        compare: dict,
        func: tp.Optional[tp.Callable[[tp.Any, tp.Any], bool]] = None,
) -> "Result":    # starichenko
    """Compare dicts 1 level.

    :param target:
    :param compare:
    :param func: used to compare values
    """
    class Result:
        equel_by_values: dict = {}
        diff_by_values: dict = {}
        intersection: dict = {}     # updated intersection!
        not_in_a: dict = {}
        not_in_b: dict = {}

    result = Result()

    if func is None:
        func = lambda x1, x2: x1 == x2

    for key, value in target.items():
        if key not in compare:
            result.not_in_b.update({key: value})
            continue

        result.intersection.update({key: value})

        if func(value, compare.get(key)):
            result.equel_by_values.update({key: value})
        else:
            result.diff_by_values.update({key: value})

    # NOT_IN_A --------------------------------------------
    for key, value in compare.items():
        if key not in target:
            result.not_in_a.update({key: value})

    return result


def dict_compare_by_same_values(
        source: dict,
        compare: dict,
        func: tp.Optional[tp.Callable[[tp.Any, tp.Any], bool]] = None,
        return_by: int = 0
) -> dict:    # starichenko
    """Return new dict by Delete from source dict keys with same values from compare dict!

    specially created for finding params not already set on Volga!

    :param source:
    :param compare:
    :param func: used to compare values
    :param return_by:
        - 0: all
        - 1: same
        - 2: diff
    :return: new dict
    """
    result = {}

    # if func is None:
    #     func = lambda x1, x2: x1 == x2
    #
    # for key, value in source.items():
    #     if func(value, compare.get(key)):
    #         result.update({key: value})
    return result


def dicts_compare(dict1, dict2, use_only_keys_list=None):     # starichenko
    """
    if dicts eaual - then fully equivalent of direct comparing!
    but if not - will show the different keys and different values!

    :param dict1:
    :param dict2:
    :param keys_list:  if specified compare only this keys!
    :return:
    """
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        msg = f"incorrect input types {dict1=}/{dict2=}"
        logging_and_print_warning(msg)
        return

    dict1 = copy.deepcopy(dict1)
    dict2 = copy.deepcopy(dict2)

    if use_only_keys_list:
        dict1 = dict_keys_delete_by_name(dict1, keys_list_or_func_link=use_only_keys_list, reverse_decision=True)
        dict2 = dict_keys_delete_by_name(dict2, keys_list_or_func_link=use_only_keys_list, reverse_decision=True)

    if dict1 == dict2:
        return True

    # diff_keys -------------------------------------------------------------------------------------------------------
    diff_keys = sequences_get_different_elements(dict1, dict2)

    # diff_values -----------------------------------------------------------------------------------------------------
    diff_values = {}
    for key, value in dict1.items():
        if key not in diff_keys:
            if value != dict2.get(key):
                diff_values.update({key: [value, dict2.get(key)]})
                msg = f"incorrect value dict1({key}:{value}) != dict2({key}:{dict2.get(key)})"
                logging_and_print_warning(msg)

    if diff_keys or diff_values:
        return False


def dict_validate_by_etalon(source, etalon, allow_extra_keys=True, nested=True):  #starichenko
    """

    KEYS compare for existance!
    VALUES compare for types
        VALUE is correct always if any of value_* is None otherwise it must be equal types!!!

    if values in etalon_dict is dict - validation will continue by recursion!

    specially created for validating dicts in testcase

    :param source:
    :param etalon: values must be exact types or None for any type!
    :return:
    """
    result = True

    if not isinstance(source, dict) or not isinstance(etalon, dict):
        msg = f"incorrect input types {source=}/{etalon=}"
        logging_and_print_warning(msg)
        return False

    for key_etalon, value_etalon in etalon.items():
        if key_etalon not in source:
            msg = f"missing expected {key_etalon=}"
            logging_and_print_warning(msg)
            result = False
        else:

            value_source = source.get(key_etalon)
            if None not in [value_source, value_etalon]:
                if type(value_source) != type(value_etalon):
                    msg = f"different types {value_source=}/{value_etalon=}"
                    logging_and_print_warning(msg)
                    result = False
                elif nested:
                    if isinstance(value_etalon, dict):
                        result &= dict_validate_by_etalon(source=value_source, etalon=value_etalon, allow_extra_keys=allow_extra_keys, nested=nested)
                    elif isinstance(value_etalon, (set, list)) and len(value_etalon) == 1 and isinstance(value_etalon[0], dict):
                        result &= dicts_list_validate_by_etalon(source=value_source, etalon=value_etalon[0], allow_extra_keys=allow_extra_keys, nested=nested)

    # allow_extra_keys
    if not allow_extra_keys:
        for key_source in source:
            if key_source not in etalon:
                msg = f"not allowed {key_source=}"
                logging_and_print_warning(msg)
                result = False

    return result


def dicts_list_validate_by_etalon(source, etalon, allow_extra_keys=True, nested=True):  #starichenko
    if source is None:
        return True
    if not isinstance(source, (set, list)):
        return

    if len(source) == 0:
        return True

    result = True
    for item in source:
        result &= dict_validate_by_etalon(
            source=item,
            etalon=etalon,
            allow_extra_keys=allow_extra_keys,
            nested=nested)

    return result


# dict-MERGE+UPDATES --------------------
def dicts_merge(source_list):     # starichenko
    """
    merge dicts

    1. if any dict have valuetype=dict - other dicts MUST have:
        1. same type - will launch recursion
        2. or any blank value - will assumed as blank dict and recursion applied
        3. in other types - process will be stopped and return None
    2. if no one dict in source_list have dict type in considered value all values will be REPLACED!
        no matter was it list and int or both lists!
    """
    for item_dict in source_list:
        if not isinstance(item_dict, (dict,)):
            msg = f"incorrect types {item_dict=}"
            logging_and_print_warning(msg)
            return

    result_dict = {}
    for new_dict in source_list:
        for new_key, new_value in new_dict.items():
            if new_key not in result_dict:
                result_dict[new_key] = new_value
            elif isinstance(result_dict.get(new_key), dict) and isinstance(new_value, dict):
                # recursion
                result_dict[new_key] = dicts_merge(source_list=[result_dict.get(new_key), new_value])
            else:
                result_dict[new_key] = new_value

    return result_dict


# dict-MAKE
def dict_make_simple_example():     # Starichenko
    sample_dict = {'param1': 'Value1str', 'param2': 123, 'param3': {1: 1, 2: 2}, 'param4': ['list_value1', 'list_value2']}
    return sample_dict


def dict_make_from_keys_list_with_none_values(keys_list):
    """ Returns dict of keys with empty values.
    """
    result_dict = {}
    for key in keys_list:
        result_dict[key] = None
    return result_dict


def dict_ensure_first_key(source, first_key=None):
    """ Returns dict with first key as 'first_key' if present.
    """
    result_dict = dict()

    if first_key and first_key in source:
        result_dict[first_key] = source[first_key]

    for key, value in source.items():
        result_dict[key] = value
    return result_dict


# dict-VALUES
def dict_value_get_with_default_and_replacing(source, key, default=None, replace_list=[], replace_dict={}):    # starichenko
    """
    useful if its not enough for you standard GET method which give you default only if key is not exist in dict

    :param source: source dict
    :param key: key to get value
    :param default: the same default param as for GET method
    :param replace_list: sequence or results which you want to replace (useful for None result)
    :param replace_dict: dict value-result you want to replace in final value from source
    """
    type_check_by_variants(source, (dict,))

    # 1=step default
    result = source.get(key, default)

    # 2=step replace_list
    if result in replace_list:
        result = default

    # 2=step replace_dict
    result = value_try_replace_by_dict(source=result, search_dict=replace_dict, search_type_1starts_2full_3ends_4any_5fullmatch=2)
    return result


def dict_collapse_values_dict_by_key(source, key_priority_seq=[], default=None):     # starichenko
    """
    specially created for 2level-dicts!
    main idia to use values like dicts as variety and we can select now exact composition! remain other values without variants

    dicts like
        {
            1: {1:1, 2:2, 3:3},
            2: {1:1, 2:None},
            3: {1:1},
            4: 4,
        }
    for key=2 return
        {
            1: 2,
            2: None,
            3: None,
            4: 4,
        }

    ??????
    # test_dict = {1: {1: 1}, 2: {2: 2, 3: 3}, 3: {3: 3, 4: {1: 1, 2: 2}}, 4: {3: {1: 1, 4: 4}}}
    # test_list = [2, 3, 4]

    """
    # INPUT ---------------------------------------------------
    if not key_priority_seq:
        msg = f"blank input {key_priority_seq=}"
        logging_and_print_warning(msg)
        return
    key_priority_seq = sequence_make_ensured_if_not(key_priority_seq)

    # PRECHECK ---------------------------------------------------
    if not isinstance(source, dict):
        msg = f"incorrect input {source=}"
        logging_and_print_warning(msg)
        return

    # WORK ---------------------------------------------------
    result = dict()
    for root_key, root_value in source.items():
        if not isinstance(root_value, dict):
            result[root_key] = root_value   # dont change not dicts
            continue

        value = None
        for key in key_priority_seq:
            if key in root_value:
                value = root_value.get(key)
                break
        # if not found
        if value is None:
            value = default

        result[root_key] = value

    return result


def dict_value_get_by_keypath(source: dict, keypath: tp.Union[str, list]) -> tp.Optional[tp.Any]:      # Starichenko
    """get value from dictionary specifying by keys like a path

    example:
        for {1:1, "2":{3:3}}
        with keypath=["2", 3]
        result = 3

    CAUTION: RETURN DICTS DIRECT ACCESS!!!
    """
    # INPUT ---------------------------------------------------
    value_temp = source
    keypath = sequence_make_ensured_if_not(keypath)
    if not keypath:
        msg = f"blank {keypath=}"
        logging_and_print_warning(msg)
        return

    # WORK ---------------------------------------------------
    try:
        for key in keypath:
            value_temp = value_temp[key]
    except Exception as exx:
        msg = f"no {keypath=} in {source=}\n{exx!r}"
        logging_and_print_warning(msg)
        return

    # RESULT ---------------------------------------------------
    return value_temp


def dict_values_check_all_none(dictionary, nested=False):
    """ Returns True if all values of given dictionary are None
        and False otherwise.

    :param nested:
        if False - walk only 1 level and nested dicts are not acceptable! because will return False!
        if True - nested dict is acceptable! will walk all nested dicts
    """
    for key, value in dictionary.items():
        if nested and isinstance(value, dict):
            recursion_result = dict_values_check_all_none(value, nested=True)
            if not recursion_result:
                return False
        elif value is not None:
            return False
    return True


def dict_values_replace(
        source,
        old_values_list_or_func_link=None,
        new_value_or_func_link=None,
        protect_keys_or_func_link=None,
        nested=True,
        delete_found_keys=None,    # dont deprecate! its necessary!
):     # Starichenko
    """walk dict and rewrite exact values by exact new value
    If you need replace ALL VALUES use old_values_list_or_func_link = lambdaTrue!

    :param old_values_list_or_func_link: if value is in here - rewrite value!
    :param protect_keys_or_func_link: dont touch values if so!
    :param delete_found_keys: if value Matched - key will be deleted
    """
    if not isinstance(source, dict):
        return source

    result_dict = copy.deepcopy(source)

    for key, value in source.items():
        # decide ---------------------------
        # value
        if callable(old_values_list_or_func_link):
            decision_v = old_values_list_or_func_link(value)
        elif isinstance(old_values_list_or_func_link, (list, tuple, set)):
            decision_v = value in old_values_list_or_func_link
        else:
            decision_v = value == old_values_list_or_func_link

        # key
        if protect_keys_or_func_link:
            if callable(protect_keys_or_func_link):
                protect_k = protect_keys_or_func_link(key)
            elif isinstance(protect_keys_or_func_link, (list, tuple, set)):
                protect_k = key in protect_keys_or_func_link
            else:
                protect_k = key == protect_keys_or_func_link
        else:
            protect_k = False

        # work -----------------------------
        if decision_v and not protect_k:
            if delete_found_keys:
                result_dict.pop(key)
            else:
                if callable(new_value_or_func_link):
                    result_dict[key] = new_value_or_func_link(value)
                else:
                    result_dict[key] = new_value_or_func_link
            continue

        # nested ---------------------------
        if isinstance(value, dict) and nested:
            result_dict[key] = dict_values_replace(
                source=value,
                old_values_list_or_func_link=old_values_list_or_func_link,
                new_value_or_func_link=new_value_or_func_link,
                protect_keys_or_func_link=protect_keys_or_func_link,
                nested=nested,
                delete_found_keys=delete_found_keys,
            )

    return result_dict


def dict_values_get_list_for_key(
        source,
        key,
        return_first_value=False,
        no_repetitions=True,
        use_blank=False):             # Starichenko
    """выдает списоком значения всех ключей с именем key в многооуровневом словаре.
    результат в списке. если ничего не найдено? то выдаст пустой список [].

    :param return_first_value:
        для случаев, когда подразумевается, что в словаре в разных местах (в разной глубине) вставлены одни и теже значения для одного ключа!
    :param no_repetitions: если выводится несколько значений, то если уже есть такое значение, то не добавляется!
        можно использовать повторяющиеся значения для дальнейшего анализа их количенства
    """
    key_find = key
    value_list = []
    if not isinstance(source, dict):
        return

    # level root
    if key_find in source:
        value = source[key_find]
        if not value_is_blanked(value, zero_as_blank=False) or use_blank:
            if no_repetitions and value in value_list:
                pass
            else:
                value_list.append(value)
            if return_first_value:
                return value

    # level nested
    for key, value in source.items():
        if isinstance(value, dict):
            subresult_list = dict_values_get_list_for_key(
                source=value,
                key=key_find,
                return_first_value=return_first_value,
                no_repetitions=no_repetitions,
                use_blank=use_blank
            )
            if return_first_value and subresult_list:
                return subresult_list
            else:
                value_list = lists_sum([value_list, subresult_list], no_repetitions=no_repetitions)

    logging_and_print_debug(f"source[{key_find}]list={value_list=}")
    return value_list


def dict_value_get_by_short_key(name, source,
                                 dict_already_short=False,
                                 subkeys_list=[],
                                 nested=True,
                                 return_first_value=True,
                                 no_repetitions=True):  # STARICHENKO
    """функция ищет указанное имя с обрамляющими квадратными скобками в Settings.
    И выдает его значение.

    :raw_dict/short_dict: используется только одно значение!!!
        если raw_dict - то из него формируется short_dict

    subkeys_list: список ключей который могут быть полезны для определения значения (не все могут быть использованы!)
        для передачи этих ключей рекомендуется создавать отдельный параметр в самом DUT
    :nested: если False - смотрит только корень переданного словаря! если True - смотрит еще и все вложенные словари!
    :dont_give_error_if_found_same_name_with_same_value: вообще лучше если будет предупреждение по поводу одинакового имени в параметрах,
        но скорее всего это будет часто происходить но с одинаковыми значениями, и лучше его отключить по умолчанию
        при разных значениях ошибка в любом случае Критическая и обязана быть!

    отличия от get_value_named_setting_with_keys:
    1. работает независимо от количества ключей
    2. при наличии любого количества ключей в рассматриваемой строке Settings - смотрится есть ли они в списке subkeys_list
    3. если все ключи есть - параметр принимается, если нет - анализ останавливается и переходим к следующей строке
    4. если втречается дважды полностью подходящее значение - вызывается ошибка!

    ВЫВОД:
    ключи должны быть уникальными, тоесть однозначно должно быть понятно что они подразумевают без контекста!
    тоесть "DC" "1200" - всем понятные контексты!
    """
    name = str(name)

    # todo: dont short dict, just only find exact names!!!
    if dict_already_short:
        short_dict = source
    else:
        if nested:
            raw_dict = dict_flatten(source)
        short_dict = dict_keys_short_names(source=raw_dict, subkeys_list=subkeys_list)

    if name in short_dict:
        return short_dict[name]
    else:
        logging_and_print_warning(f"нет в словаре нужной переменной [{name}]")
        return


# dict-CONVERTION
def dict_unique__collapse_flatten_by_level(source: dict, level: int = -1):    #starichenko
    """
    works in dicts with UNIQUE keys by max level deep.

    special created for getting Volga params info from sections GDDU

    :param source:
    :param level: use negative for all levels!
    :return:
    """
    result = dict()

    if level == 0:
        return source

    for key, value in source.items():
        if not isinstance(value, dict):
            result[key] = value
            continue

        value = dict_unique__collapse_flatten_by_level(source=value, level=level-1)
        result.update(value)
    return result


def dict_flatten(source,
                 keys_list_del=[],
                 keys_list_update=[],
                 keys_list_dont_go_deep=[],
                 new_values_update=False,
                 new_values_replace_by="#ОШИБКА#",
                 _is_recursion_applied=False,
                 _result_dict={}):                  # Starichenko
    """
    преобразует все сложенные словари в словарь одного уровня вложенности!
    т.е. все ключи из всех словарей выводит в один словарь.

    :keys_list_del: прежде чем чтото будет делаться - очищается весь словарь от этих ключей!
    :keys_list_update: все ключи из этого списка будут перезаписаны в результирующем словаре, если будут иметь разные значения, независимо от других настроек функции
    :keys_list_dont_go_deep: if this keys have dict-value don't go deep, use like ordinary value
    :_is_recursion_applied: mark function as recursion step! dont use from outside!
    :_result_dict: for marking when recurtion is started!
    """
    source = dict_keys_delete_by_name(source=source, keys_list_or_func_link=keys_list_del)

    result_dict = _result_dict
    for key, value in source.items():
        if isinstance(value, dict) and key not in keys_list_dont_go_deep:
            result_dict = dict_flatten(source=value,
                                       keys_list_del=keys_list_del,
                                       keys_list_update=keys_list_update,
                                       keys_list_dont_go_deep=keys_list_dont_go_deep,
                                       new_values_update=new_values_update,
                                       new_values_replace_by=new_values_replace_by,
                                       _is_recursion_applied=True,
                                       _result_dict=result_dict)
        else:
            if key not in result_dict or key in keys_list_update:
                result_dict.update({key: value})
            elif result_dict[key] == source[key]:
                pass
            else:       # если значения не сходятся!
                logging_and_print_warning("error!!! detected same keys with DIFFERENT values")
                logging_and_print_warning(dict_get_pretty_string(result_dict))
                msg = F"1, key=[{key}] old_value result_dict[key]=[{result_dict[key]}]"
                logging_and_print_warning(msg)
                msg = F"2, key=[{key}] new_value=[{value}]"
                logging_and_print_warning(msg)
                if new_values_update:
                    result_dict.update({key: value})
                elif new_values_replace_by:
                    result_dict.update({key: new_values_replace_by})
                    msg = F"3, key=[{key}] OVERRITEN_value=[{new_values_replace_by}]"
                    logging_and_print_warning(msg)

    if not _is_recursion_applied:
        logging_and_print_debug(f"result_dict={result_dict}")
    return result_dict


def dict_get_pretty_string(source, name=None, _print=False):   # starichenko
    """return pretty string for dict
    """
    try:
        pretty_string = json.dumps(source, indent=4)
    except:
        msg = f"CANT jsonDUMP source=[{source}]"
        logging_and_print_warning(msg)
        pretty_string = str(source)

    if name:
        pretty_string = f"{name} = {pretty_string}"

    if _print:
        print(pretty_string)
    return pretty_string


# dict-COMBINATIONS
def dict_iter_combinations_by_key_list_and_value_list(source=None):   # starichenko
    """return all combinations between key+value lists.
    can be used for brute force login+password.

    Example:
        {1: 2, 10: [11, 12], (21, 22): 23, (31, 32): (33, 34)}
        [(1, 2),    (10, 11), (10, 12),    (21, 23), (22, 23),     (31, 33), (31, 34), (32, 33), (32, 34),]
    """
    if source is None:
        source = source = {1: 2, 10: [11, 12], (21, 22): 23, (31, 32): (33, 34)}

    for key_seq, value_seq in source.items():

        if not type_is_iterable_but_not_str(key_seq):
            key_seq = [key_seq, ]
        if not type_is_iterable_but_not_str(value_seq):
            value_seq = [value_seq, ]

        for key in key_seq:
            for value in value_seq:
                yield (key, value)


def dict_make_string_of_values_if_object(source):  # starichenko
    """
    if you want to dump dict wich can have values as object like pathlib - you will use it!

    :param source:
    :return:
    """
    result = dict_values_replace(
        source=source,
        old_values_list_or_func_link=lambda _value: not type_is_elementary_single_or_container(_value),
        new_value_or_func_link=str
    )
    return result


# =====================================================================================================================

def remove_all_space(string: str):
    return string.replace(' ', '')


def is_k_string(str: str):
    try:
        if str[0] == '"' and str[-1] == '"':
            return True
        elif str[0] == "'" and str[-1] == "'":
            return True
        return False
    except Exception:
        return False


def is_string(string: str):
    if is_k_string(string):
        return True
    # elif not is_int(string) and isinstance(string, str):
    #     return True
    return False


def is_int(string: str):
    string = str(string).strip()
    try:
        int(string)
        return True
    except Exception:
        try:
            float(string)
            return True
        except Exception:
            return False


def add_str(str: str):
    return '"' + str + '"'


def to_len(index: int, ln: int):
    if index >= ln:
        index -= ln
        index = to_len(index, ln)
    return index


def remove_start_spaces(str: str):
    try:
        if str[0] == ' ':
            str = str[1:]
            return remove_start_spaces(str)
        if str[-1] == ' ':
            str = str[:-1]
            return remove_start_spaces(str)
    except Exception:
        pass
    return str


def remove_space(string: str):
    if string and string[0] == ' ':
        string = string[1:]
        return remove_space(string)
    else:
        return string


def remove_s(string: str):
    try:
        if string[0] == '"' or string[0] == "'":
            string = string[1:]
            return remove_s(string)
        elif string[-1] == '"' or string[-1] == "'":
            string = string[:-1]
            return remove_s(string)
        else:
            return string
    except Exception:
        return string


def parse_args(args):
    parsed_args = []
    for arg in args:
        if arg != '':
            parsed_args.append(arg)

    return parsed_args


def check_type(value, type):
    if type == 'str':
        if is_string(value):
            if is_k_string(value):
                value = value[1:-1]
            try:
                value = str(value)
            except Exception:
                return False
            return True
        else:
            return False
    elif type == 'int':
        if isinstance(value, float):
            return False
        try:
            value = int(value)
        except Exception:
            return False
        return True
    elif type == 'float':
        try:
            value = float(value)
        except Exception:
            return False
        return True
    elif type == 'list':
        return True
    elif type == 'node':
        from node import Node

        return isinstance(value, Node)
    elif type == 'class':
        return isinstance(value, dict)
    elif type == 'bool':
        return True
    else:
        return False

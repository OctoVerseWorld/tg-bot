from typing import Any


def parse_start_command_args(message_text: str) -> dict[str, Any]:
    args_str_ = message_text.split(' ')
    if len(args_str_) > 1:
        args_str_ = args_str_[1]
    else:
        return {}
    args_list_ = args_str_.split('&')
    args = {}
    for arg_ in args_list_:
        arg_key, arg_val = arg_.split('__')
        args[arg_key] = arg_val
    return args

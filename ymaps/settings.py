from typing import Optional, Dict, List
from decimal import Decimal


# Types
_Scheme = Optional[str]
_Timeout = Optional[int]
_Proxies = Optional[Dict[str, str]]

_list_i = Optional[List[int]]
_list_f = Optional[List[type(Decimal)]]
_list_s = Optional[List[str]]
_float_l = List[type(Decimal)]


# Default options
class options:
    default_scheme = 'https'
    default_timeout = 1
    default_proxies = None


# Exception
class YandexSearchException(Exception):
    pass


class UnexpectedResponse(YandexSearchException):
    pass


class InvalidKey(YandexSearchException):
    pass


class InvalidParameters(YandexSearchException):
    pass


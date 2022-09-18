"""
Settings and Exceptions for ymaps
"""


# Default options
class options:
    default_timeout = 1
    default_lang = "ru_RU"


# Exception
class YandexSearchException(Exception):
    pass


class UnexpectedResponse(YandexSearchException):
    pass


class InvalidKey(YandexSearchException):
    pass


class InvalidParameters(YandexSearchException):
    pass


class YandexSearchException(Exception):
    pass


class UnexpectedResponse(YandexSearchException):
    pass


class InvalidKey(YandexSearchException):
    pass


class InvalidParameters(YandexSearchException):
    pass


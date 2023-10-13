"""
Exceptions for ymaps
"""


class Exceptions:
    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        self.text = response.text

    def get_exception_or_response(self):
        if self.status_code == 200:
            return self.response
        elif self.status_code == 400:
            raise InvalidParameters(self.text)
        elif self.status_code == 403:
            raise InvalidKey(self.text)
        else:
            raise UnexpectedResponse(self.text)


class YandexApiException(Exception):
    pass


class UnexpectedResponse(YandexApiException):
    pass


class InvalidKey(YandexApiException):
    pass


class InvalidParameters(YandexApiException):
    pass

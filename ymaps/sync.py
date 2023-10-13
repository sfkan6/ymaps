"""
Synchronous Client for Yandex Maps API
"""

from httpx import Client
from typing import Dict, List, Optional

from ymaps.settings import DefaultSettings
from ymaps.exceptions import Exceptions
from ymaps.api_parameters import ParameterCollector


class BaseClient:
    """
    Base class for Yandex API client

    Documentation at:
        https://yandex.ru/dev/maps/mapsapi/
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        language: Optional[str] = DefaultSettings.language,
        timeout: Optional[int] = DefaultSettings.timeout,
    ):
        client_settings = {"apikey": api_key, "lang": language}
        self._client = Client(
            base_url=base_url,
            params=client_settings,
            timeout=timeout,
        )

    def _get(self, request_parameters):
        response = self._client.get(".", params=request_parameters)
        return Exceptions(response).get_exception_or_response()

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class SearchClient(BaseClient, ParameterCollector):
    """
    Yandex Place API client

    Documentation at:
        https://yandex.ru/dev/geosearch/doc/ru/
    """

    BASE_URL = "https://search-maps.yandex.ru/v1"

    def __init__(
        self,
        api_key: str,
        language: Optional[str] = DefaultSettings.language,
        timeout: Optional[int] = DefaultSettings.timeout,
    ):
        super().__init__(self.BASE_URL, api_key, language, timeout)

    def search(self, text: str, **params) -> Dict:
        """Search for a geographical object or organization"""
        request_parameters = super()._collect_request_parameters(text=text, **params)
        return self._get(request_parameters).json()


class GeocodeClient(BaseClient, ParameterCollector):
    """
    Yandex Geocoder API client

    Documentation at:
        https://yandex.ru/dev/geocode/doc/ru/
    """

    BASE_URL = "https://geocode-maps.yandex.ru/1.x"

    def __init__(
        self,
        api_key: str,
        language: Optional[str] = DefaultSettings.language,
        timeout: Optional[int] = DefaultSettings.timeout,
    ):
        super().__init__(self.BASE_URL, api_key, language, timeout)

    def geocode(self, geocode: str, **params) -> Dict:
        """Search for geographical coordinates of objects"""
        request_parameters = self._collect_request_parameters(geocode=geocode, **params)
        return self._get(request_parameters)

    def reverse(self, geocode: List, **params) -> Dict:
        """Search for objects by geographical coordinates"""
        request_parameters = self._collect_reverse_parameters(geocode, **params)
        return self._get(request_parameters)

    def _get(self, request_parameters):
        result = super()._get(request_parameters)
        if request_parameters["format"] == "json" and not request_parameters.get(
            "callback"
        ):
            return result.json()
        return result.text

    def _collect_reverse_parameters(self, geocode, **params):
        request_parameters = self._collect_request_parameters(reverse=geocode, **params)
        request_parameters["geocode"] = request_parameters.pop("reverse")
        return request_parameters

    def _collect_request_parameters(self, **params):
        params["format"] = params.get("format", "json")
        return super()._collect_request_parameters(**params)


class SuggestClient(BaseClient, ParameterCollector):
    """
    Yandex Suggest API client

    Documentation at:
        https://yandex.ru/dev/geosuggest/doc/ru/
    """

    BASE_URL = "https://suggest-maps.yandex.ru/v1/suggest"

    def __init__(
        self,
        api_key: str,
        language: Optional[str] = DefaultSettings.suggest_language,
        timeout: Optional[int] = DefaultSettings.timeout,
    ):
        super().__init__(self.BASE_URL, api_key, language, timeout)

    def suggest(self, text: str, **params) -> Dict:
        """Get suggestions based on search results"""
        request_parameters = super()._collect_request_parameters(text=text, **params)
        return self._get(request_parameters).json()


class StaticClient(BaseClient, ParameterCollector):
    """
    Yandex Static API client

    Documentation at:
        https://yandex.ru/dev/staticapi/doc/ru/
    """

    BASE_URL = "https://static-maps.yandex.ru/v1"

    def __init__(
        self,
        api_key: str,
        language: Optional[str] = DefaultSettings.language,
        timeout: Optional[int] = DefaultSettings.timeout,
    ):
        super().__init__(self.BASE_URL, api_key, language, timeout)

    def get_image(self, **params) -> bytes:
        """
        Returns an image according to the given parameters

        Save image:
            >>> response = StaticClient('api_key').get_image(...)
            >>> with open('file.png', 'wb') as file:
            >>>     file.write(response)
        """
        request_parameters = self._collect_request_parameters(**params)
        return self._get(request_parameters).content

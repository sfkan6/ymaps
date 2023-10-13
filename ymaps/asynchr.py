"""
Asynchronous Client for Yandex Maps API
"""

from httpx import AsyncClient
from typing import Dict, List, Optional

from ymaps.settings import DefaultSettings
from ymaps.exceptions import Exceptions
from ymaps.api_parameters import ParameterCollector


class BaseAsyncClient:
    """
    Base class for Async Yandex API client

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
        self._client = AsyncClient(
            base_url=base_url,
            params=client_settings,
            timeout=timeout,
        )

    async def _get(self, request_parameters):
        response = await self._client.get(".", params=request_parameters)
        return Exceptions(response).get_exception_or_response()

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, tb):
        await self.close()


class SearchAsyncClient(BaseAsyncClient, ParameterCollector):
    """
    Async Yandex Place API client

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

    async def search(self, text: str, **params) -> Dict:
        """Search for a geographical object or organization"""
        request_parameters = super()._collect_request_parameters(text=text, **params)
        response = await self._get(request_parameters)
        return response.json()


class GeocodeAsyncClient(BaseAsyncClient, ParameterCollector):
    """
    Async Yandex Geocoder API client

    Documentation at:
        https://yandex.ru/dev/geocode/doc/ru/
    """

    BASE_URL = "https://geocode-maps.yandex.ru/1.x"

    def __init__(
        self,
        api_key: str,
        language: Optional[str] = DefaultSettings.language,
        timeout: Optional[int] = DefaultSettings.timeout,
    ) -> None:
        super().__init__(self.BASE_URL, api_key, language, timeout)

    async def geocode(self, geocode: str, **params) -> Dict:
        """Search for geographical coordinates of objects"""
        request_parameters = await self._collect_request_parameters(
            geocode=geocode, **params
        )
        return await self._get(request_parameters)

    async def reverse(self, geocode: List, **params) -> Dict:
        """Search for objects by geographical coordinates"""
        request_parameters = await self._collect_reverse_parameters(geocode, **params)
        return await self._get(request_parameters)

    async def _get(self, request_parameters):
        result = await super()._get(request_parameters)
        if request_parameters["format"] == "json" and not request_parameters.get(
            "callback"
        ):
            return result.json()
        return result.text

    async def _collect_reverse_parameters(self, geocode, **params):
        request_parameters = await self._collect_request_parameters(
            reverse=geocode, **params
        )
        request_parameters["geocode"] = request_parameters.pop("reverse")
        return request_parameters

    async def _collect_request_parameters(self, **params):
        params["format"] = params.get("format", "json")
        return super()._collect_request_parameters(**params)


class SuggestAsyncClient(BaseAsyncClient, ParameterCollector):
    """
    Async Yandex Suggest API client

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

    async def suggest(self, text: str, **params) -> Dict:
        """Get suggestions based on search results"""
        request_parameters = self._collect_request_parameters(text=text, **params)
        response = await self._get(request_parameters)
        return response.json()


class StaticAsyncClient(BaseAsyncClient, ParameterCollector):
    """
    Async Yandex Static API client

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

    async def get_image(self, **params) -> bytes:
        """
        Returns an image according to the given parameters
        Save image:
            >>> response = StaticClient('api_key').get_image(...)
            >>> with open('file.png', 'wb') as file:
            >>>     file.write(response)

        """
        params = self._collect_request_parameters(**params)
        response = await self._get(params)
        return response.content

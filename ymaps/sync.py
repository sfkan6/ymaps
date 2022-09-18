"""
Synchronous Client for Yandex Maps API
"""

from typing import Dict, List, Optional
from httpx import Client
from ymaps.settings import options, InvalidKey, UnexpectedResponse, InvalidParameters


class BaseClient:
    """
    Base class for Yandex API client

    Documentation at:
        https://yandex.ru/dev/maps/mapsapi/
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str],
        timeout: Optional[int] = options.default_timeout,
        lang: Optional[str] = None,
    ) -> None:
        params = {"lang": lang or options.default_lang}
        if api_key:
            params["apikey"] = api_key

        self._client = Client(
            params=params,
            timeout=timeout,
        )
        self.base_url = base_url

    def __enter__(self) -> "BaseClient":
        return self

    def __exit__(self, exc_type, exc_val, tb):
        self.close()

    def _request(self, params):
        """Fulfills the request"""
        response = self._client.get(
            self.base_url,
            params=params,
        )
        if response.status_code == 200:
            return response
        elif response.status_code == 400:
            raise InvalidParameters
        elif response.status_code == 403:
            raise InvalidKey
        else:
            raise UnexpectedResponse(
                f"status_code={response.status_code}\nurl={response.url}"
            )

    def _collect(self, **kwargs):
        """Collects request parameters"""
        params = kwargs

        if params.get("ll"):
            ll = params["ll"]
            params["ll"] = f"{ll[0]},{ll[1]}"
        if params.get("spn"):
            spn = params["spn"]
            params["spn"] = f"{spn[0]},{spn[1]}"
        if params.get("bbox"):
            bbox = params["bbox"]
            params["bbox"] = f"{bbox[0]},{bbox[1]}~{bbox[2]},{bbox[3]}"
        if params.get("rspn"):
            params["rspn"] = 1
        return params

    def close(self):
        """Close network connection"""
        self._client.close()


class SearchClient(BaseClient):
    """
    Yandex Place API client

    Documentation at:
        https://yandex.ru/dev/maps/geosearch/doc/concepts/request.html
    """

    BASE_URL = "https://search-maps.yandex.ru/v1/"

    def __init__(
        self, api_key: str, timeout: Optional[int] = None, lang: Optional[str] = None
    ) -> None:
        super().__init__(self.BASE_URL, api_key, timeout, lang)

    def search(self, query: str, **kwargs) -> Dict:
        """Get geo objects and organizations"""
        params = self._collect(text=query, **kwargs)
        return self._request(params).json()


class GeocodeClient(BaseClient):
    """
    Yandex Geocoder API client

    Documentation at:
        https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/input_params.html
    """

    BASE_URL = "https://geocode-maps.yandex.ru/1.x/"

    def __init__(
        self, api_key: str, timeout: Optional[int] = None, lang: Optional[str] = None
    ) -> None:
        super().__init__(self.BASE_URL, api_key, timeout, lang)

    def _collect(self, **kwargs):
        data = {"format": "json"}
        data.update(kwargs)
        params = super()._collect(**data)
        return params

    def geocode(self, geocode: str, **kwargs) -> Dict:
        """Search for geocoordinates"""
        params = self._collect(geocode=geocode, **kwargs)
        return self._request(params).json()

    def reverse(self, geocode: List, **kwargs) -> Dict:
        """Search for an object by geocoordinates"""
        params = self._collect(geocode=f"{geocode[0]},{geocode[1]}", **kwargs)
        return self._request(params).json()


class StaticClient(BaseClient):
    """
    Yandex Static API client

    Documentation at:
        https://yandex.ru/dev/maps/staticapi/doc/1.x/dg/concepts/input_params.html
    """

    BASE_URL = "https://static-maps.yandex.ru/1.x/"

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> None:
        super().__init__(self.BASE_URL, api_key, timeout, lang)

    def _collect(self, **kwargs):
        data = {"l": ["sat"]}
        data.update(kwargs)
        params = super()._collect(**data)

        params["l"] = ",".join(params["l"])
        if params.get("size"):
            size = params["size"]
            params["size"] = f"{size[0]},{size[1]}"
        if params.get("pt"):
            pt = params["pt"]
            params["pt"] = "~".join(pt)
        if params.get("pl"):
            pl = params["pl"]
            params["pl"] = "~".join(pl)
        return params

    def getimage(self, ll: List, **kwargs) -> bytes:
        """
        Returns an image according to the given parameters
        Save image:
            >>> with open('file.png', "wb") as file:
            >>>     file.write(response.content)
        """
        params = self._collect(ll=ll, **kwargs)
        return self._request(params).content

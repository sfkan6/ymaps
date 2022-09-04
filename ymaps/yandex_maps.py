import requests

from urllib.request import getproxies
from .settings import options, InvalidKey, UnexpectedResponse, InvalidParameters
from .settings import _Scheme, _Timeout, _Proxies, _list_f, _list_i, _list_s, _float_l


class BaseClient:
    """
    Base class for Yandex API client

    Documentation at:
        https://yandex.ru/dev/maps/mapsapi/
    """

    DOMAIN = 'yandex.ru'
    API_PATH = '/'

    def __init__(
            self,
            api_key,
            scheme:  _Scheme = None,
            timeout: _Timeout = None,
            proxies: _Proxies = None
    ):
        self.api_key = api_key
        self.scheme = scheme or options.default_scheme
        self.timeout = timeout or options.default_timeout
        self.proxies = self._normalize_proxies(proxies)
        self.base_url = '%s://%s%s' % (self.scheme, self.DOMAIN, self.API_PATH)

    @staticmethod
    def _normalize_proxies(proxies):
        """
        Normalizes a custom proxy
        Kind of custom proxy:

        proxies =  {
            “http”: “http://0.0.0.0:8000”,
            “https”: “http://0.0.0.0:8000”,
        }
        """

        if proxies is None:
            proxies = getproxies()
        if not proxies:
            return {}

        normalized = {}
        for scheme, url in proxies.items():
            if url and '://' not in url:
                url = "http://%s" % url
            normalized[scheme] = url
        return normalized

    def _request(self, params):
        """Fulfills the request"""

        response = requests.get(
            self.base_url,
            params=params,
            timeout=self.timeout,
            proxies=self.proxies
        )
        if response.status_code == 200:
            return response
        elif response.status_code == 400:
            raise InvalidParameters
        elif response.status_code == 403:
            raise InvalidKey
        else:
            raise UnexpectedResponse(
                f"status_code={response.status_code}, body={response.content}"
            )


class SearchClient(BaseClient):
    """
    Yandex Place API client
    
    Documentation at:
        https://yandex.ru/dev/maps/geosearch/doc/concepts/request.html
    """

    DOMAIN = 'search-maps.yandex.ru'
    API_PATH = '/v1/'

    def __init__(self, api_key: str, scheme: _Scheme=None, timeout: _Timeout=None, proxies: _Proxies=None):
        super().__init__(api_key, scheme, timeout, proxies)

    def _collect(
            self,
            text,
            lang=None,
            type_objects=None,
            ll=None,
            spn=None,
            bbox=None,
            rspn=None,
            results=None,
            skip=None,
    ):
        """ Collects request parameters """

        params = {
            'apikey': self.api_key,
            'text': text,
            'lang': 'ru_RU',
        }

        if lang:
            params['lang'] = lang
        if type_objects:
            params['type'] = type_objects
        if ll and spn:
            try:
                params['ll'] = f'{ll[0]},{ll[1]}'
                params['spn'] = f'{spn[0]},{spn[1]}'
            except:
                raise InvalidParameters
        if bbox:
            try:
                params['bbox'] = f'{bbox[0]},{bbox[1]}~{bbox[2]},{bbox[3]}'
            except:
                raise InvalidParameters
        if rspn:
            params['rspn'] = 1
        if results:
            params['results'] = results
        if skip:
            params['skip'] = skip
        return params

    def search(
            self,
            text:   str,
            lang:   str|None = None,
            type_objects: str|None = None,
            ll:     _list_f = None,
            spn:    _list_f = None,
            bbox:   _list_f = None,
            rspn:   bool|None = None,
            results: int|None = None,
            skip:   int|None = None,
    ):
        """ Get geo objects and organizations"""
        params = self._collect(
                text=text, lang=lang, type_objects=type_objects,
                ll=ll, spn=spn, bbox=bbox, rspn=rspn,
                results=results, skip=skip
        )
        return self._request(params).json()


class GeocoderClient(BaseClient):
    """
    Yandex Geocoder API client

    Documentation at:
        https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/input_params.html
    """

    DOMAIN = 'geocode-maps.yandex.ru'
    API_PATH = '/1.x/'

    def __init__(self, api_key, scheme:_Scheme=None, timeout:_Timeout=None, proxies:_Proxies=None):
        super().__init__(api_key, scheme, timeout, proxies)
    
    def _collect(
            self,
            geocode,
            sco=None,
            kind=None,
            rspn=None,
            ll=None,
            spn=None,
            bbox=None,
            form=None,
            results=None,
            skip=None,
            lang=None
    ):
        """ Collects request parameters """

        params = {
            'apikey': self.api_key,
            'geocode': geocode,
            'format': 'json'
        }

        if sco:
            params['sco'] = sco
        if kind:
            params['kind'] = kind
        if rspn:
            params['rspn'] = 1
        if ll and spn:
            try:
                params['ll'] = f'{ll[0]},{ll[1]}'
                params['spn'] = f'{spn[0]},{spn[1]}'
            except:
                raise InvalidParameters
        if bbox:
            try:
                params['bbox'] = f'{bbox[0]},{bbox[1]}~{bbox[2]},{bbox[3]}'
            except:
                raise InvalidParameters
        if form:
            params['format'] = form
        if results:
            params['results'] = results
        if skip:
            params['skip'] = skip 
        if lang:
            params['lang'] = lang

        return params

    def geocode(
            self,
            address: str,
            rspn:   bool|None = None,
            ll:     _list_f = None,
            spn:    _list_f = None,
            bbox:   _list_f = None,
            form:   str|None = None,
            results: int|None = None,
            skip:   int|None = None,
            lang:   str|None = None
    ):
        """ Search for geocoordinates """

        params = self._collect(
                geocode=address,rspn=rspn,
                ll=ll, spn=spn, bbox=bbox,
                form=form, results=results,
                skip=skip, lang=lang
        )
        return self._request(params).json()

    def reverse(
            self,
            geocode: _float_l,
            sco:    str|None = None,
            kind:   str|None = None,
            rspn:   bool|None = None,
            ll:     _list_f = None,
            spn:    _list_f = None,
            bbox:   _list_f = None,
            form:   str|None = None,
            results: int|None = None,
            skip:   int|None = None,
            lang:   str|None = None
    ):
        """ Search for an object by geocoordinates """

        try:
            geodata = '{},{}'.format(geocode[1], geocode[0])
        except:
            raise InvalidParameters

        params = self._collect(
                geocode=geodata, sco=sco, kind=kind,
                rspn=rspn, ll=ll, spn=spn, bbox=bbox,
                form=form, results=results, skip=skip, lang=lang
        )
        return self._request(params).json()


class StaticClient(BaseClient):
    """ 
    Yandex Static API client

    Documentation at:
        https://yandex.ru/dev/maps/staticapi/doc/1.x/dg/concepts/input_params.html
    """

    DOMAIN = 'static-maps.yandex.ru'
    API_PATH = '/1.x/'

    def __init__(self, api_key=None, scheme: _Scheme=None, timeout: _Timeout=None, proxies: _Proxies=None):
        super().__init__(api_key, scheme, timeout, proxies)

    def _collect(
            self,
            l,
            ll,
            spn=None,
            z=None,
            size=None,
            scale=None,
            pt=None,
            pl=None,
            lang=None
    ):
        """ Collects request parameters """

        params = {}
        if self.api_key:
            params['key'] = self.api_key

        try:
            params['l'] = ','.join(l)
            params['ll'] = f'{ll[0]},{ll[1]}'
        except:
            raise InvalidParameters

        if spn:
            params['spn'] = f'{spn[0]},{spn[1]}'
        if z:
            params['z'] = z
        if size:
            params['size'] = f'{size[0]},{size[1]}'
        if scale:
            params['scale'] = scale
        if pt:
            params['pt'] = '~'.join(pt)
        if pl:
            params['pl'] = '~'.join(pl)
        if lang:
            params['lang'] = lang
        return params
 
    def getimage(
            self,
            l:      _list_s,
            ll:     _float_l,
            spn:    _list_f = None,
            z:      int|None = None,
            size:   _list_i = None,
            scale:  float|None = None,
            pt:     _list_s = None,
            pl:     _list_s =None,
            lang:   str|None = None
    ):
        """
        Returns an image according to the given parameters
        Save image:
            >>> with open('file.png', "wb") as file:
            >>>     file.write(response.content)
        """
        params = self._collect(
            l=l, ll=ll, spn=spn, z=z, size=size,
            scale=scale, pt=pt, pl=pl, lang=lang
        )
        return self._request(params).content


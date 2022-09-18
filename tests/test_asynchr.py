'''
Tests for asynchronous Yandex Maps API client
'''

import pytest

from unittest import mock
from pytest_httpx import HTTPXMock
from ymaps import (
    SearchAsync,
    GeocodeAsync,
    StaticAsync,
    InvalidKey,
    InvalidParameters,
    UnexpectedResponse,
)


# class testing

def test_init_search_client():
    search = SearchAsync('api_key')
    assert search.base_url == 'https://search-maps.yandex.ru/v1/'
    assert search._client.params['lang'] == 'ru_RU'
    assert search._client.params['apikey'] == 'api_key'


def test_init_geocode_client():
    geocode = GeocodeAsync('api_key')
    assert geocode.base_url == 'https://geocode-maps.yandex.ru/1.x/'
    assert geocode._client.params['lang'] == 'ru_RU'
    assert geocode._client.params['apikey'] == 'api_key'


def test_init_static_client():
    static = StaticAsync('api_key')
    assert static.base_url == 'https://static-maps.yandex.ru/1.x/'
    assert static._client.params['lang'] == 'ru_RU'
    assert static._client.params['apikey'] == 'api_key'

    static = StaticAsync()
    assert static.base_url == 'https://static-maps.yandex.ru/1.x/'
    assert static._client.params['lang'] == 'ru_RU'
    assert static._client.params.get('apikey', None) == None


# search testing

@pytest.mark.asyncio
async def test_search(httpx_mock: HTTPXMock):
    request = 'Car service, Moscow, 2 Vyazovsky proezd 4a'
    expected = {'request': request}
    httpx_mock.add_response(
        method='GET',
        url='%s?lang=ru_RU&apikey=api_key&text=%s' % (SearchAsync.BASE_URL, request),
        json=expected,
    )
    actual = await SearchAsync('api_key').search(request)
    assert actual == expected


@pytest.mark.asyncio
async def test_search_with_lang_type(httpx_mock: HTTPXMock):
    request = 'Car service, Moscow, 2 Vyazovsky proezd 4a'
    params = {'lang': 'tr_TR', 'type': 'biz'}
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url='%s?lang=tr_TR&apikey=api_key&text=%s&type=biz' % (SearchAsync.BASE_URL, request),
        json=expected,
    )
    actual = await SearchAsync('api_key').search(request, **params)
    assert actual == expected


@pytest.mark.asyncio
async def test_search_with_ll_spn(httpx_mock: HTTPXMock):
    request = 'Car service, Moscow, 2 Vyazovsky proezd 4a'
    params = {'ll': [37.61892, 55.756994], 'spn': [0.552069, 0.400552]}
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url='%s?lang=ru_RU&apikey=api_key&text=%s&ll=37.61892,55.756994&spn=0.552069,0.400552' % (SearchAsync.BASE_URL, request),
        json=expected,
    )
    actual = await SearchAsync('api_key').search(request, **params)
    assert actual == expected


@pytest.mark.asyncio
async def test_search_with_bbox(httpx_mock: HTTPXMock):
    request = 'Car service, Moscow, 2 Vyazovsky proezd 4a'
    params = {'bbox': [36.83, 55.67, 38.24, 55.91]}
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url='%s?lang=ru_RU&apikey=api_key&text=%s&bbox=36.83,55.67~38.24,55.91' % (SearchAsync.BASE_URL, request),
        json=expected,
    )
    actual = await SearchAsync('api_key').search(request, **params)
    assert actual == expected


@pytest.mark.asyncio
async def test_search_with_rspn_results_skip(httpx_mock: HTTPXMock):
    request = 'Car service, Moscow, 2 Vyazovsky proezd 4a'
    params = {'rspn': True, 'results': 10, 'skip': 10}
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url='%s?lang=ru_RU&apikey=api_key&text=%s&rspn=1&results=10&skip=10' % (SearchAsync.BASE_URL, request),
        json=expected,
    )
    actual = await SearchAsync('api_key').search(request, **params)
    assert actual == expected


@pytest.mark.asyncio
async def test_search_with_all(httpx_mock: HTTPXMock):
    request = 'Car service, Moscow, 2 Vyazovsky proezd 4a'
    params = {
        'll': [37.61892, 55.756994],
        'spn': [0.552069, 0.400552],
        'bbox': [36.83, 55.67, 38.24, 55.91],
        'rspn': True, 'results': 10, 'skip': 10,
        'lang': 'tr_TR', 'type': 'biz'
    }
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url='%s?lang=tr_TR&apikey=api_key&text=%s&ll=37.61892,55.756994&spn=0.552069,0.400552&rspn=1&results=10&skip=10&type=biz&bbox=36.83,55.67~38.24,55.91' % 
        (SearchAsync.BASE_URL, request),
        json=expected,
    )
    actual = await SearchAsync('api_key').search(request, **params)
    assert actual == expected


# geocode testing

@pytest.mark.asyncio
async def test_geocode(httpx_mock: HTTPXMock):
    request = 'Moscow, Novy Arbat street, 24'
    expected = {'request': request}
    httpx_mock.add_response(
        method='GET',
        url='%s?lang=ru_RU&apikey=api_key&format=json&geocode=%s' % (GeocodeAsync.BASE_URL, request),
        json=expected,
    )
    actual = await GeocodeAsync('api_key').geocode(request)
    assert actual == expected


@pytest.mark.asyncio
async def test_geocode_with_lang_sco_kind_rspn(httpx_mock: HTTPXMock):
    request = 'Moscow, Novy Arbat street, 24'
    params = {'sco': 'latlong' ,'lang': 'tr_TR', 'kind': 'metro', 'rspn': True}
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url='%s?lang=tr_TR&apikey=api_key&geocode=%s&format=json&sco=latlong&kind=metro&rspn=1' % (GeocodeAsync.BASE_URL, request),
        json=expected,
    )
    actual = await GeocodeAsync('api_key').geocode(request, **params)
    assert actual == expected


@pytest.mark.asyncio
async def test_geocode_with_ll_spn(httpx_mock: HTTPXMock):
    request = 'Moscow, Novy Arbat street, 24'
    params = {'ll': [37.61892, 55.756994], 'spn': [0.552069, 0.400552]}
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url='%s?lang=ru_RU&apikey=api_key&geocode=%s&format=json&ll=37.61892,55.756994&spn=0.552069,0.400552' % (GeocodeAsync.BASE_URL, request),
        json=expected,
    )
    actual = await GeocodeAsync('api_key').geocode(request, **params)
    assert actual == expected


@pytest.mark.asyncio
async def test_geocode_with_bbox(httpx_mock: HTTPXMock):
    request = 'Moscow, Novy Arbat street, 24'
    params = {'bbox': [36.83, 55.67, 38.24, 55.91]}
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url='%s?lang=ru_RU&apikey=api_key&geocode=%s&format=json&bbox=36.83,55.67~38.24,55.91' % (GeocodeAsync.BASE_URL, request),
        json=expected,
    )
    actual = await GeocodeAsync('api_key').geocode(request, **params)
    assert actual == expected


@pytest.mark.asyncio
async def test_geocode_with_rspn_results_format_results_skip(httpx_mock: HTTPXMock):
    request = 'Moscow, Novy Arbat street, 24'
    params = {'format': 'xml', 'results': 10, 'skip': 10}
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url='%s?lang=ru_RU&apikey=api_key&geocode=%s&format=xml&results=10&skip=10' % (GeocodeAsync.BASE_URL, request),
        json=expected,
    )
    actual = await GeocodeAsync('api_key').geocode(request, **params)
    assert actual == expected


@pytest.mark.asyncio
async def test_geocode_with_all(httpx_mock: HTTPXMock):
    request = 'Moscow, Novy Arbat street, 24'
    params = {
        'kind': 'street', 'rspn': True,
        'll': [37.61892, 55.756994],
        'spn': [0.552069, 0.400552],
        'bbox': [36.83, 55.67, 38.24, 55.91],
        'format': 'xml', 'results': 10,
        'skip': 10, 'lang': 'tr_TR' 
    }
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url='%s?lang=tr_TR&apikey=api_key&geocode=%s&ll=37.61892,55.756994&spn=0.552069,0.400552&rspn=1&kind=street&results=10&skip=10&format=xml&bbox=36.83,55.67~38.24,55.91' % 
        (GeocodeAsync.BASE_URL, request),
        json=expected,
    )
    actual = await GeocodeAsync('api_key').geocode(request, **params)
    assert actual == expected


# reverse testing

@pytest.mark.asyncio
async def test_reverse(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    expected = {'request': request}
    httpx_mock.add_response(
        method='GET',
        url='%s?lang=ru_RU&apikey=api_key&format=json&geocode=%s' % (GeocodeAsync.BASE_URL, f'{request[0]},{request[1]}'),
        json=expected,
    )
    actual = await GeocodeAsync('api_key').reverse(request)
    assert actual == expected


@pytest.mark.asyncio
async def test_reverse_with_sco_lang_kind_rspn(httpx_mock: HTTPXMock):
    request = [55.760241, 37.611347]
    params = {'sco': 'latlong' ,'lang': 'tr_TR', 'kind': 'metro', 'rspn': True}
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url='%s?lang=tr_TR&apikey=api_key&geocode=%s&format=json&sco=latlong&kind=metro&rspn=1' % 
        (GeocodeAsync.BASE_URL, f'{request[0]},{request[1]}'),
        json=expected,
    )
    actual = await GeocodeAsync('api_key').reverse(request, **params)
    assert actual == expected


@pytest.mark.asyncio
async def test_reverse_with_ll_spn(httpx_mock: HTTPXMock):
    request =  [37.611347, 55.760241]
    params = {'ll': [37.61892, 55.756994], 'spn': [0.552069, 0.400552]}
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url='%s?lang=ru_RU&apikey=api_key&geocode=%s&format=json&ll=37.61892,55.756994&spn=0.552069,0.400552' % 
        (GeocodeAsync.BASE_URL, f'{request[0]},{request[1]}'),
        json=expected,
    )
    actual = await GeocodeAsync('api_key').reverse(request, **params)
    assert actual == expected


@pytest.mark.asyncio
async def test_reverse_with_bbox(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    params = {'bbox': [36.83, 55.67, 38.24, 55.91]}
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url="%s?lang=ru_RU&apikey=api_key&geocode=%s&format=json&"\
            "bbox=36.83,55.67~38.24,55.91" % 
        (GeocodeAsync.BASE_URL, f'{request[0]},{request[1]}'),
        json=expected,
    )
    actual = await GeocodeAsync('api_key').reverse(request, **params)
    assert actual == expected


@pytest.mark.asyncio
async def test_reverse_with_rspn_results_format_results_skip(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    params = {'format': 'xml', 'results': 10, 'skip': 10}
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url="%s?lang=ru_RU&apikey=api_key&geocode=%s&format=xml&results=10&skip=10" % 
        (GeocodeAsync.BASE_URL, f'{request[0]},{request[1]}'),
        json=expected,
    )
    actual = await GeocodeAsync('api_key').reverse(request, **params)
    assert actual == expected


@pytest.mark.asyncio
async def test_reverse_with_all(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    params = {
        'sco': 'latlong',
        'kind': 'street', 'rspn': True,
        'll': [37.61892, 55.756994],
        'spn': [0.552069, 0.400552],
        'bbox': [36.83, 55.67, 38.24, 55.91],
        'format': 'xml', 'results': 10,
        'skip': 10, 'lang': 'tr_TR' 
    }
    expected = {'request': request, 'params': params}

    httpx_mock.add_response(
        method='GET',
        url="%s?lang=tr_TR&apikey=api_key&geocode=%s&ll=37.61892,55.756994&"\
            "spn=0.552069,0.400552&sco=latlong&rspn=1&kind=street&results=10&"\
            "skip=10&format=xml&bbox=36.83,55.67~38.24,55.91" % 
            (GeocodeAsync.BASE_URL, f'{request[0]},{request[1]}'),
        json=expected,
    )
    actual = await GeocodeAsync('api_key').reverse(request, **params)
    assert actual == expected


# getimage testing

@pytest.mark.asyncio
async def test_getimage(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    expected = 'test_getimage'
    httpx_mock.add_response(
        method='GET',
        url='%s?ll=%s&l=sat&lang=ru_RU' % 
            (StaticAsync.BASE_URL, f'{request[0]},{request[1]}'),
        json=expected,
    )
    actual = await StaticAsync().getimage(request)
    assert actual.decode() == f'"{expected}"'


@pytest.mark.asyncio
async def test_getimage_with_l_z_scale_lang(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    params = {'l': ['sat', 'skl', 'trf'] , 'z': '16', 'scale': 1.6, 'lang': 'tr_TR'}
    expected = 'test_getimage_with_l_z_scale_lang'

    httpx_mock.add_response(
        method='GET',
        url='%s?ll=%s&lang=tr_TR&l=sat,skl,trf&z=16&scale=1.6' % 
            (StaticAsync.BASE_URL, f'{request[0]},{request[1]}'),
        json=expected,
    )
    actual = await StaticAsync().getimage(request, **params)
    assert actual.decode() == f'"{expected}"'


@pytest.mark.asyncio
async def test_getimage_with_spn_size(httpx_mock: HTTPXMock):
    request =  [37.611347, 55.760241]
    params = {'spn': [0.552069, 0.400552], 'size': [600, 400]}
    expected = 'test_getimage_with_spn_size'

    httpx_mock.add_response(
        method='GET',
        url='%s?ll=%s&lang=ru_RU&l=sat&spn=0.552069,0.400552&size=600,400' % 
        (StaticAsync.BASE_URL, f'{request[0]},{request[1]}'),
        json=expected,
    )
    actual = await StaticAsync().getimage(request, **params)
    assert actual.decode() == f'"{expected}"'


@pytest.mark.asyncio
async def test_getimage_with_pt_pl(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    params = {
        'pt': ['37.620070,55.753630,pmwtm1', '37.620074,55.753632,pmwtl20'],
        'pl': [
            'c:cd5b45,f:2222DDC0,w:5,37.656705,55.741092,37.653551,55.742387',
            'c:dc143c,f:8822DDC0,w:5,37.660286,55.743301,37.661831,55.745165',
        ],
    }
    expected = 'test_getimage_with_pt_pl'

    httpx_mock.add_response(
        method='GET',
        url="%s?ll=%s&lang=ru_RU&l=sat&pt=37.620070,55.753630,pmwtm1~37.620074,55.753632,pmwtl20&"\
            "pl=c:cd5b45,f:2222DDC0,w:5,37.656705,55.741092,37.653551,55.742387~c:dc143c,"\
            "f:8822DDC0,w:5,37.660286,55.743301,37.661831,55.745165" % 
        (StaticAsync.BASE_URL, f'{request[0]},{request[1]}'),
        json=expected,
    )
    actual = await StaticAsync().getimage(request, **params)
    assert actual.decode() == f'"{expected}"'


@pytest.mark.asyncio
async def test_getimage_with_all(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    params = {
        'lang': 'tr_TR',
        'l': ['sat', 'skl', 'trf'] ,
        'z': '16',
        'scale': 1.6,
        'spn': [0.552069, 0.400552],
        'size': [600, 400],
        'pt': ['37.620070,55.753630,pmwtm1', '37.620074,55.753632,pmwtl20'],
        'pl': [
            'c:cd5b45,f:2222DDC0,w:5,37.656705,55.741092,37.653551,55.742387',
            'c:dc143c,f:8822DDC0,w:5,37.660286,55.743301,37.661831,55.745165',
        ],
    }
    expected = 'test_getimage_with_all'

    httpx_mock.add_response(
        method='GET',
        url="%s?ll=%s&lang=tr_TR&l=sat,skl,trf&z=16&scale=1.6&"\
            "spn=0.552069,0.400552&size=600,400&"\
            "pt=37.620070,55.753630,pmwtm1~37.620074,55.753632,pmwtl20&"\
            "pl=c:cd5b45,f:2222DDC0,w:5,37.656705,55.741092,37.653551,"\
            "55.742387~c:dc143c,f:8822DDC0,w:5,37.660286,55.743301,"\
            "37.661831,55.745165" %
        (StaticAsync.BASE_URL, f'{request[0]},{request[1]}'),
        json=expected,
    )
    actual = await StaticAsync().getimage(request, **params)
    assert actual.decode() == f'"{expected}"'


@mock.patch("ymaps.asynchr.AsyncClient", autospec=True)
@pytest.mark.asyncio
async def test_context_manager(mock_client):
    async with SearchAsync('') as client:
        await client._collect()
    mock_client.return_value.aclose.assert_called_once()


@pytest.mark.asyncio
async def test_invalid_parameters(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=400)
    with pytest.raises(InvalidParameters):
        await SearchAsync('').search('')


@pytest.mark.asyncio
async def test_invalid_key(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=403)
    with pytest.raises(InvalidKey):
        await SearchAsync('').search('')


@pytest.mark.asyncio
async def test_unexpected_response(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=503)
    with pytest.raises(UnexpectedResponse):
        await SearchAsync('').search('')

"""
Tests for asynchronous Yandex Maps API client
"""

import pytest
from unittest import mock
from pytest_httpx import HTTPXMock

from ymaps.exceptions import (
    InvalidKey,
    InvalidParameters,
    UnexpectedResponse,
)
from ymaps.asynchr import (
    SearchAsyncClient,
    GeocodeAsyncClient,
    SuggestAsyncClient,
    StaticAsyncClient,
)


# initialization testing


def test_init_search_client():
    search = SearchAsyncClient("api_key", timeout=10)
    assert search._client.params["apikey"] == "api_key"
    assert search._client.params["lang"] == "ru_RU"
    assert search._client.timeout.read == 10


def test_init_geocode_client():
    geocode = GeocodeAsyncClient("api_key", timeout=10)
    assert geocode._client.params["apikey"] == "api_key"
    assert geocode._client.params["lang"] == "ru_RU"
    assert geocode._client.timeout.read == 10


def test_init_suggest_client():
    geocode = SuggestAsyncClient("api_key", timeout=10)
    assert geocode._client.params["apikey"] == "api_key"
    assert geocode._client.params["lang"] == "ru"
    assert geocode._client.timeout.read == 10


def test_init_static_client():
    static = StaticAsyncClient("api_key", timeout=10)
    assert static._client.params["apikey"] == "api_key"
    assert static._client.params["lang"] == "ru_RU"
    assert static._client.timeout.read == 10


# search testing


@pytest.mark.asyncio
async def test_search(httpx_mock: HTTPXMock):
    request = "Автосервис, Москва, 2-й Вязовский проезд, 4а"
    expected = {"request": request}
    httpx_mock.add_response(
        method="GET",
        url=f"{SearchAsyncClient.BASE_URL}?apikey=api_key&lang=ru_RU&text={request}",
        json=expected,
    )
    actual = await SearchAsyncClient("api_key").search(request)
    assert actual == expected


@pytest.mark.asyncio
async def test_search_by_all_parameters(httpx_mock: HTTPXMock):
    request = "Автосервис, Москва, 2-й Вязовский проезд, 4а"
    params = {
        "lang": "tr_TR",
        "type": "biz",
        "ll": [37.61892, 55.756994],
        "spn": [0.552069, 0.400552],
        "bbox": [36.83, 55.67, 38.24, 55.91],
        "rspn": True,
        "results": 10,
        "skip": 10,
        "uri": "ymaps:123",
    }
    expected = {"request": request, "params": params}

    httpx_mock.add_response(
        method="GET",
        url=f"{SearchAsyncClient.BASE_URL}?apikey=api_key&lang=tr_TR&text={request}&"
        f"type=biz&ll=37.61892,55.756994&spn=0.552069,0.400552&bbox=36.83,55.67~38.24,55.91&"
        f"rspn=1&results=10&skip=10&uri=ymaps:123",
        json=expected,
    )
    actual = await SearchAsyncClient("api_key").search(request, **params)
    assert actual == expected


# geocode testing


@pytest.mark.asyncio
async def test_geocode(httpx_mock: HTTPXMock):
    request = "Moscow, Novy Arbat street, 24"
    expected = {"request": request}
    httpx_mock.add_response(
        method="GET",
        url=f"{GeocodeAsyncClient.BASE_URL}?apikey=api_key&lang=ru_RU&"
        f"format=json&geocode={request}",
        json=expected,
    )
    actual = await GeocodeAsyncClient("api_key").geocode(request)
    assert actual == expected


@pytest.mark.asyncio
async def test_geocode_by_format(httpx_mock: HTTPXMock):
    request = "Moscow, Novy Arbat street, 24"
    params = {"format": "xml"}
    expected = "response"

    httpx_mock.add_response(
        method="GET",
        url=f"{GeocodeAsyncClient.BASE_URL}?apikey=api_key&lang=ru_RU&geocode={request}&format=xml",
        json=expected,
    )
    actual = await GeocodeAsyncClient("api_key").geocode(request, **params)
    assert actual == f'"{expected}"'


@pytest.mark.asyncio
async def test_geocode_by_all_parameters(httpx_mock: HTTPXMock):
    request = "Moscow, Novy Arbat street, 24"
    params = {
        "lang": "tr_TR",
        "format": "json",
        "rspn": True,
        "results": 10,
        "skip": 10,
        "ll": [37.61892, 55.756994],
        "spn": [0.552069, 0.400552],
        "bbox": [36.83, 55.67, 38.24, 55.91],
        "uri": "ymaps:123",
    }
    expected = {"request": request, "params": params}

    httpx_mock.add_response(
        method="GET",
        url=f"{GeocodeAsyncClient.BASE_URL}?apikey=api_key&lang=tr_TR&geocode={request}&"
        f"format=json&ll=37.61892,55.756994&spn=0.552069,0.400552&rspn=1&results=10&"
        f"skip=10&bbox=36.83,55.67~38.24,55.91&uri=ymaps:123",
        json=expected,
    )
    actual = await GeocodeAsyncClient("api_key").geocode(request, **params)
    assert actual == expected


# reverse testing


@pytest.mark.asyncio
async def test_reverse(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    expected = {"request": request}
    httpx_mock.add_response(
        method="GET",
        url=f"{GeocodeAsyncClient.BASE_URL}?apikey=api_key&lang=ru_RU&"
        f"geocode={request[0]},{request[1]}&format=json",
        json=expected,
    )
    actual = await GeocodeAsyncClient("api_key").reverse(request)
    assert actual == expected


@pytest.mark.asyncio
async def test_reverse_by_all_parameters(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    params = {
        "sco": "latlong",
        "kind": "street",
        "rspn": True,
        "ll": [37.61892, 55.756994],
        "spn": [0.552069, 0.400552],
        "bbox": [36.83, 55.67, 38.24, 55.91],
        "format": "json",
        "results": 10,
        "skip": 10,
        "lang": "tr_TR",
        "uri": "ymaps:123",
    }
    expected = {"request": request, "params": params}

    httpx_mock.add_response(
        method="GET",
        url=f"{GeocodeAsyncClient.BASE_URL}?apikey=api_key&lang=tr_TR&format=json&"
        f"geocode={request[0]},{request[1]}&sco=latlong&kind=street&rspn=1&"
        f"ll=37.61892,55.756994&spn=0.552069,0.400552&bbox=36.83,55.67~38.24,55.91&"
        f"results=10&skip=10&uri=ymaps:123",
        json=expected,
    )
    actual = await GeocodeAsyncClient("api_key").reverse(request, **params)
    assert actual == expected


# suggest testing


@pytest.mark.asyncio
async def test_suggest(httpx_mock: HTTPXMock):
    request = "санкт"
    expected = "test_suggest"
    httpx_mock.add_response(
        method="GET",
        url=f"{SuggestAsyncClient.BASE_URL}?apikey=api_key&lang=ru&text={request}",
        json=expected,
    )
    actual = await SuggestAsyncClient("api_key").suggest(request)
    assert actual == expected


@pytest.mark.asyncio
async def test_suggest_by_all_parameters(httpx_mock: HTTPXMock):
    request = "санкт"
    params = {
        "lang": "tr",
        "results": 10,
        "highlight": 0,
        "ll": [37.611347, 55.760241],
        "spn": [0.4, 0.3],
        "types": ["street", "geo"],
        "strict_bounds": 1,
        "ull": [37.6113, 55.7602],
        "org_address_kind": "house",
        "attrs": "ymaps:123",
        "bbox": [36.83, 55.67, 38.24, 55.91],
        "print_address": True,
    }
    expected = "test_get_image_with_all"

    httpx_mock.add_response(
        method="GET",
        url=f"{SuggestAsyncClient.BASE_URL}?apikey=api_key&lang=tr&text={request}&results=10&"
        f"highlight=0&ll=37.611347,55.760241&spn=0.4,0.3&strict_bounds=1&types=street,geo&"
        f"org_address_kind=house&attrs=ymaps:123&ull=37.6113,55.7602&"
        f"bbox=36.83,55.67~38.24,55.91&print_address=1",
        json=expected,
    )
    actual = await SuggestAsyncClient("api_key").suggest(request, **params)
    assert actual == expected


# get_image testing


@pytest.mark.asyncio
async def test_get_image(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    expected = "test_get_image"
    httpx_mock.add_response(
        method="GET",
        url=f"{StaticAsyncClient.BASE_URL}?apikey=api_key&lang=ru_RU&ll={request[0]},{request[1]}",
        json=expected,
    )
    actual = await StaticAsyncClient("api_key").get_image(ll=request)
    assert actual.decode() == f'"{expected}"'


@pytest.mark.asyncio
async def test_url_static_client(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    params = {"l": ["sat", "skl"]}
    expected = "test_get_image"
    httpx_mock.add_response(
        method="GET",
        url=f"https://static-maps.yandex.ru/1.x?apikey=api_key&lang=ru_RU&"
        f"&ll={request[0]},{request[1]}&l=sat,skl",
        json=expected,
    )
    actual = await StaticAsyncClient("api_key", url="1.x").get_image(
        ll=request, **params
    )
    assert actual.decode() == f'"{expected}"'


@pytest.mark.asyncio
async def test_url_static_client(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    params = {"l": ["sat", "skl"]}
    expected = "test_get_image"
    httpx_mock.add_response(
        method="GET",
        url=f"https://static-maps.yandex.ru/1.x/?apikey=api_key&lang=ru_RU"
        f"&ll={request[0]},{request[1]}&l=sat,skl",
        json=expected,
    )
    actual = await StaticAsyncClient("api_key", url="1.x").get_image(
        ll=request, **params
    )
    assert actual.decode() == f'"{expected}"'


@pytest.mark.asyncio
async def test_get_image_by_all_parameters(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    params = {
        "lang": "tr_TR",
        "z": "16",
        "scale": 1.6,
        "spn": [0.552069, 0.400552],
        "size": [600, 400],
        "pt": ["37.620070,55.753630,pmwtm1", "37.620074,55.753632,pmwtl20"],
        "pl": [
            "c:cd5b45,f:2222DDC0,w:5,37.656705,55.741092,37.653551,55.742387",
            "c:dc143c,f:8822DDC0,w:5,37.660286,55.743301,37.661831,55.745165",
        ],
    }
    expected = "test_get_image_with_all"

    httpx_mock.add_response(
        method="GET",
        url=f"{StaticAsyncClient.BASE_URL}?apikey=api_key&lang=tr_TR&size=600,400&"
        f"z=16&scale=1.6&spn=0.552069,0.400552&ll={request[0]},{request[1]}&"
        f'pt={params["pt"][0]}~{params["pt"][1]}&'
        f'pl={params["pl"][0]}~{params["pl"][1]}',
        json=expected,
    )
    actual = await StaticAsyncClient("api_key").get_image(ll=request, **params)
    assert actual.decode() == f'"{expected}"'


# testing context manager


@mock.patch("ymaps.asynchr.AsyncClient", autospec=True)
@pytest.mark.asyncio
async def test_search_context_manager(mock_client):
    async with SearchAsyncClient("api_key") as client:
        await client.__aenter__()
    mock_client.return_value.aclose.assert_called_once()


@mock.patch("ymaps.asynchr.AsyncClient", autospec=True)
@pytest.mark.asyncio
async def test_geocode_context_manager(mock_client):
    async with GeocodeAsyncClient("api_key") as client:
        await client.__aenter__()
    mock_client.return_value.aclose.assert_called_once()


@mock.patch("ymaps.asynchr.AsyncClient", autospec=True)
@pytest.mark.asyncio
async def test_suggest_context_manager(mock_client):
    async with SuggestAsyncClient("api_key") as client:
        await client.__aenter__()
    mock_client.return_value.aclose.assert_called_once()


@mock.patch("ymaps.asynchr.AsyncClient", autospec=True)
@pytest.mark.asyncio
async def test_static_context_manager(mock_client):
    async with StaticAsyncClient("api_key") as client:
        await client.__aenter__()
    mock_client.return_value.aclose.assert_called_once()


# testing exceptions


@pytest.mark.asyncio
async def test_invalid_parameters(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=400)
    with pytest.raises(InvalidParameters):
        await SearchAsyncClient("").search("")


@pytest.mark.asyncio
async def test_invalid_key(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=403)
    with pytest.raises(InvalidKey):
        await SearchAsyncClient("").search("")


@pytest.mark.asyncio
async def test_unexpected_response(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=503)
    with pytest.raises(UnexpectedResponse):
        await SearchAsyncClient("").search("")

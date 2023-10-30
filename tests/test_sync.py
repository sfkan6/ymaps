"""
Tests for synchronous Yandex Maps API client
"""

import pytest
from unittest import mock
from pytest_httpx import HTTPXMock

from ymaps.exceptions import (
    InvalidKey,
    InvalidParameters,
    UnexpectedResponse,
)
from ymaps.sync import (
    SearchClient,
    GeocodeClient,
    SuggestClient,
    StaticClient,
)


# initialization testing


def test_init_search_client():
    search = SearchClient("api_key", timeout=10)
    assert search._client.params["apikey"] == "api_key"
    assert search._client.params["lang"] == "ru_RU"
    assert search._client.timeout.read == 10


def test_init_geocode_client():
    geocode = GeocodeClient("api_key", timeout=10)
    assert geocode._client.params["apikey"] == "api_key"
    assert geocode._client.params["lang"] == "ru_RU"
    assert geocode._client.timeout.read == 10


def test_init_suggest_client():
    geocode = SuggestClient("api_key", timeout=10)
    assert geocode._client.params["apikey"] == "api_key"
    assert geocode._client.params["lang"] == "ru"
    assert geocode._client.timeout.read == 10


def test_init_static_client():
    static = StaticClient("api_key", timeout=10)
    assert static._client.params["apikey"] == "api_key"
    assert static._client.params["lang"] == "ru_RU"
    assert static._client.timeout.read == 10


# search testing


def test_search(httpx_mock: HTTPXMock):
    request = "Автосервис, Москва, 2-й Вязовский проезд, 4а"
    expected = {"request": request}
    httpx_mock.add_response(
        method="GET",
        url=f"{SearchClient.BASE_URL}?apikey=api_key&lang=ru_RU&text={request}",
        json=expected,
    )
    actual = SearchClient("api_key").search(request)
    assert actual == expected


def test_search_by_all_parameters(httpx_mock: HTTPXMock):
    request = "Автосервис, Москва, 2-й Вязовский проезд, 4а"
    params = {
        "lang": "tr_TR",
        "type": "biz",
        "ll": [37.763775, 55.720281],
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
        url=f"{SearchClient.BASE_URL}?apikey=api_key&lang=tr_TR&text={request}&"
        f"type=biz&ll=37.763775,55.720281&spn=0.552069,0.400552&bbox=36.83,55.67~38.24,55.91&"
        f"rspn=1&results=10&skip=10&uri=ymaps:123",
        json=expected,
    )
    actual = SearchClient("api_key").search(request, **params)
    assert actual == expected


# geocode testing


def test_geocode(httpx_mock: HTTPXMock):
    request = "Москва, улица Новый Арбат, 24"
    expected = {"request": request}
    httpx_mock.add_response(
        method="GET",
        url=f"{GeocodeClient.BASE_URL}?apikey=api_key&lang=ru_RU&format=json&geocode={request}",
        json=expected,
    )
    actual = GeocodeClient("api_key").geocode(request)
    assert actual == expected


def test_geocode_by_format(httpx_mock: HTTPXMock):
    request = "Москва, улица Новый Арбат, 24"
    params = {"format": "xml"}
    expected = "response"

    httpx_mock.add_response(
        method="GET",
        url=f"{GeocodeClient.BASE_URL}?apikey=api_key&lang=ru_RU&geocode={request}&format=xml",
        json=expected,
    )
    actual = GeocodeClient("api_key").geocode(request, **params)
    assert actual == f'"{expected}"'


def test_geocode_by_all_parameters(httpx_mock: HTTPXMock):
    request = "Москва, улица Новый Арбат, 24"
    params = {
        "lang": "tr_TR",
        "format": "json",
        "rspn": True,
        "results": 10,
        "skip": 10,
        "ll": [37.587614, 55.753088],
        "spn": [0.552069, 0.400552],
        "bbox": [37.583508, 55.750773, 37.591719, 55.755403],
        "uri": "ymaps:123",
    }
    expected = {"request": request, "params": params}

    httpx_mock.add_response(
        method="GET",
        url=f"{GeocodeClient.BASE_URL}?apikey=api_key&lang=tr_TR&geocode={request}&"
        f"format=json&ll=37.587614,55.753088&spn=0.552069,0.400552&rspn=1&results=10&"
        f"skip=10&bbox=37.583508,55.750773~37.591719,55.755403&uri=ymaps:123",
        json=expected,
    )
    actual = GeocodeClient("api_key").geocode(request, **params)
    assert actual == expected


# reverse testing


def test_reverse(httpx_mock: HTTPXMock):
    request = [37.587614, 55.753088]
    expected = {"request": request}
    httpx_mock.add_response(
        method="GET",
        url=f"{GeocodeClient.BASE_URL}?apikey=api_key&lang=ru_RU&"
        f"geocode={request[0]},{request[1]}&format=json",
        json=expected,
    )
    actual = GeocodeClient("api_key").reverse(request)
    assert actual == expected


def test_reverse_by_all_parameters(httpx_mock: HTTPXMock):
    request = [37.587614, 55.753088]
    params = {
        "sco": "longlat",
        "kind": "street",
        "rspn": True,
        "ll": [37.611347, 55.760241],
        "spn": [0.552069, 0.400552],
        "bbox": [37.583508, 55.750773, 37.591719, 55.755403],
        "format": "json",
        "results": 10,
        "skip": 10,
        "lang": "tr_TR",
        "uri": "ymaps:123",
    }
    expected = {"request": request, "params": params}

    httpx_mock.add_response(
        method="GET",
        url=f"{GeocodeClient.BASE_URL}?apikey=api_key&lang=tr_TR&format=json&"
        f"geocode={request[0]},{request[1]}&sco=longlat&kind=street&rspn=1&"
        f"ll=37.611347,55.760241&spn=0.552069,0.400552&"
        f"bbox=37.583508,55.750773~37.591719,55.755403&"
        f"results=10&skip=10&uri=ymaps:123",
        json=expected,
    )
    actual = GeocodeClient("api_key").reverse(request, **params)
    assert actual == expected


# suggest testing


def test_suggest(httpx_mock: HTTPXMock):
    request = "санкт"
    expected = "test_suggest"
    httpx_mock.add_response(
        method="GET",
        url=f"{SuggestClient.BASE_URL}?apikey=api_key&lang=ru&text={request}",
        json=expected,
    )
    actual = SuggestClient("api_key").suggest(request)
    assert actual == expected


def test_suggest_by_all_parameters(httpx_mock: HTTPXMock):
    request = "санкт"
    params = {
        "lang": "tr",
        "results": 10,
        "highlight": 0,
        "ll": [30.655285, 59.932992],
        "spn": [0.4, 0.3],
        "types": ["street", "geo"],
        "strict_bounds": 1,
        "ull": [30.513564, 59.908494],
        "org_address_kind": "house",
        "attrs": "ymaps:123",
        "bbox": [30.033788, 59.853361, 30.495067, 60.109461],
        "print_address": True,
    }
    expected = "test_get_image_with_all"

    httpx_mock.add_response(
        method="GET",
        url=f"{SuggestClient.BASE_URL}?apikey=api_key&lang=tr&text={request}&results=10&"
        f"highlight=0&ll=30.655285,59.932992&spn=0.4,0.3&strict_bounds=1&types=street,geo&"
        f"org_address_kind=house&attrs=ymaps:123&ull=30.513564,59.908494&"
        f"bbox=30.033788,59.853361~30.495067,60.109461&print_address=1",
        json=expected,
    )
    actual = SuggestClient("api_key").suggest(request, **params)
    assert actual == expected


# get_image testing


def test_get_image(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    expected = "test_get_image"
    httpx_mock.add_response(
        method="GET",
        url=f"{StaticClient.BASE_URL}?apikey=api_key&lang=ru_RU&ll={request[0]},{request[1]}",
        json=expected,
    )
    actual = StaticClient("api_key").get_image(ll=request)
    assert actual.decode() == f'"{expected}"'


def test_url_static_client(httpx_mock: HTTPXMock):
    request = [37.611347, 55.760241]
    params = {"l": ["sat", "skl"]}
    expected = "test_get_image"
    httpx_mock.add_response(
        method="GET",
        url=f"https://static-maps.yandex.ru/1.x/?apikey=api_key&lang=ru_RU"
        f"&ll={request[0]},{request[1]}&l=sat,skl",
        json=expected,
    )
    actual = StaticClient("api_key", url="1.x").get_image(ll=request, **params)
    assert actual.decode() == f'"{expected}"'


def test_get_image_by_all_parameters(httpx_mock: HTTPXMock):
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
        url=f"{StaticClient.BASE_URL}?apikey=api_key&lang=tr_TR&size=600,400&"
        f"z=16&scale=1.6&spn=0.552069,0.400552&ll={request[0]},{request[1]}&"
        f'pt={params["pt"][0]}~{params["pt"][1]}&'
        f'pl={params["pl"][0]}~{params["pl"][1]}',
        json=expected,
    )
    actual = StaticClient("api_key").get_image(ll=request, **params)
    assert actual.decode() == f'"{expected}"'


# testing context manager


@mock.patch("ymaps.sync.Client", autospec=True)
def test_search_context_manager(mock_client):
    with SearchClient("api_key") as client:
        client.__enter__()
    mock_client.return_value.close.assert_called_once()


@mock.patch("ymaps.sync.Client", autospec=True)
def test_geocode_context_manager(mock_client):
    with GeocodeClient("api_key") as client:
        client.__enter__()
    mock_client.return_value.close.assert_called_once()


@mock.patch("ymaps.sync.Client", autospec=True)
def test_suggest_context_manager(mock_client):
    with SuggestClient("api_key") as client:
        client.__enter__()
    mock_client.return_value.close.assert_called_once()


@mock.patch("ymaps.sync.Client", autospec=True)
def test_static_context_manager(mock_client):
    with StaticClient("api_key") as client:
        client.__enter__()
    mock_client.return_value.close.assert_called_once()


# testing exceptions


def test_invalid_parameters(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=400)
    with pytest.raises(InvalidParameters):
        SearchClient("").search("")


def test_invalid_key(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=403)
    with pytest.raises(InvalidKey):
        SearchClient("").search("")


def test_unexpected_response(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=503)
    with pytest.raises(UnexpectedResponse):
        SearchClient("").search("")

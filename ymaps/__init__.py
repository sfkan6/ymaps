"""
Client for Yandex Maps API
"""

from ymaps.sync import BaseClient, SearchClient, GeocodeClient, StaticClient

from ymaps.asynchr import (
    BaseAsyncClient as BaseAsync,
    SearchAsyncClient as SearchAsync,
    GeocodeAsyncClient as GeocodeAsync,
    StaticAsyncClient as StaticAsync,
)

from ymaps.settings import (
    InvalidKey,
    UnexpectedResponse,
    YandexSearchException,
    InvalidParameters,
)


__version__ = "1.1"
__all__ = [
    "BaseClient",
    "SearchClient",
    "GeocodeClient",
    "StaticClient",
    "BaseAsync",
    "SearchAsync",
    "GeocodeAsync",
    "StaticAsync",
    "InvalidKey",
    "UnexpectedResponse",
    "YandexSearchException",
    "InvalidParameters",
]

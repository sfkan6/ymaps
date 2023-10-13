"""
Client for Yandex Maps API
"""

from ymaps.sync import (
    BaseClient as Base,
    SearchClient as Search,
    GeocodeClient as Geocode,
    SuggestClient as Suggest,
    StaticClient as Static,
)

from ymaps.asynchr import (
    BaseAsyncClient as BaseAsync,
    SearchAsyncClient as SearchAsync,
    GeocodeAsyncClient as GeocodeAsync,
    SuggestAsyncClient as SuggestAsync,
    StaticAsyncClient as StaticAsync,
)


__version__ = "1.2"
__all__ = [
    "Base",
    "Search",
    "Geocode",
    "Suggest",
    "Static",
    "BaseAsync",
    "SearchAsync",
    "GeocodeAsync",
    "SuggestAsync",
    "StaticAsync",
]

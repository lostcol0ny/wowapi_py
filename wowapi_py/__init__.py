from api import Api
from async_api import AsyncApi
from wow_game_data import WowGameDataApi
from wow_profile_data import WowProfileDataApi
from async_wow_game_data import AsyncWowGameDataApi
from exceptions import (
    BlizzardApiException,
    AuthenticationError,
    RateLimitError,
    ResourceNotFoundError,
    InvalidRegionError,
    ApiConnectionError,
    InvalidResponseError,
)
import custom_types

__all__ = [
    "Api",
    "AsyncApi",
    "custom_types",
    "WowGameDataApi",
    "WowProfileDataApi",
    "AsyncWowGameDataApi",
    "BlizzardApiException",
    "AuthenticationError",
    "RateLimitError",
    "ResourceNotFoundError",
    "InvalidRegionError",
    "ApiConnectionError",
    "InvalidResponseError",
]

"""
Blizzard API Wrapper

This package provides a Pythonic interface to the Blizzard API,
including classes for interacting with World of Warcraft game data
and profile information.

Classes:
    Api: Base class for API interaction
    WowGameDataApi: Class for accessing WoW game data
    WowProfileApi: Class for accessing WoW profile data
"""

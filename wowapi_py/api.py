"""
Blizzard API Client

This module provides a client for interacting with Blizzard's API services.

The main class, Api, handles authentication, request management, and
provides methods for making API calls to different Blizzard services.

Features:
- Support for multiple regions (US, EU, KR, TW, CN)
- Automatic token refresh
- Context manager support for proper resource management

Usage with context manager:
with WowGameDataApi(client_id, client_secret) as api:
    achievement = api.get_achievement(region, locale, 10)

Usage without context manager:
api = WowGameDataApi(client_id, client_secret)
achievement = api.get_achievement(region, locale, 10)

For more information on Blizzard's API, visit:
https://develop.battle.net/documentation
"""

from typing import Dict, Any, Literal, TypedDict, Optional, Callable
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from dataclasses import dataclass, field
from requests.exceptions import RequestException, HTTPError
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from exceptions import (
    BlizzardApiException,
    AuthenticationError,
    RateLimitError,
    ResourceNotFoundError,
    InvalidRegionError,
    ApiConnectionError,
    InvalidResponseError,
)

from time import time
from functools import wraps
from custom_types import RegionType


def method_cache(func: Callable):
    cache = {}

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(self, *args, **kwargs)
        return cache[key]

    return wrapper


class OAuthToken(TypedDict):
    access_token: str
    token_type: str
    expires_in: int
    expires_at: float


class ApiResponse(TypedDict, total=False):
    id: int
    name: str
    description: Optional[str]


@dataclass
class Api:
    """Base API class for interacting with Blizzard's API.

    This class handles authentication and requests to Blizzard's API endpoints.
    It supports both synchronous and asynchronous operations.

    Attributes:
        client_id: A string representing the client ID for API authentication.
        client_secret: A string representing the client secret for API authentication.
        token: A dictionary containing the current OAuth token information.
        token_expiration: A datetime object representing when the current token expires.
        api_url: A string template for the main API URL.
        api_url_cn: A string template for the China-specific API URL.
        oauth_url: A string template for the OAuth token URL.
        oauth_url_cn: A string for the China-specific OAuth token URL.
        session: An OAuth2Session object for making authenticated requests.
        async_session: An aiohttp.ClientSession object for making asynchronous requests.
    """

    client_id: str
    client_secret: str
    token: Dict[str, Any] = field(default_factory=dict, init=False)
    api_url: str = field(
        default="https://{region}.api.blizzard.com{resource}", init=False
    )
    api_url_cn: str = field(
        default="https://gateway.battlenet.com.cn{resource}", init=False
    )
    oauth_url: str = field(default="https://oauth.battle.net/authorize", init=False)
    token_url: str = field(default="https://oauth.battle.net/token", init=False)
    oauth_url_cn: str = field(
        default="https://www.battlenet.com.cn/oauth/authorize", init=False
    )
    token_url_cn: str = field(
        default="https://www.battlenet.com.cn/oauth/token", init=False
    )
    session: OAuth2Session = field(init=False)

    def __post_init__(self):
        # Initialize the session
        client = BackendApplicationClient(client_id=self.client_id)
        self.session = OAuth2Session(client=client)

    def __enter__(self):
        """Enter the runtime context for synchronous operations."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context for synchronous operations."""
        self.session.close()

    @method_cache
    def get_client_credentials_token(self, region: RegionType) -> Dict[str, Any]:
        """Fetch a token using the client credentials flow."""
        token_url = self.token_url_cn if region == "cn" else self.token_url
        auth = (self.client_id, self.client_secret)
        try:
            response = self.session.fetch_token(token_url=token_url, auth=auth)
            self.token = response
            return self.token
        except OAuth2Error as oauth_err:
            raise AuthenticationError(
                f"Failed to fetch client credentials token: {oauth_err}"
            )

    def _format_url(self, resource: str, region: RegionType) -> str:
        """Format the URL into a usable URL."""
        return (
            self.api_url_cn.format(resource=resource)
            if region == "cn"
            else self.api_url.format(region=region, resource=resource)
        )

    def request(
        self, method: str, resource: str, region: RegionType, **kwargs
    ) -> Dict[str, Any]:
        if region not in ["us", "eu", "tw", "kr", "cn"]:
            raise InvalidRegionError(
                f"Invalid region: {region}. Must be one of: 'us', 'eu', 'tw', 'kr', or 'cn'"
            )

        url = self._format_url(resource, region)
        kwargs["headers"] = kwargs.get("headers", {})

        # Use a single token request per region
        if not self.token or self.token.get("expires_at", 0) <= time() + 60:
            self.token = self.get_client_credentials_token(region)

        kwargs["headers"]["Authorization"] = f"Bearer {self.token['access_token']}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            if response.status_code == 401:
                # Token might be expired, retry once with a new token
                self.token = self.get_client_credentials_token(region)
                kwargs["headers"][
                    "Authorization"
                ] = f"Bearer {self.token['access_token']}"
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()
            elif response.status_code == 404:
                raise ResourceNotFoundError(f"Resource not found: {method, url}")
            elif response.status_code == 429:
                raise RateLimitError(
                    "API rate limit exceeded. Please wait before making more requests."
                )
            else:
                raise BlizzardApiException(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
            raise ApiConnectionError(f"Error connecting to API: {req_err}")
        except ValueError:
            raise InvalidResponseError("Invalid JSON response received from API")

    def get(self, resource: str, region: RegionType, **kwargs) -> Dict[str, Any]:
        return self.request("GET", resource, region, **kwargs)

    def _refresh_token(self, region: RegionType) -> None:
        """Fetch a new access token using OAuth2."""
        token_url = (
            self.oauth_url_cn
            if region == "cn"
            else self.oauth_url.format(region=region)
        )
        try:
            self.token = self.session.fetch_token(
                token_url=token_url,
                client_id=self.client_id,
                client_secret=self.client_secret,
            )
        except OAuth2Error as oauth_err:
            raise AuthenticationError(f"Failed to refresh token: {oauth_err}")

    def get(self, resource: str, region: RegionType, **kwargs) -> Dict[str, Any]:
        return self.request("GET", resource, region, **kwargs)

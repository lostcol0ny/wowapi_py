"""
Blizzard API Client

This module provides a client for asynchronours interactions with Blizzard's API services.

The main class, Api, handles authentication, request management, and
provides methods for making API calls to different Blizzard services.

Features:
- Support for multiple regions (US, EU, KR, TW, CN)
- Automatic token refresh
- Context manager support for proper resource management
- Asynchronous support

Usage:
    server_list = [121, 127, 151, 115, 106, 1072]

    async def fetch_realm_data(api, server_id):
        try:
            data = await api.get_connected_realm(region, locale, server_id)
            print(f"Fetched data for server {server_id}")
            return data
        except Exception as e:
            print(f"Error fetching data for server {server_id}: {e}")
            return None

    async def main():
        async with await AsyncWowGameDataApi.create(client_id, client_secret) as api:
            tasks = [fetch_realm_data(api, server_id) for server_id in server_list]
            results = await asyncio.gather(*tasks)
            
            for server_id, result in zip(server_list, results):
                if result:
                    print(f"Data for server {server_id}:")
                    print(json.dumps(result, indent=2))
                    print("\n" + "="*50 + "\n")  # Separator between server data

    asyncio.run(main())

This client is designed to work with Blizzard's various API services,
including but not limited to World of Warcraft, Diablo, Hearthstone,
and Starcraft II.

For more information on Blizzard's API, visit:
https://develop.battle.net/documentation
"""

from typing import Any, Optional
import aiohttp
from aiohttp import ClientSession
from dataclasses import dataclass, field
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
from api import RegionType, ApiResponse, OAuthToken


@dataclass
class AsyncApi:
    client_id: str
    client_secret: str
    token: OAuthToken = field(default_factory=dict, init=False)
    api_url: str = field(
        default="https://{region}.api.blizzard.com{resource}", init=False
    )
    api_url_cn: str = field(
        default="https://gateway.battlenet.com.cn{resource}", init=False
    )
    oauth_url: str = field(
        default="https://{region}.battle.net/oauth/token", init=False
    )
    oauth_url_cn: str = field(
        default="https://www.battlenet.com.cn/oauth/token", init=False
    )
    session: Optional[ClientSession] = field(default=None, init=False)

    async def __aenter__(self) -> "AsyncApi":
        if self.session is None or self.session.closed:
            self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    def _format_url(self, resource: str, region: RegionType) -> str:
        return (
            self.api_url_cn.format(resource=resource)
            if region == "cn"
            else self.api_url.format(region=region, resource=resource)
        )

    async def request(
        self, method: str, resource: str, region: RegionType, **kwargs: Any
    ) -> ApiResponse:
        if region not in ["us", "eu", "tw", "kr", "cn"]:
            raise InvalidRegionError(
                f"Invalid region: {region}. Must be one of: 'us', 'eu', 'tw', 'kr', or 'cn'"
            )

        current_time = time()
        if not self.token or self.token.get("expires_at", 0) <= current_time + 60:
            await self._refresh_token(region)

        url = self._format_url(resource, region)
        kwargs.setdefault("headers", {})[
            "Authorization"
        ] = f"Bearer {self.token['access_token']}"

        try:
            async with self.session.request(method, url, **kwargs) as response:
                if response.status == 401:
                    await self._refresh_token(region)
                    kwargs["headers"][
                        "Authorization"
                    ] = f"Bearer {self.token['access_token']}"
                    async with self.session.request(method, url, **kwargs) as response:
                        response.raise_for_status()
                        return await response.json()
                else:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientResponseError as http_err:
            if http_err.status == 401:
                raise AuthenticationError(
                    "Authentication failed. Check your client ID and secret."
                )
            elif http_err.status == 404:
                raise ResourceNotFoundError(f"Resource not found: {resource}")
            elif http_err.status == 429:
                raise RateLimitError(
                    "API rate limit exceeded. Please wait before making more requests."
                )
            else:
                raise BlizzardApiException(f"HTTP error occurred: {http_err}")
        except aiohttp.ClientError as client_err:
            raise ApiConnectionError(f"Error connecting to API: {client_err}")
        except ValueError:
            raise InvalidResponseError("Invalid JSON response received from API")

    async def _refresh_token(self, region: RegionType) -> None:
        token_url = (
            self.oauth_url_cn
            if region == "cn"
            else self.oauth_url.format(region=region)
        )
        try:
            async with self.session.post(
                token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            ) as response:
                response.raise_for_status()
                self.token = await response.json()
                self.token["expires_at"] = time() + self.token["expires_in"]
        except aiohttp.ClientResponseError as err:
            raise AuthenticationError(f"Failed to refresh token: {err}")

    async def get(
        self, resource: str, region: RegionType, **kwargs: Any
    ) -> ApiResponse:
        return await self.request("GET", resource, region, **kwargs)

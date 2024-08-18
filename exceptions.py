class BlizzardApiException(Exception):
    """Base exception for Blizzard API errors"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class AuthenticationError(BlizzardApiException):
    """Raised when there's an authentication problem"""

    pass


class RateLimitError(BlizzardApiException):
    """Raised when API rate limit is exceeded"""

    pass


class ResourceNotFoundError(BlizzardApiException):
    """Raised when a requested resource is not found"""

    pass


class InvalidRegionError(BlizzardApiException):
    """Raised when an invalid region is provided"""

    pass


class ApiConnectionError(BlizzardApiException):
    """Raised when there's a problem connecting to the API"""

    pass


class InvalidResponseError(BlizzardApiException):
    """Raised when the API returns an unexpected response"""

    pass

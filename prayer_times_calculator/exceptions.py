class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class CalculationMethodError(Error):
    """Exception raised for invalid calculation method"""

    def __init__(self, variable: str, supported_values: list[str]) -> None:
        self.message = f"{variable} is invaild. Must be one of {supported_values}"
        super().__init__(self.message)


class InvalidResponseError(Error):
    """Exception raised when receiving an invalid response"""

    pass

class MoQLBaseError(Exception):
    """Base HQL errors."""


class SkipError(MoQLBaseError):
    """Raised when skip is negative / bad value."""


class LimitError(MoQLBaseError):
    """Raised when limit is negative / bad value."""


class ListOperatorError(MoQLBaseError):
    """Raised list operator was not possible."""


class FilterError(MoQLBaseError):
    """Raised when parse filter method fail to find a valid match."""


class TextOperatorError(MoQLBaseError):
    """Raised when parse text operator contain an empty string."""


class CustomCasterError(MoQLBaseError):
    """Raised when a custom cast fail."""


class ProjectionError(MoQLBaseError):
    """Raised when projection json is invalid."""


class LogicalPopulationError(MoQLBaseError):
    """Raised when method fail to find logical population item."""


class LogicalSubPopulationError(MoQLBaseError):
    """Raised when method fail to find logical sub population item."""

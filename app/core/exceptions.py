"""
Application exceptions.
"""


class AppException(Exception):
    """Base exception."""


class ValidationException(AppException):
    """Validation failed."""


class DatabaseException(AppException):
    """Database error."""


class CacheException(AppException):
    """Redis error."""


class RetrievalException(AppException):
    """RAG retrieval failed."""


class EmbeddingException(AppException):
    """Embedding generation failed."""


class LLMException(AppException):
    """LLM call failed."""


class ToolException(AppException):
    """Tool execution failed."""


class FinancialException(AppException):
    """Financial calculation failed."""


class AuthenticationException(AppException):
    """Authentication failed."""


class AuthorizationException(AppException):
    """Permission denied."""
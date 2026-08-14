class AIServiceError(Exception):
    """Base exception for LoanWise AI failures."""


class AIProviderError(AIServiceError):
    """Raised when the configured AI provider cannot answer."""


class AIConfigurationError(AIServiceError):
    """Raised when AI configuration is missing or invalid."""

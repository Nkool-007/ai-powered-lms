class AIError(Exception):
    pass


class AIConfigurationError(AIError):
    pass


class AIProviderError(AIError):
    pass


class AIRateLimitError(AIError):
    pass


class AIRequestTimeoutError(AIError):
    pass


class AIInvalidResponseError(AIError):
    pass

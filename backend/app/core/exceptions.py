class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundError(AppError):
    def __init__(self, message: str):
        super().__init__(message, 404)


class ValidationError(AppError):
    def __init__(self, message: str):
        super().__init__(message, 422)


class ExternalServiceError(AppError):
    def __init__(self, message: str):
        super().__init__(message, 502)


class DuplicateOutreachError(AppError):
    def __init__(self, message: str):
        super().__init__(message, 409)

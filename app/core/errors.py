from fastapi import HTTPException, status


class GatewayConnectionError(HTTPException):
    def __init__(self, description: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Gateway connection error: {description}"
        )


class GatewayResponseValidationError(HTTPException):
    def __init__(self, description: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Gateway response validation error: {description}"
        )


class GatewayError(HTTPException):
    """Базовый класс для ошибок, связанных с взаимодействием через шлюз."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class ServiceInitializationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

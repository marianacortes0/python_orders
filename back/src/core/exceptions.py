class AppException(Exception):
    status_code: int = 500
    detail: str = "Error interno del servidor"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class BadRequestError(AppException):
    status_code = 400
    detail = "Solicitud inválida"


class NotFoundError(AppException):
    status_code = 404
    detail = "Recurso no encontrado"


class ConflictError(AppException):
    status_code = 409
    detail = "Conflicto con el estado actual del recurso"

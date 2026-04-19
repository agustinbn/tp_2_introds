class Errores(Exception):
    def __init__(self, message, code="INTERNAL_ERROR", description=None, status_code=500, level="error"):
        super().__init__()
        self.message = message
        self.code = code
        self.description = description or message
        self.status_code = status_code
        self.level = level

    def to_dict(self):
        return {
            "errors": [
                {
                    "code": f"{self.status_code} - {self.code}",
                    "message": self.message,
                    "level": self.level,
                    "description": self.description
                }
            ]
        }

class BadRequestError(Errores):
    def __init__(self, message, description=None):
        super().__init__(message, code="BAD_REQUEST", description=description, status_code=400)

class NotFoundError(Errores):
    def __init__(self, message, description=None):
        super().__init__(message, code="NOT_FOUND", description=description, status_code=404)

class ConflictError(Errores):
    def __init__(self, message, description=None):
        super().__init__(message, code="CONFLICT", description=description, status_code=409)
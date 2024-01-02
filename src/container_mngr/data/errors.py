class ContainerRuntimeAPIError(Exception):
    def __init__(self, message: str, inner_error: Exception) -> None:
        super().__init__(message)

        self.inner_error = inner_error

class ContainerRuntimerPermissionsError(Exception):
    def __init__(self, inner_error: Exception) -> None:
        super().__init__("User does not have permissions to use container runtime API")

        self.inner_error = inner_error

class ModelMappingError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

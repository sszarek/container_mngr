from docker import DockerClient
from docker.errors import APIError
from .errors import ContainerRuntimeAPIError


def get_runtime_info() -> dict[str, str]:
    try:
        client = DockerClient.from_env()
        return client.info()
    except APIError as ex:
        raise ContainerRuntimeAPIError(
            "Error while pulling runtime information from Docker API", ex
        )


def get_images():
    try:
        client = DockerClient.from_env()
        return client.images.list()
    except APIError as ex:
        raise ContainerRuntimeAPIError(
            "Error while pulling list of images from Docker API", ex
        )

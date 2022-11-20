from datetime import datetime
from docker import DockerClient
from docker.models.images import Model
from docker.errors import APIError
from .models import ContainerRuntimeInfo, Image
from .errors import ContainerRuntimeAPIError


def get_runtime_info() -> ContainerRuntimeInfo:
    try:
        client = DockerClient.from_env()
        raw_data = client.info()

        return ContainerRuntimeInfo(
            cpu_count=raw_data["NCPU"],
            cpu_architecture=raw_data["Architecture"],
            kernel_version=raw_data["KernelVersion"],
            name=raw_data["Name"],
            os=raw_data["OperatingSystem"],
            os_type=raw_data["OSType"],
            os_version=raw_data["OSVersion"],
            server_version=raw_data["ServerVersion"],
        )
    except APIError as ex:
        raise ContainerRuntimeAPIError(
            "Error while pulling runtime information from Docker API", ex
        )


def get_images() -> list[Image]:
    try:
        client = DockerClient.from_env()
        raw_image_list = client.images.list()
        return map(_map_image, raw_image_list)
    except APIError as ex:
        raise ContainerRuntimeAPIError(
            "Error while pulling list of images from Docker API", ex
        )


def _map_image(raw_image: Model) -> Image:
    return Image(
        repository="".join(raw_image.attrs.get("RepoTags")),
        tag="latest",
        image_id=raw_image.short_id,
        created=raw_image.attrs.get("Created"),
        size_bytes=raw_image.attrs.get("Size"),
    )

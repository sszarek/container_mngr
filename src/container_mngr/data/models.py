from datetime import datetime
from dataclasses import dataclass


@dataclass
class ContainerRuntimeInfo:
    cpu_count: int
    cpu_architecture: str
    name: str
    server_version: str
    kernel_version: str
    os_type: str
    os: str
    os_version: str


@dataclass
class Image:
    repository: str
    tag: str
    image_id: str
    created: datetime
    size_bytes: float
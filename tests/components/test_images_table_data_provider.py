import pytest
from datetime import datetime
from unittest.mock import Mock
from src.container_mngr.components.images import ImagesTableDataProvider
from src.container_mngr.data import docker
from src.container_mngr.data.errors import ContainerRuntimeAPIError
from src.container_mngr.data.models import Image


image_a = Image(
    name="redis",
    tag="latest",
    image_id="3358aea34e8c",
    created=datetime.fromisoformat("2023-01-20 19:20"),
    size_bytes=117000000,
)
image_b = Image(
    name="rabbitmq",
    tag="3.10-management",
    image_id="f231cd854f72",
    created=datetime.fromisoformat("2022-02-15 16:50"),
    size_bytes=230000000,
)


@pytest.fixture
def mock_get_images(monkeypatch) -> Mock:
    get_images_mock = Mock()
    monkeypatch.setattr(docker, "get_images", get_images_mock)
    return get_images_mock


def test_get_headers_returns_headers():
    data_provider = ImagesTableDataProvider()

    columns = data_provider.get_headers()

    assert columns == ["Repository", "Tag", "Image Id", "Created", "Size"]


def test_get_rows_rethrows_error(mock_get_images: Mock):
    mock_get_images.side_effect = ContainerRuntimeAPIError("Error 1", None)

    data_provider = ImagesTableDataProvider()

    with pytest.raises(ContainerRuntimeAPIError) as err:
        data_provider.get_rows()

    assert str(err.value) == "Error 1"


def test_get_rows_returns_mapped_rows(mock_get_images: Mock):
    mock_get_images.return_value = [image_a, image_b]

    data_provider = ImagesTableDataProvider()

    rows = data_provider.get_rows()

    assert rows[0] == [
        "redis",
        "latest",
        "3358aea34e8c",
        "2023-01-20 19:20",
        "117.00 MB",
    ]

    assert rows[1] == [
        "rabbitmq",
        "3.10-management",
        "f231cd854f72",
        "2022-02-15 16:50",
        "230.00 MB"
    ]

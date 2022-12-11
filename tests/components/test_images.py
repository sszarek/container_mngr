import pytest
from datetime import datetime
from unittest.mock import Mock
from textual.app import App, ComposeResult
from src.container_mngr.components.images import ImagesPanel
from src.container_mngr.data.models import Image
from src.container_mngr.data import docker


class ImagesTestApp(App):
    def compose(self) -> ComposeResult:
        yield ImagesPanel()


@pytest.fixture
def mock_get_images(monkeypatch):
    get_images_mock = Mock()
    monkeypatch.setattr(docker, "get_images", get_images_mock)
    return get_images_mock


@pytest.mark.asyncio
async def test_first(mock_get_images) -> None:
    mock_get_images.return_value = []
    app = ImagesTestApp()

    async with app.run_test():
        images = app.query_one(ImagesPanel)
        table = images._image_table
        assert table.row_count == 0


@pytest.mark.asyncio
async def test_second(mock_get_images) -> None:
    mock_get_images.return_value = [
        Image(
            name="redis",
            tag="latest",
            image_id="3358aea34e8c",
            created=datetime.now(),
            size_bytes=117,
        ),
        Image(
            name="rabbitmq",
            tag="3.10-management",
            image_id="f231cd854f72",
            created=datetime.now(),
            size_bytes=230,
        ),
    ]

    app = ImagesTestApp()

    async with app.run_test():
        images = app.query_one(ImagesPanel)
        table = images._image_table
        assert table.row_count == 2

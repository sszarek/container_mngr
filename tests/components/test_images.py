import pytest
from datetime import datetime
from unittest.mock import Mock
from textual.app import App, ComposeResult
from src.container_mngr.components.images import ImagesPanel
from src.container_mngr.data.models import Image
from src.container_mngr.data import docker
from src.container_mngr.data.errors import ContainerRuntimeAPIError


image_a = Image(
    name="redis",
    tag="latest",
    image_id="3358aea34e8c",
    created=datetime.now(),
    size_bytes=117,
)
image_b = Image(
    name="rabbitmq",
    tag="3.10-management",
    image_id="f231cd854f72",
    created=datetime.now(),
    size_bytes=230,
)


class ImagesTestApp(App):
    def compose(self) -> ComposeResult:
        yield ImagesPanel()


@pytest.fixture
def mock_get_images(monkeypatch) -> Mock:
    get_images_mock = Mock()
    monkeypatch.setattr(docker, "get_images", get_images_mock)
    return get_images_mock


@pytest.mark.parametrize("images", [([]), ([image_a, image_b])])
@pytest.mark.asyncio
async def test_compose_proper_number_of_images(
    mock_get_images, images: list[Image]
) -> None:
    mock_get_images.return_value = images
    app = ImagesTestApp()

    async with app.run_test():
        images_panel = app.query_one(ImagesPanel)
        table = images_panel._image_table
        assert table.row_count == len(images)


@pytest.mark.asyncio
async def test_compose_no_style_set(mock_get_images) -> None:
    mock_get_images.return_value = [image_a, image_b]

    app = ImagesTestApp()

    async with app.run_test():
        images = app.query_one(ImagesPanel)
        table = images._image_table
        assert table.row_count == 2
        assert table.rows[0].style is None
        assert table.rows[1].style is None


@pytest.mark.asyncio
async def test_compose_error_getting_images(mock_get_images: Mock) -> None:
    error = ContainerRuntimeAPIError("Error 1", inner_error=Exception("inner"))
    mock_get_images.side_effect = error

    app = ImagesTestApp()

    async with app.run_test():
        images = app.query_one(ImagesPanel)
        child = images.children[0]
        assert child is None


@pytest.mark.asyncio
async def test_action_move_down_no_images(mock_get_images):
    mock_get_images.return_value = []

    app = ImagesTestApp()

    async with app.run_test():
        images = app.query_one(ImagesPanel)
        images.action_move_down()


@pytest.mark.asyncio
async def test_action_move_up_no_images(mock_get_images):
    mock_get_images.return_value = []

    app = ImagesTestApp()

    async with app.run_test():
        images = app.query_one(ImagesPanel)
        images.action_move_up()


@pytest.mark.asyncio
async def test_action_move_down_highlight_style_set(mock_get_images):
    mock_get_images.return_value = [image_a, image_b]

    app = ImagesTestApp()

    async with app.run_test():
        images = app.query_one(ImagesPanel)
        images.action_move_down()
        table = images._image_table
        assert table.rows[0].style is not None
        assert table.rows[1].style is None

        images.action_move_down()
        assert table.rows[0].style is None
        assert table.rows[1].style is not None

        images.action_move_down()
        assert table.rows[0].style is not None
        assert table.rows[1].style is None


@pytest.mark.asyncio
async def test_action_move_up_highlight_style_set(mock_get_images):
    mock_get_images.return_value = [image_a, image_b]

    app = ImagesTestApp()

    async with app.run_test():
        images = app.query_one(ImagesPanel)
        images.action_move_up()
        table = images._image_table
        assert table.rows[0].style is None
        assert table.rows[1].style is not None

        images.action_move_down()
        assert table.rows[0].style is not None
        assert table.rows[1].style is None

        images.action_move_down()
        assert table.rows[0].style is None
        assert table.rows[1].style is not None

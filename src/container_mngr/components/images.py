from typing import Final
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from ..data import docker
from ..data.models import Image
from ..components.table_wrapper import TableDataProvider, TableWrapper


class ImagesTableDataProvider(TableDataProvider):
    def get_headers(self) -> list[str]:
        return ["Repository", "Tag", "Image Id", "Created", "Size"]

    def get_rows(self) -> list:
        images = docker.get_images()
        return list(map(self._map_image, images))

    def _map_image(self, image: Image):
        return [
            image.name,
            image.tag,
            image.image_id,
            image.created.isoformat(sep=" ", timespec="minutes"),
            "{:.2f} MB".format(float(image.size_bytes) / 1000000),
        ]


class ImagesPanel(Widget):
    _image_data_provider: ImagesTableDataProvider
    _image_table: TableWrapper
    _content: Static
    _cur_idx: int = -1
    _HEADERS: Final = ["Repository", "Tag", "Image Id", "Created", "Size"]

    def compose(self) -> ComposeResult:
        self._image_data_provider = ImagesTableDataProvider()
        self._image_table = TableWrapper(self._image_data_provider)

        self.styles.border = ("heavy", "white")
        self.styles.outline = ("round", "white")
        yield self._image_table

    def action_move_down(self):
        self._image_table.action_move_down()

    def action_move_up(self):
        self._image_table.action_move_up()

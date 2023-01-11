from typing import Final
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from rich import box
from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from ..data import docker
from ..data.models import Image
from ..data.errors import ContainerRuntimeAPIError
from ..components.table_wrapper import TableDataProvider


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
    _image_table: Table
    _content: Static
    _cur_idx: int = -1
    _HEADERS: Final = ["Repository", "Tag", "Image Id", "Created", "Size"]

    def compose(self) -> ComposeResult:
        try:
            images = docker.get_images()
            self._image_table = Table(
                box=box.SIMPLE_HEAVY, show_header=True, header_style="bold bright_blue"
            )

            for header in self._HEADERS:
                self._image_table.add_column(header)

            for image in images:
                self._image_table.add_row(
                    image.name,
                    image.tag,
                    image.image_id,
                    image.created.isoformat(sep=" ", timespec="minutes"),
                    "{:.2f} MB".format(float(image.size_bytes) / 1000000),
                )

            self._content = self._render_in_panel(self._image_table)
            yield self._content
        except ContainerRuntimeAPIError as ex:
            yield self._render_in_panel(
                Text(
                    text=f"{ex}: {ex.inner_error}",
                    justify="center",
                    style="bold red",
                )
            )

    def action_move_down(self) -> None:
        if self._image_table.row_count == 0:
            return

        if self._cur_idx >= 0:
            self._remove_row_highlight(self._cur_idx)

        if self._cur_idx == (self._image_table.row_count - 1):
            self._cur_idx = 0
        else:
            self._cur_idx += 1

        self._highlight_row(self._cur_idx)
        self._content.refresh()

    def action_move_up(self) -> None:
        if self._image_table.row_count == 0:
            return

        if self._cur_idx >= 0:
            self._remove_row_highlight(self._cur_idx)

        if self._cur_idx <= 0:
            self._cur_idx = self._image_table.row_count - 1
        else:
            self._cur_idx -= 1

        self._highlight_row(self._cur_idx)
        self._content.refresh()

    def _highlight_row(self, row_idx: int) -> None:
        self._image_table.rows[row_idx].style = "black on white"

    def _remove_row_highlight(self, row_idx: int) -> None:
        self._image_table.rows[row_idx].style = None

    def _render_in_panel(self, content: RenderableType) -> Static:
        return Static(Panel(content, title="Images"))

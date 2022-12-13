from typing import Final
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from rich import box
from rich.panel import Panel
from rich.table import Table
from ..data import docker


class ImagesPanel(Widget):
    _image_table: Table
    _content: Static
    _cur_idx: int = -1
    _HEADERS: Final = ["Repository", "Tag", "Image Id", "Created", "Size"]

    def compose(self) -> ComposeResult:
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
                str(image.created),
                "{:.2f} MB".format(float(image.size_bytes) / 1000000),
            )

        self._content = Static(Panel(self._image_table, title="Images"))
        yield self._content

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

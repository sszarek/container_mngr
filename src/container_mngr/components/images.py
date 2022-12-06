from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from rich import box
from rich.panel import Panel
from rich.table import Table
from ..data.docker import get_images


class ImagesPanel(Widget):
    image_table: Table
    static: Static
    _cur_idx = -1
    _HEADERS = ["Repository", "Tag", "Image Id", "Created", "Size"]

    def compose(self) -> ComposeResult:
        images = get_images()

        self.image_table = Table(
            box=box.SIMPLE_HEAVY, show_header=True, header_style="bold bright_blue"
        )

        for header in self._HEADERS:
            self.image_table.add_column(header)

        for image in images:
            self.image_table.add_row(
                image.name,
                image.tag,
                image.image_id,
                str(image.created),
                "{:.2f} MB".format(float(image.size_bytes) / 1000000),
            )

        self.static = Static(Panel(self.image_table, title="Images"))
        yield self.static

    def action_move_down(self) -> None:
        if self._cur_idx >= 0:
            self.image_table.rows[self._cur_idx].style = "none"

        if self._cur_idx == (self.image_table.row_count - 1):
            self._cur_idx = 0
        else:
            self._cur_idx += 1

        self.image_table.rows[self._cur_idx].style = "black on white"
        self.static.refresh()

    def action_move_up(self) -> None:
        if self._cur_idx >= 0:
            self.image_table.rows[self._cur_idx].style = "none"

        if self._cur_idx == 0:
            self._cur_idx = self.image_table.row_count - 1
        else:
            self._cur_idx -= 1

        self.image_table.rows[self._cur_idx].style = "black on white"
        self.static.refresh()

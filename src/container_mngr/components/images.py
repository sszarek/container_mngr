from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from rich import box
from rich.panel import Panel
from rich.table import Table
from ..data.docker import get_images


class ImagesPanel(Widget):
    _HEADERS = ["Repository", "Tag", "Image Id", "Created", "Size"]

    def compose(self) -> ComposeResult:
        images = get_images()

        image_table = Table(
            box=box.SIMPLE_HEAVY, show_header=True, header_style="bold bright_blue"
        )

        for header in self._HEADERS:
            image_table.add_column(header)

        for image in images:
            image_table.add_row(
                image.name,
                image.tag,
                image.image_id,
                str(image.created),
                "{:.2f} MB".format(float(image.size_bytes) / 1000000),
            )

        yield Static(Panel(image_table, title="Images"))

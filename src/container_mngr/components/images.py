from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from rich.panel import Panel
from rich.table import Table
from ..data.docker import get_images


class ImagesPanel(Widget):
    _HEADERS = ["Repository", "Tag", "Image Id", "Created", "Size"]

    def compose(self) -> ComposeResult:
        images = get_images()

        image_table = Table(
            box=None,
            show_header=True,
            expand=False,
            pad_edge=False,
            show_edge=False,
        )

        for header in self._HEADERS:
            image_table.add_column(header)

        for image in images:
            image_table.add_row(
                "".join(image.attrs.get("RepoTags")),
                "latest",
                image.short_id,
                image.attrs.get("Created"),
                str(image.attrs.get("Size")),
            )

        yield Static(Panel(image_table, title="Images"))
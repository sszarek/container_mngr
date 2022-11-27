from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from ..data.docker import get_containers


class ContainersPanel(Widget):
    _HEADERS = ["Container ID", "Image", "Command", "Status", "Ports", "Names"]

    def compose(self) -> ComposeResult:
        containers = get_containers()

        renderable = (
            self._render_no_containers_info()
            if len(containers) == 0
            else self._render_containers_table(containers)
        )

        yield Static(Panel(renderable, title="Containers"))

    def _render_no_containers_info(self):
        return Text(text="No containers running", style="bold blue", justify="center")

    def _render_containers_table(self, containers):
        container_table = Table(
            box=box.SIMPLE_HEAVY, show_header=True, header_style="bold bright_blue"
        )

        for header in self._HEADERS:
            container_table.add_column(header)

        for container in containers:
            container_table.add_row(
                container.id,
                container.image,
                container.command,
                container.status,
                ", ".join(
                    [f"{port.container}:{port.host}" for port in container.ports]
                ),
                container.name,
            )

        return container_table

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from ..data.docker import get_runtime_info
from ..data.errors import ContainerRuntimeAPIError


class RuntimePanel(Widget):
    _property_mapping = {
        "NCPU": "CPU Count",
        "Architecture": "CPU Architecture",
        "Name": "Name",
        "ServerVersion": "Server Version",
        "KernelVersion": "Kernel Version",
        "OSType": "OS Type",
        "OperatingSystem": "Operating System",
        "OSVersion": "OS Version",
    }

    def compose(self) -> ComposeResult:
        content = self._render_content()

        yield Static(Panel(content, title="Runtime"))

    def _render_content(self):
        try:
            info = get_runtime_info()
            return self._render_runtime_info(info)
        except ContainerRuntimeAPIError as ex:
            return self._render_error(ex)

    def _render_runtime_info(self, runtime_info: dict[str, str]):
        property_table = Table(
            box=None, show_header=False, expand=False, pad_edge=False, show_edge=False
        )

        for key, value in self._property_mapping.items():
            property_table.add_row(
                value, Text(text=f"{runtime_info[key]}", style="Bold")
            )

        return property_table

    def _render_error(self, ex: ContainerRuntimeAPIError):
        return Text(
            f"Error while pulling runtime information: {ex.inner_error}",
            style="Bold Red",
        )

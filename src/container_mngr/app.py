from textual.app import App, ComposeResult
from textual.widgets import Static, Footer
from rich.panel import Panel
from .components.runtime import RuntimePanel
from .components.images import ImagesPanel


class ContainerMngrApp(App):
    CSS_PATH = "container_mngr_app.css"
    BINDINGS = [
        ("C-c", "toggle_containers", "Containers"),
        ("C-r", "toggle_runtime_info", "Runtime Info"),
        ("C-s", "start_new_container", "Start")
    ]

    def compose(self) -> ComposeResult:
        yield RuntimePanel()
        yield ImagesPanel()
        yield Footer()

    def toggle_runtime_info(self) -> None:
        pass

    def toggle_containers(self) -> None:
        pass

    def start_new_container(self) -> None:
        pass

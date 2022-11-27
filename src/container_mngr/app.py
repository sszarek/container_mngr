from textual.app import App, ComposeResult
from textual.widgets import Footer
from .components.runtime import RuntimePanel
from .components.images import ImagesPanel
from .components.containers import ContainersPanel


class ContainerMngrApp(App):
    CSS_PATH = "container_mngr_app.css"
    BINDINGS = [
        ("C-c", "toggle_containers", "Containers"),
        ("C-r", "toggle_runtime_info", "Runtime Info"),
        ("C-s", "start_new_container", "Start")
    ]

    def compose(self) -> ComposeResult:
        yield ContainersPanel()
        yield ImagesPanel()
        yield RuntimePanel()
        yield Footer()

    def toggle_runtime_info(self) -> None:
        pass

    def toggle_containers(self) -> None:
        pass

    def start_new_container(self) -> None:
        pass

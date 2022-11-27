from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer
from .components.screens import RuntimeScreen, ContainersScreen, ImagesScreen


class ContainerMngrApp(App):
    CSS_PATH = "container_mngr_app.css"
    TITLE = "Container Manager"
    BINDINGS = [
        ("f1", "app.switch_screen('containers')", "Containers"),
        ("f2", "app.switch_screen('runtime')", "Runtime Info"),
        ("f3", "app.switch_screen('images')", "Images"),
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=True)
    ]
    SCREENS = {
        "runtime": RuntimeScreen(),
        "images": ImagesScreen(),
        "containers": ContainersScreen()
    }

    def compose(self) -> ComposeResult:
        yield Footer()

    def on_mount(self) -> None:
        self.switch_screen("containers")

    def toggle_runtime_info(self) -> None:
        pass

    def toggle_containers(self) -> None:
        pass

    def start_new_container(self) -> None:
        pass

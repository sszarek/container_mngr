from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, TabbedContent, TabPane
from .components import ContainersPanel, ImagesPanel, RuntimePanel


class ContainerMngrApp(App):
    CSS_PATH = "container_mngr_app.css"
    TITLE = "Container Manager"
    BINDINGS = [
        ("f1", "show_tab('containers')", "Containers"),
        ("f2", "show_tab('images')", "Images"),
        ("f3", "show_tab('runtime')", "Runtime Info"),
        ("ctrl+r", "run_container", "Run container"),
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=True),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="containers"):
            with TabPane("Containers", id="containers"):
                yield ContainersPanel()
            with TabPane("Images", id="images"):
                yield ImagesPanel()
            with TabPane("Runtime", id="runtime"):
                yield RuntimePanel()

        yield Footer()

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab

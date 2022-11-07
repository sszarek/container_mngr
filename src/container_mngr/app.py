from textual.app import App, ComposeResult
from textual.widgets import Static, Footer, Placeholder


class ContainerMngrApp(App):
    CSS_PATH = "container_mngr_app.css"

    def compose(self) -> ComposeResult:
        yield Placeholder(Static("Foo Bar"), title="Containers", name="Containers")
        yield Footer()

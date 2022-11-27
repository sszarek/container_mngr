from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Footer
from .runtime import RuntimePanel
from .containers import ContainersPanel
from .images import ImagesPanel


class BaseScreen(Screen):
    def compose(self) -> ComposeResult:
        for widget in self.compose_screen():
            yield widget

        yield Footer()

    def compose_screen(self) -> ComposeResult:
        return []


class RuntimeScreen(BaseScreen):
    def compose_screen(self) -> ComposeResult:
        yield RuntimePanel()


class ImagesScreen(BaseScreen):
    def compose_screen(self) -> ComposeResult:
        yield ImagesPanel()


class ContainersScreen(BaseScreen):
    def compose_screen(self) -> ComposeResult:
        yield ContainersPanel()

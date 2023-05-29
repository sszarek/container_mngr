from abc import ABC, abstractmethod
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, DataTable
from rich.text import Text


class TableDataProvider(ABC):
    @abstractmethod
    def get_headers(self) -> list[str]:
        return []

    @abstractmethod
    def get_rows(self) -> list:
        pass


class TableWrapper(Widget):
    _data_provider: TableDataProvider
    _inner_table: DataTable
    _cur_idx: int = -1

    def __init__(
        self,
        data_provider: TableDataProvider,
        *children: Widget,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            *children, name=name, id=id, classes=classes, disabled=disabled
        )
        self._data_provider = data_provider

    def compose(self) -> ComposeResult:
        try:
            self._inner_table = DataTable(
                show_header=True,
                show_cursor=True,
            )

            yield self._inner_table
        except Exception as ex:
            yield Static(
                Text(
                    text=f"{ex}",
                    justify="center",
                    style="bold red",
                )
            )

    def on_mount(self) -> None:
        self._inner_table.add_columns(*self._data_provider.get_headers())

        self._inner_table.add_rows(self._data_provider.get_rows())

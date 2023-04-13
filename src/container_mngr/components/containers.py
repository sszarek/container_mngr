from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label
from ..data import docker
from ..data.models import Container
from ..components.table_wrapper import TableDataProvider, TableWrapper


class ContainersTableDataProvider(TableDataProvider):
    def get_headers(self) -> list[str]:
        return ["Container ID", "Image", "Command", "Status", "Ports", "Names"]

    def get_rows(self) -> list:
        containers = docker.get_containers()
        return list(map(self._map_containers, containers))

    def _map_containers(self, container: Container) -> list[str]:
        return [
            container.id,
            container.image,
            container.command,
            container.status,
            ", ".join([f"{port.container}:{port.host}" for port in container.ports]),
            container.name,
        ]


class ContainersPanel(Widget):
    _container_data_provider: ContainersTableDataProvider
    _container_table: TableWrapper

    def compose(self) -> ComposeResult:
        self._container_data_provider = ContainersTableDataProvider()
        self._container_table = TableWrapper(self._container_data_provider)

        yield Label("Containers", classes="label-center-top")
        yield self._container_table

    def action_move_down(self):
        self._container_table.action_move_down()

    def action_move_up(self):
        self._container_table.action_move_up()

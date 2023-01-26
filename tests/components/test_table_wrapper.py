import pytest
from unittest.mock import Mock
from textual.app import App, ComposeResult
from src.container_mngr.components.table_wrapper import TableWrapper, TableDataProvider
from src.container_mngr.data.errors import ContainerRuntimeAPIError


class TableWrapperTestProvider(TableDataProvider):
    def get_headers(self) -> list[str]:
        return ["col A", "col B"]

    def get_rows(self) -> list:
        return [["row 11", "row12"], ["row21", "row22"]]


class TableWrapperTestApp(App):
    _provider: TableDataProvider

    def __init__(self, provider: TableDataProvider):
        super().__init__(None, None, None)
        self._provider = provider

    def compose(self) -> ComposeResult:
        yield TableWrapper(self._provider)


@pytest.fixture
def mock_table_data_provider() -> Mock:
    table_data_provider = Mock()
    table_data_provider.get_headers = Mock(return_value=["col A", "col B"])

    return table_data_provider


@pytest.fixture
def get_success_table_data_provider(mock_table_data_provider) -> Mock:
    mock_table_data_provider.get_rows = Mock(
        return_value=[["row 11", "row12"], ["row21", "row22"]]
    )

    return mock_table_data_provider


@pytest.mark.asyncio
async def test_compose_proper_number_of_rows(get_success_table_data_provider) -> None:
    app = TableWrapperTestApp(get_success_table_data_provider)

    async with app.run_test():
        table_wrapper = app.query_one(TableWrapper)
        table = table_wrapper._inner_table
        assert table.row_count == 2


@pytest.mark.asyncio
async def test_compose_no_style_set(get_success_table_data_provider) -> None:
    app = TableWrapperTestApp(get_success_table_data_provider)

    async with app.run_test():
        table_wrapper = app.query_one(TableWrapper)
        inner_table = table_wrapper._inner_table
        assert inner_table.row_count == 2
        assert inner_table.rows[0].style is None
        assert inner_table.rows[1].style is None


@pytest.mark.asyncio
async def test_compose_error_getting_rows(mock_table_data_provider) -> None:
    error = ContainerRuntimeAPIError("Error 1", inner_error=Exception("inner"))
    mock_table_data_provider.get_rows = Mock(side_effect=error)

    app = TableWrapperTestApp(mock_table_data_provider)

    async with app.run_test():
        table_wrapper = app.query_one(TableWrapper)
        assert table_wrapper.renderable.plain == "Error 1"


@pytest.mark.asyncio
async def test_action_move_up_no_rows(mock_table_data_provider):
    mock_table_data_provider.get_rows = Mock(return_value=[])

    app = TableWrapperTestApp(mock_table_data_provider)

    async with app.run_test():
        table_wrapper = app.query_one(TableWrapper)
        table_wrapper.action_move_up()


@pytest.mark.asyncio
async def test_action_move_down_highlight_style_set(get_success_table_data_provider):
    app = TableWrapperTestApp(get_success_table_data_provider)

    async with app.run_test():
        table_wrapper = app.query_one(TableWrapper)
        table_wrapper.action_move_down()
        inner_table = table_wrapper._inner_table
        assert inner_table.rows[0].style is not None
        assert inner_table.rows[1].style is None

        table_wrapper.action_move_down()
        assert inner_table.rows[0].style is None
        assert inner_table.rows[1].style is not None

        table_wrapper.action_move_down()
        assert inner_table.rows[0].style is not None
        assert inner_table.rows[1].style is None


@pytest.mark.asyncio
async def test_action_move_up_highlight_style_set(get_success_table_data_provider):
    app = TableWrapperTestApp(get_success_table_data_provider)

    async with app.run_test():
        table_wrapper = app.query_one(TableWrapper)
        table_wrapper.action_move_up()
        inner_table = table_wrapper._inner_table
        assert inner_table.rows[0].style is None
        assert inner_table.rows[1].style is not None

        table_wrapper.action_move_down()
        assert inner_table.rows[0].style is not None
        assert inner_table.rows[1].style is None

        table_wrapper.action_move_down()
        assert inner_table.rows[0].style is None
        assert inner_table.rows[1].style is not None

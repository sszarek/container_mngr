import pytest
from dateutil.tz import tzutc
from datetime import datetime
from unittest.mock import Mock
from docker import DockerClient
from docker.errors import APIError
from docker.models.images import Image as DockerImage
from src.container_mngr.data.models import ContainerRuntimeInfo
from src.container_mngr.data.docker import get_runtime_info, get_images
from src.container_mngr.data.errors import ContainerRuntimeAPIError, ModelMappingError


@pytest.fixture
def mock_env_client(monkeypatch):
    env_client_mock = Mock()
    from_env_mock = Mock(return_value=env_client_mock)
    monkeypatch.setattr(DockerClient, "from_env", staticmethod(from_env_mock))
    return env_client_mock


@pytest.fixture
def mock_get_info(mock_env_client) -> Mock:
    info_mock = Mock()
    mock_env_client.info = info_mock

    return info_mock


@pytest.fixture
def mock_images(mock_env_client) -> Mock:
    images_mock = Mock()
    mock_env_client.images = images_mock

    return images_mock


def test_runtime_info_returns_valid_response(mock_get_info: Mock):
    runtime_dict = {
        "NCPU": 2,
        "Architecture": "x86",
        "KernelVersion": "1.0.0",
        "Name": "redis",
        "OperatingSystem": "Windows",
        "OSType": "Linux",
        "OSVersion": "2.0.0",
        "ServerVersion": "3.0.0",
    }

    mock_get_info.return_value = runtime_dict

    actual = get_runtime_info()

    assert actual == ContainerRuntimeInfo(
        cpu_count=runtime_dict["NCPU"],
        cpu_architecture=runtime_dict["Architecture"],
        kernel_version=runtime_dict["KernelVersion"],
        name=runtime_dict["Name"],
        os=runtime_dict["OperatingSystem"],
        os_type=runtime_dict["OSType"],
        os_version=runtime_dict["OSVersion"],
        server_version=runtime_dict["ServerVersion"],
    )


def test_runtime_info_raises_exception(mock_get_info: Mock):
    error = APIError("something wrong happened")

    mock_get_info.side_effect = error

    with pytest.raises(ContainerRuntimeAPIError):
        get_runtime_info()


def test_runtime_info_invalid_response(mock_get_info: Mock):
    runtime_dict = {
        "NCPU": 1,
        "Architecture": "x86",
        "KernelVersion": "1.0.0",
        "Name": "redis",
        "OperatingSystem": "Windows",
    }

    mock_get_info.return_value = runtime_dict

    with pytest.raises(ModelMappingError) as err:
        get_runtime_info()

    assert (
        str(err.value) == "Error mapping from Docker API response."
        " Missing expected fields: OSType, OSVersion, ServerVersion"
    )


def test_get_images_returns_valid_response(mock_images):
    images_dict = [
        DockerImage(
            attrs={
                "RepoTags": ["redis:latest"],
                "Id": "sha:3358aea34e8c871cc2ecec590dcefcf0945e76ec3f82071f30156ed1be97a5fb",  # noqa E501
                "Created": "2022-11-15T14:41:42.98180605Z",
                "Size": 116950664,
            }
        )
    ]

    mock_images.list = Mock(return_value=images_dict)

    actual = get_images()

    assert len(actual) == 1
    assert actual[0].created == datetime(
        2022, 11, 15, 14, 41, 42, 981806, tzinfo=tzutc()
    )
    assert (
        actual[0].image_id
        == "3358aea34e8c871cc2ecec590dcefcf0945e76ec3f82071f30156ed1be97a5fb"
    )  # noqa E501
    assert actual[0].name == "redis"
    assert actual[0].size_bytes == 116950664
    assert actual[0].tag == "latest"

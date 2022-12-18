import pytest
from unittest.mock import Mock
from docker import DockerClient
from docker.errors import APIError
from docker.models.images import Image as DockerImage
from src.container_mngr.data.models import ContainerRuntimeInfo, Image
from src.container_mngr.data.docker import get_runtime_info
from src.container_mngr.data.errors import ContainerRuntimeAPIError, ModelMappingError


def patch_docker_client_info_response(monkeypatch, response):
    env_client_mock = Mock()
    env_client_mock.info = Mock(return_value=response)

    from_env_mock = Mock(return_value=env_client_mock)
    monkeypatch.setattr(DockerClient, "from_env", staticmethod(from_env_mock))


def patch_docker_client_info_error(monkeypatch, error):
    env_client_mock = Mock()
    env_client_mock.info = Mock(side_effect=error)

    from_env_mock = Mock(return_value=env_client_mock)
    monkeypatch.setattr(DockerClient, "from_env", staticmethod(from_env_mock))


@pytest.fixture
def mock_get_info(monkeypatch):
    info_mock = Mock()
    env_clien_mock = Mock()
    env_clien_mock.info = info_mock

    from_env_mock = Mock(return_value=env_clien_mock)
    monkeypatch.setattr(DockerClient, "from_env", staticmethod(from_env_mock))
    return info_mock


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
    # patch_docker_client_info_response(monkeypatch, runtime_dict)

    with pytest.raises(ModelMappingError) as err:
        get_runtime_info()

    assert (
        str(err.value) == "Error mapping from Docker API response."
        " Missing expected fields: OSType, OSVersion, ServerVersion"
    )


def test_get_images_returns_valid_response():
    images_dict = [
        DockerImage(attrs={
            "RepoTags": ["redis:latest"],
            "Id": "sha:3358aea34e8c871cc2ecec590dcefcf0945e76ec3f82071f30156ed1be97a5fb",
            "Created": "2022-11-15T14:41:42.98180605Z",
            "Size": 116950664
        })
    ]

    # TODO add proper assertion
    assert images_dict is not None

import pytest
from unittest.mock import Mock
from docker import DockerClient
from docker.errors import APIError
from src.container_mngr.data.models import ContainerRuntimeInfo
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


def test_runtime_info_returns_valid_response(monkeypatch):
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

    patch_docker_client_info_response(monkeypatch, runtime_dict)

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


def test_runtime_info_raises_exception(monkeypatch):
    error = APIError("something wrong happened")

    patch_docker_client_info_error(monkeypatch, error)

    with pytest.raises(ContainerRuntimeAPIError):
        get_runtime_info()


def test_runtime_info_invalid_response(monkeypatch):
    runtime_dict = {
        "NCPU": 1,
        "Architecture": "x86",
        "KernelVersion": "1.0.0",
        "Name": "redis",
        "OperatingSystem": "Windows",
    }

    patch_docker_client_info_response(monkeypatch, runtime_dict)

    with pytest.raises(ModelMappingError) as err:
        get_runtime_info()

    assert (
        str(err.value) == "Error mapping from Docker API response."
        " Missing expected fields: OSType, OSVersion, ServerVersion"
    )

# import os
# os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"

from base_aux.base_types.m2_info import ObjectInfo
import docker
# import testcontainers


# =====================================================================================================================
class _Docker_ExcVariants:
    DOCKER_DESCTOP = "docker.errors.DockerException: Error while fetching server API version: (2, 'CreateFile', 'Не удается найти указанный файл.')"
    MODULES_UPDATE = "docker.errors.DockerException: Error while fetching server API version: Not supported URL scheme http+docker"
    TESTCONTAINERS_ENV = "ConnectionError: Port mapping for container f58f05a18244edddfce5034e809dfe2cd6d4e36284e19f974e260c7ebbcd8f17 and port 8080 is not available"


# =====================================================================================================================
def docker__check_ready_os() -> bool:
    result = None

    try:
        client = docker.from_env()
        print(f"{client.ping()=}")  # Должно вернуть True
        print(f"{client.version()=}")

        result = client.ping()
    except docker.errors.DockerException as exc:
        print(f"{exc!r}")
        ObjectInfo(exc).print()

        if "CreateFile" in str(exc):
            print(f"[err/docker] DockerDesctop NOT started!")

        elif "URL scheme" in str(exc):
            print(f"[err/docker] OLD MODULES => update all modules like 'pip install --upgrade testcontainers docker sqlalchemy psycopg2-binary'")

        result = False

    except BaseException as exc:
        print(f"[err/docker] UNEXPECTED {exc!r}")
        ObjectInfo(exc).print()
        result = False

    print(f"docker__check_ready_os({result=})")
    return result


# =====================================================================================================================
if __name__ == "__main__":
    docker__check_ready_os()


# =====================================================================================================================

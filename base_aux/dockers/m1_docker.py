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
    try:
        client = docker.from_env()
        print(f"{client.ping()=}")  # Должно вернуть True
        print(f"{client.version()=}")

        result = client.ping()
    except docker.errors.DockerException as exc:
        print(f"{exc!r}")
        ObjectInfo(exc).print()

        if "CreateFile" in str(exc):
            print(f"[err/docker] Windows DockerDesctop NOT started!")

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
class Docker:
    def __init__(self):
        self.client = docker.from_env()
        pass

    def connect(self):
        """
        GOAL
        ----
        """

    def run(self, image: str = "ubuntu:latest", cmd: str = "echo hello world", detach=True):
        self.client.containers.run(image, cmd, detach=detach)
        # <Container '45e6d2de7c54'>
        print(f"{self.client=}")

    def cont__list(self):
        cont_list = self.client.containers.list()
        print(f"{cont_list=}")
        # [<Container '45e6d2de7c54'>, <Container 'db18e4f20eaa'>, ...]

        if not cont_list:
            return

        try:
            self.container = self.client.containers.get('45e6d2de7c54')
            print(f"{self.container=}")
        except:
            return

        cont_attrs = self.container.attrs['Config']['Image']  # "bfirsh/reticulate-splines"
        print(f"{cont_attrs=}")

        print(f"{self.container.logs()=}")
        "Reticulating spline 1...\n"

        self.container.stop()

    def cont__stream_logs(self):
        for line in self.container.logs(stream=True):
            print(line.strip())

    def images__list(self):
        images_list = self.client.images.list()
        # [<Image 'ubuntu'>, <Image 'nginx'>, ...]
        print(f"{images_list=}")


# =====================================================================================================================
if __name__ == "__main__":
    assert docker__check_ready_os()

    docker = Docker()
    docker.run()
    docker.cont__list()


# =====================================================================================================================

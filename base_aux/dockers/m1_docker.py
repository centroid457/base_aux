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
    print()
    return result


# =====================================================================================================================
class DockerMan:
    def __init__(
            self,
            image_name: str = "ubuntu:latest",
            container_name: str = "test_container",
    ):
        self.image_name: str = image_name
        self.container_name: str = container_name

        self._client: docker.client.DockerClient | None = None
        self.container = None

    def connect(self) -> bool:
        """
        GOAL
        ----
        create connection to the system docker service-daemon!
        """
        result = True
        try:
            self._client = docker.from_env()     # connect to daemon!
        except BaseException as exc:
            print(f"{exc!r}")
            result = False

        print(f"connect/{result=}")
        return True

    def run_img(self) -> bool:
        """
        GOAL
        ----
        run image - create container
        """
        result = True

        # check old/existed
        try:
            old_container = self._client.containers.get(self.container_name)
            print(f"old exists: {old_container.id=}")

            if old_container.status == "running":
                print("old.stopping...")
                old_container.stop()
                print("old.stopped...")

            print("old.deleting...")
            old_container.remove()
            print("old.deleted...")
        except docker.errors.NotFound:
            print("Старый контейнер не найден, создаю новый...")
        except docker.errors.APIError as e:
            print(f"Ошибка при удалении старого контейнера: {e}")

        try:
            self.container = self._client.containers.run(
                image=self.image_name,
                name=self.container_name,
                # command=None,   # str/list
                command="tail -f /dev/null",  # Бесконечная команда для поддержания работы иначе контейнер будет остановлен!!
                detach=True,
                remove=True,    # autoremove cont after stop
            )
            """
            DETACH
                if TRUE return ContainerCollection
                FALSE - bytes (as cmd answer!)
                bytes | docker.client.ContainerCollection
                
                detach=True/result=<Container: 153d16781ab9>    # OBJECT
                detach=False/result=b'hello world\n'            # OUTPUT
            """
        except BaseException as exc:
            print(f"{exc!r}")
            result = False

        print(f"run_img//{self.image_name=}/{self.container_name=}/{result=}")
        return result

    def send_cmd(
            self,
            cmd: str = "echo hello world",
    ) -> str:
        result = self.container.exec_run(cmd)
        result = result.output.decode('utf-8') if result.output else ""
        print(f"send_cmd//{cmd=}/{result=}")
        return result

    # ---------------------------------------------------------------------------------
    def cont__list(self):
        cont_list = self._client.containers.list()
        print(f"{cont_list=}")
        # [<Container '45e6d2de7c54'>, <Container 'db18e4f20eaa'>, ...]

        if not cont_list:
            return

        try:
            self.container = self._client.containers.get('45e6d2de7c54')
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
        images_list = self._client.images.list()
        # [<Image 'ubuntu'>, <Image 'nginx'>, ...]
        print(f"{images_list=}")


# =====================================================================================================================
if __name__ == "__main__":
    assert docker__check_ready_os()

    docker_man = DockerMan()
    docker_man.connect()
    docker_man.run_img()
    print()
    docker_man.send_cmd(f"echo hello 111")
    docker_man.send_cmd(f"date")
    docker_man.send_cmd(f"uname -a")
    docker_man.send_cmd(f"ping localhost")
    docker_man.send_cmd(f"echo hello 222")
    docker_man.send_cmd(f"ping")
    docker_man.send_cmd(f"ping ya.ru")

    # docker_man.run(detach=False)

    # result = docker_man.run(detach=True)
    #
    # print()
    # ObjectInfo(result).print()
    # print()
    # ObjectInfo(result._client).print()

    # docker_man.cont__list()


# =====================================================================================================================

# import os
# os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"

from base_aux.base_types.m2_info import ObjectInfo
import docker
# from docker.models.containers import Container
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

        self._client_daemon: docker.client.DockerClient | None = None
        self.container: docker.models.containers.Container | None = None

    def connect_daemon(self) -> bool:
        """
        GOAL
        ----
        create connection to the system docker service-daemon!
        """
        result = True
        if self._client_daemon is None:
            try:
                # connect to daemon!
                # any call - always create new object!
                self._client_daemon = docker.from_env()
            except BaseException as exc:
                print(f"{exc!r}")
                result = False
        else:
            print(f"connect_daemon//already existed")

        print(f"connect_daemon/{result=}")
        return True

    def run_container(self) -> bool:
        """
        GOAL
        ----
        run image - create container
        """
        result = True
        old_container: docker.models.containers.Container

        # check old/existed
        try:
            old_container = self._client_daemon.containers.get(self.container_name)
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
        except docker.errors.APIError as exc:
            print(f"Ошибка при удалении старого контейнера: {exc!r}")
        except BaseException as exc:
            print(f"[unexpected] {exc!r}")

        try:
            self.container = self._client_daemon.containers.run(
                image=self.image_name,
                name=self.container_name,
                # command=None,   # str/list
                command="tail -f /dev/null",  # Бесконечная команда для поддержания работы иначе контейнер будет остановлен!!
                detach=True,
                # remove=True,    # autoremove cont after stop
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

    def stop_container(self) -> bool:
        """
        GOAL
        ----
        finish working with container!
        stop/remove container
        """
        try:
            if self.container.status == "running":
                print("container.stopping...")
                self.container.stop()
                print("container.stopped...")

            print("container.deleting...")
            self.container.remove()
            print("container.deleted...")
            return True

        except BaseException as exc:
            print(f"[unexpected] {exc!r}")

        return False

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
        cont_list = self._client_daemon.containers.list()
        print(f"{cont_list=}")
        # [<Container '45e6d2de7c54'>, <Container 'db18e4f20eaa'>, ...]

        if not cont_list:
            return

        try:
            self.container = self._client_daemon.containers.get('45e6d2de7c54')
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
        images_list = self._client_daemon.images.list()
        # [<Image 'ubuntu'>, <Image 'nginx'>, ...]
        print(f"{images_list=}")


# =====================================================================================================================
if __name__ == "__main__":
    assert docker__check_ready_os()

    docker_man = DockerMan()
    docker_man.connect_daemon()
    docker_man.run_container()
    print()
    docker_man.send_cmd(f"echo hello 111")
    docker_man.send_cmd(f"date")
    docker_man.send_cmd(f"uname -a")
    docker_man.send_cmd(f"ping localhost")
    docker_man.send_cmd(f"echo hello 222")
    docker_man.send_cmd(f"ping")
    docker_man.send_cmd(f"free -m")
    """
    send_cmd//cmd='free -m'/result='               total        used        free      shared  buff/cache   available\nMem:            7788         920        6563           5         468        6867\nSwap:           2048           0        2048\n'
    
    C:\\Users\a.starichenko>docker run busybox free -m
                  total        used        free      shared  buff/cache   available
    Mem:           7788         730        5110           5        1948        6900
    Swap:          2048           0        2048
    
    C:\\Users\a.starichenko>
    """
    docker_man.send_cmd(f"ps aux")
    """
    send_cmd//cmd='ps aux'/result='USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\nroot           1  1.2  0.0   2728  1280 ?        Ss   10:18   0:00 tail -f /dev/null\nroot          49 40.0  0.0   7888  3712 ?        Rs   10:18   0:00 ps aux\n'
    
    C:\\Users\a.starichenko>docker run busybox ps aux
    PID   USER     TIME  COMMAND
        1 root      0:00 ps aux
    
    C:\\Users\a.starichenko>
    """

    docker_man.stop_container()

    # docker_man.run(detach=False)

    # result = docker_man.run(detach=True)
    #
    # print()
    # ObjectInfo(result).print()
    # print()
    # ObjectInfo(result._client_daemon).print()

    # docker_man.cont__list()


# =====================================================================================================================

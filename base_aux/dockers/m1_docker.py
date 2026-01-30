from typing import *

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
class DockerMan:
    def __init__(
            self,
            image_name: str = "ubuntu",
            container_name: str = "test_container",

            raised: bool = True
    ) -> None | NoReturn:
        self.image_name: str = image_name
        self.container_name: str = container_name

        self._daemon_client: docker.client.DockerClient | None = None
        self.container: docker.models.containers.Container | None = None

        if not self.docker__check_ready_os() and raised:
            msg = f"DockerMan.docker__check_ready_os=False"
            raise Exception(msg)

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def docker__check_ready_os() -> bool:
        try:
            client = docker.from_env()
            print(f"{client.ping()=}")  # Должно вернуть True
            print(f"{client.version()=}")

            result = client.ping()
        except docker.errors.DockerException as exc:
            print(f"{exc!r}")
            # ObjectInfo(exc).print()

            if "CreateFile" in str(exc):
                print(f"[err/docker] Windows DockerDesctop NOT started!")

            elif "URL scheme" in str(exc):
                print(
                    f"[err/docker] OLD MODULES => update all modules like 'pip install --upgrade testcontainers docker sqlalchemy psycopg2-binary'")

            result = False

        except BaseException as exc:
            print(f"[docker] UNEXPECTED {exc!r}")
            # ObjectInfo(exc).print()
            result = False

        print(f"docker__check_ready_os({result=})")
        print()
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def daemon_connect(self) -> bool:
        """
        GOAL
        ----
        create connection to the system docker service-daemon!
        """
        result = True
        if self._daemon_client is None:
            try:
                # connect to daemon!
                # any call - always create new object!
                self._daemon_client = docker.from_env()
            except BaseException as exc:
                print(f"{exc!r}")
                result = False
        else:
            print(f"connect_daemon//already existed")

        print(f"connect_daemon/{result=}")
        return True

    # -----------------------------------------------------------------------------------------------------------------
    def images_list(self) -> list[docker.models.containers.Image]:
        """
        GOAL
        ----
        show all already downloaded (used before) images in system


            item=<Image: ''>
            item=<Image: ''>
            item=<Image: 'ubuntu:latest'>
            item=<Image: 'rabbitmq:latest'>
            item=<Image: 'reponame:latest'>
            item=<Image: '4volume-2compose-app:latest'>
            item=<Image: 'flask_only:latest'>
            item=<Image: 'hello-web1:latest'>
            item=<Image: 'myflask:latest'>
            item=<Image: 'redis:alpine'>
            item=<Image: 'myrepo:latest'>
            item=<Image: 'hello-web:latest'>
            item=<Image: 'project-web:latest'>
            item=<Image: 'python:3.10-alpine'>
            item=<Image: 'python:latest'>
            item=<Image: 'alpine:latest'>
            item=<Image: 'rabbitmq:management'>
            item=<Image: 'busybox:latest'>
            item=<Image: 'rabbitmq:3-management'>
            item=<Image: 'testcontainers/ryuk:0.8.1'>
        """
        images_list = self._daemon_client.images.list(
            # name="ubuntu",
            # can use only FULL name! like ubuntu (for any variants ubuntu:latest/...)
            # PART names is not working!
            # all=True,
        )
        for item in images_list:
            print(f"\t{item=}")
        return images_list

    # -----------------------------------------------------------------------------------------------------------------
    def containers_list(self) -> list[docker.models.containers.Container]:
        """
        GOAL
        ----
        show list of existed containers
        """
        cont_list = self._daemon_client.containers.list()
        print(f"containers_list.COUNT/{len(cont_list)=}")
        for item in cont_list:
            print(f"\t{item=}")

        return cont_list

    def container_start(self) -> bool:
        """
        GOAL
        ----
        run image - create container or get old existed
        """
        result = True
        old_container: docker.models.containers.Container | None = None

        # 1=old check exists ------------
        try:
            old_container = self._daemon_client.containers.get(self.container_name)
            print(f"old exists: {old_container.id=}")
        except docker.errors.NotFound:
            print(f"old NOT exists")
        except BaseException as exc:
            print(f"old [unexpected] {exc!r}")

        # 2=old try remove ------------
        if old_container is not None:
            try:
                if old_container.status == "running":
                    self.container = old_container
                    print(f"[OK]run_container = already exists")
                    # no need to stop old and start new

                    # print("old.stopping...")
                    # old_container.stop()
                    # print("old.stopped...")

                print("old.removing...")
                old_container.remove()
                print("old.removed...")

            except docker.errors.APIError as exc:
                print(f"Ошибка при удалении старого контейнера: {exc!r}")
            except BaseException as exc:
                print(f"[unexpected] {exc!r}")

        # 3=start new ------------
        if self.container is None:
            try:
                self.container = self._daemon_client.containers.run(
                    image=self.image_name,
                    name=self.container_name,
                    # command=None,   # str/list
                    command="tail -f /dev/null",  # Бесконечная команда для поддержания работы иначе контейнер будет остановлен!!
                    detach=True,
                    remove=True,    # autoremove container after stop
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

        # ----------------------
        cont_attrs = self.container.attrs['Config']['Image']    # "bfirsh/reticulate-splines"
        print(f"{cont_attrs=}")
        # ----------------------
        print(f"run_container//{self.image_name=}/{self.container_name=}/{result=}")
        return result

    def container_stop(self) -> bool:
        """
        GOAL
        ----
        finish working with container!
        stop/remove container
        """
        if self.container is None:
            return True

        try:
            if self.container.status == "running":
                print("container.stopping...")
                self.container.stop()
                print("container.stopped...")

            print("container.removing...")
            self.container.remove()
            print("container.removed...")
            return True

        except BaseException as exc:    # FIXME: separate excs
            print(f"[unexpected] {exc!r}")

        return False

    # -----------------------------------------------------------------------------------------------------------------
    def container_send(
            self,
            cmd: str = "echo HELLO WORLD",
    ) -> str:
        """
        GOAL
        ----
        send cmd to container
        return answer

        EXAMPLES
        --------
        1=docker_man.send_cmd(f"free -m")
            send_cmd//cmd='free -m'/result='               total        used        free      shared  buff/cache   available\nMem:            7788         920        6563           5         468        6867\nSwap:           2048           0        2048\n'

            C:\\Users\a.starichenko>docker run busybox free -m
                          total        used        free      shared  buff/cache   available
            Mem:           7788         730        5110           5        1948        6900
            Swap:          2048           0        2048

            C:\\Users\a.starichenko>

        2=docker_man.send_cmd(f"ps aux")
            send_cmd//cmd='ps aux'/result='USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\nroot           1  1.2  0.0   2728  1280 ?        Ss   10:18   0:00 tail -f /dev/null\nroot          49 40.0  0.0   7888  3712 ?        Rs   10:18   0:00 ps aux\n'

            C:\\Users\a.starichenko>docker run busybox ps aux
            PID   USER     TIME  COMMAND
                1 root      0:00 ps aux

            C:\\Users\a.starichenko>
        """
        result = self.container.exec_run(cmd)
        result = result.output.decode('utf-8') if result.output else ""
        print(f"send_cmd//{cmd=}/{result=}")
        return result

    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def container__stream_logs(self) -> Never:  # FIXME; dont understand what it is!!!
        """
        GOAL
        ----
        start streaming stdout
        blocking point!!!
        """
        for line in self.container.logs(stream=True):
            print(line.strip())


# =====================================================================================================================
if __name__ == "__main__":
    assert DockerMan.docker__check_ready_os()

    docker_man = DockerMan()
    docker_man.daemon_connect()
    # docker_man.containers_list()

    docker_man.container_start()

    docker_man.container_send(f"echo hello 111")
    docker_man.container_send(f"date")
    # docker_man.container_send("watch echo 1")
    # docker_man.container_send("printf 'HelloWorld\n%.0s' {1..5}")
    docker_man.container_send(f"ping localhost")

    # docker_man.container__stream_logs()

    # ObjectInfo(docker_man.container).print()
    # docker_man.container_send(f"echo hello 222")
    # docker_man.container_send(f"ping")


# =====================================================================================================================

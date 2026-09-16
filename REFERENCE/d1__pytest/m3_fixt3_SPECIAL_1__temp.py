import pytest


# ======================================================================================================================
# 1. ВРЕМЕННЫЕ ФАЙЛЫ И КАТАЛОГИ (tmp_path, tmpdir)
# =============================================================================
def test_create_temp_file(tmp_path):
    """tmp_path — pathlib.Path к уникальной временной папке."""
    file = tmp_path / "data.txt"
    file.write_text("pytest")
    assert file.read_text() == "pytest"
    # После теста папка удаляется автоматически

def test_temp_dir_structure(tmp_path):
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    (sub_dir / "f1.txt").write_text("content")
    assert len(list(sub_dir.iterdir())) == 1

# -----------------------------------------------------------------------------
# ВАЖНО: tmp_path уникален для каждого теста (scope="function").
# Не сохраняйте абсолютные пути на диск за пределами теста – папка будет удалена.
# -----------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 1. tmp_path — временная папка (function scope)
# ---------------------------------------------------------------------------
def test_tmp_path_example(tmp_path):
    # tmp_path — pathlib.Path, уникальная папка, удаляется после теста
    file = tmp_path / "data.txt"
    file.write_text("hello")
    assert file.read_text() == "hello"

# Ошибка: нельзя использовать tmp_path в фикстуре со scope != "function"
# (например, scope="class", "module", "session").
# Для session-уровня используйте tmp_path_factory.

# ---------------------------------------------------------------------------
# 2. tmp_path_factory — фабрика временных папок (session scope)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def session_dir(tmp_path_factory):
    # Можно создать одну папку на всю сессию
    dir = tmp_path_factory.mktemp("my_session_data")
    (dir / "config.ini").write_text("[config]")
    return dir


def test_session_uses_factory(session_dir):
    assert (session_dir / "config.ini").read_text() == "[config]"


# ======================================================================================================================

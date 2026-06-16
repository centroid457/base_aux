import pytest
from base_aux.aux_text.m9_path_tree import PathTree, PathNode


# ======================================================================================================================
class TestEventPath:
    """Тесты класса PathNode."""

    def test_eq_string(self, sample_tree):
        """PathNode должен сравниваться со строкой по полному пути."""
        assert sample_tree.ch1.stdin == "ch1.stdin"

    def test_eq_other_eventpath(self, sample_tree):
        """Два PathNode с одинаковым путём должны быть равны."""
        a = sample_tree.ch1.stdin
        b = sample_tree.ch1.stdin
        assert a == b
        assert not (a != b)

    def test_neq_different_path(self, sample_tree):
        """Разные пути не равны."""
        assert sample_tree.ch1.stdin != sample_tree.ch1.stdout

    def test_hash(self, sample_tree):
        """PathNode должен быть хешируем (равные объекты – равный хеш)."""
        a = sample_tree.ch1.stdin
        b = sample_tree.ch1.stdin
        assert hash(a) == hash(b)
        s = {a}
        assert b in s

    def test_repr(self, sample_tree):
        """repr должен содержать путь."""
        r = repr(sample_tree.ch1.stdin)
        assert "PathNode" in r
        assert "ch1.stdin" in r

    def test_str(self, sample_tree):
        """str должен возвращать путь."""
        assert str(sample_tree.ch1.stdin) == "ch1.stdin"

    def test_path_property(self, sample_tree):
        """Свойство path возвращает точечную строку."""
        assert sample_tree.ch1.stdin.path == "ch1.stdin"

    def test_access_child_of_terminal(self, sample_tree):
        """Нельзя получить атрибут у терминального события (листа)."""
        with pytest.raises(AttributeError):
            _ = sample_tree.ch1.stdin.anything

    def test_access_nonexistent_child(self, sample_tree):
        """Нельзя получить атрибут, отсутствующий в промежуточном узле."""
        with pytest.raises(AttributeError):
            _ = sample_tree.ch1.nonexistent

    def test_access_private_attr(self, sample_tree):
        """Приватные атрибуты не должны делегироваться в схему."""
        with pytest.raises(AttributeError):
            _ = sample_tree.ch1._private


# ======================================================================================================================
class TestNamesInitialization:
    """Тесты создания PathTree."""

    def test_empty_names(self):
        """Пустой PathTree не имеет каналов."""
        n = PathTree()
        with pytest.raises(AttributeError):
            _ = n.anything

    def test_init_with_sets(self):
        """Инициализация с множествами как листьями."""
        n = PathTree(io={"stdin", "stdout"})
        assert n.io.stdin == "io.stdin"
        assert n.io.stdout == "io.stdout"

    def test_init_with_nested_dicts(self):
        """Инициализация с вложенными словарями."""
        n = PathTree(
            app={
                "startup": None,
                "shutdown": None,
                "network": {"send", "recv"}
            }
        )
        assert n.app.startup == "app.startup"
        assert n.app.network.send == "app.network.send"

    def test_init_bad_type(self):
        """Нельзя передавать значения, отличные от set/dict/None."""
        with pytest.raises(TypeError):
            PathTree(bad=123)  # целое число вместо множества/словаря
        with pytest.raises(TypeError):
            PathTree(bad="string")  # строка вместо множества/словаря


# ======================================================================================================================
class TestNamesMerge:
    """Тесты метода merge_schema."""

    def test_add_new_terminal(self, sample_tree):
        """Добавление нового терминального события."""
        sample_tree.merge_schema(ch1={"st"})
        assert sample_tree.ch1.st == "ch1.st"

    def test_add_new_branch(self, sample_tree):
        """Добавление целой ветки."""
        sample_tree.merge_schema(ch1={"st": {"st1", "st2"}})
        assert sample_tree.ch1.st.st1 == "ch1.st.st1"
        assert sample_tree.ch1.st.st2 == "ch1.st.st2"

    def test_extend_terminal_into_branch(self, sample_tree):
        """Превращение существующего листа в промежуточный узел (добавление дочерних)."""
        # sample_names.ch1.stdin сейчас лист
        sample_tree.merge_schema(ch1={"stdin": {"bytes", "lines"}})
        # теперь stdin – не лист, но доступ к .stdin всё ещё даёт PathNode (промежуточный)
        assert sample_tree.ch1.stdin.bytes == "ch1.stdin.bytes"
        assert sample_tree.ch1.stdin.lines == "ch1.stdin.lines"
        # Важно: предыдущее прямое сравнение как строки "ch1.stdin" теперь не будет работать,
        # потому что узел ch1.stdin теперь словарь, а не None, и PathNode('ch1.stdin') не имеет __eq__ со строкой?
        # Проверим: на самом деле PathNode сравнивается со строкой по пути, и путь остался 'ch1.stdin'
        assert sample_tree.ch1.stdin == "ch1.stdin"  # по-прежнему должен работать

    def test_merge_preserves_existing(self, sample_tree):
        """Слияние не ломает существующие элементы."""
        old_path = sample_tree.ch1.stdin
        sample_tree.merge_schema(ch1={"extra"})
        assert sample_tree.ch1.stdin == "ch1.stdin"
        assert sample_tree.ch1.extra == "ch1.extra"

    def test_merge_multiple_channels(self, sample_tree):
        """Слияние нескольких каналов одновременно."""
        sample_tree.merge_schema(
            ch1={"new1"},
            ch2={"new2": {"sub"}},
            new_ch={"x", "y"},
        )
        assert sample_tree.ch1.new1 == "ch1.new1"
        assert sample_tree.ch2.new2.sub == "ch2.new2.sub"
        assert sample_tree.new_ch.x == "new_ch.x"

    def test_merge_empty(self, sample_tree):
        """Слияние пустого набора не меняет ничего и не вызывает ошибок."""
        old_events = list_all_events(sample_tree)
        sample_tree.merge_schema()
        assert list_all_events(sample_tree) == old_events


class TestAttributeError:
    """Тесты на ожидаемые ошибки."""

    def test_root_channel_missing(self, sample_tree):
        """Обращение к несуществующему корневому каналу – AttributeError."""
        with pytest.raises(AttributeError):
            _ = sample_tree.nonexistent

    def test_missing_leaf(self, sample_tree):
        """Обращение к отсутствующему событию внутри существующего канала."""
        with pytest.raises(AttributeError):
            _ = sample_tree.ch1.missing

    def test_missing_nested(self, sample_tree):
        """Обращение к отсутствующему вложенному событию."""
        sample_tree.merge_schema(ch1={"a": {"b"}})
        with pytest.raises(AttributeError):
            _ = sample_tree.ch1.a.c  # b есть, c – нет


# ======================================================================================================================
class TestPathNodeContains:
    def test_node_in_parent(self, sample_tree):
        node = sample_tree.ch1.stdin
        assert node in sample_tree.ch1

    def test_string_in_parent(self, sample_tree):
        assert "ch1.stdout" in sample_tree.ch1

    def test_node_not_in_wrong_channel(self, sample_tree):
        assert sample_tree.ch2.startup not in sample_tree.ch1

    def test_nonexistent_string_not_in(self, sample_tree):
        assert "ch1.nonexistent" not in sample_tree.ch1

    def test_node_contains_self(self, sample_tree):
        node = sample_tree.ch1.stdin
        assert node in node   # или "ch1.stdin" in node

    def test_child_not_contained_by_child_of_other(self, sample_tree):
        # После расширения: добавляем вложенное событие
        sample_tree.merge_schema(ch1={"stdin": {"bytes", "lines"}})
        assert "ch1.stdin.bytes" in sample_tree.ch1
        assert sample_tree.ch1.stdin.bytes in sample_tree.ch1


# ======================================================================================================================
# --------------------------------------------------------------------
# Вспомогательные функции и фикстуры
# --------------------------------------------------------------------
def list_all_events(names: PathTree) -> set:
    """Рекурсивно собирает все полные пути событий (терминальных узлов)."""
    events = set()

    def traverse(node: dict, prefix: str):
        for key, child in node.items():
            path = f"{prefix}.{key}" if prefix else key
            if child is None:
                events.add(path)
            elif isinstance(child, dict):
                if not child:  # пустой словарь считается терминальным?
                    # в нашей модели пустой словарь не образуется, но на всякий случай
                    events.add(path)
                else:
                    traverse(child, path)
            else:
                # не должно случиться
                raise TypeError(f"Unexpected node type: {type(child)}")

    traverse(names._schema, "")
    return events


@pytest.fixture
def sample_tree():
    """Базовая схема для большинства тестов."""
    return PathTree(
        ch1={"stderr", "stdin", "stdout"},
        ch2={"startup", "test", "teardown"},
    )


# ======================================================================================================================

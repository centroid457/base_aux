from typing import *


# ======================================================================================================================
class PathNode:
    """
    Представляет полный путь события (например, "ch1.stdin").
    Поддерживает доступ к дочерним элементам через атрибут,
    а также сравнение со строками.
    """
    __slots__ = ('_parts', '_schema')

    def __init__(self, parts: list[str], schema: dict):
        self._parts = parts          # список компонентов пути, например ['ch1', 'stdin']
        self._schema = schema        # корневой словарь всей схемы

    @property
    def path(self) -> str:
        """Полный путь в точечной нотации."""
        return ".".join(self._parts)

    def _get_node(self) -> dict:
        """Возвращает словарь текущего уровня (может быть пустым, если терминальный узел)."""
        node = self._schema
        for part in self._parts:
            # Каждая часть гарантированно существует (PathNode создаётся только для валидных путей)
            node = node[part]
        # node может быть None (терминальный) или dict (промежуточный)
        return node if isinstance(node, dict) else {}

    def __getattr__(self, name: str) -> 'PathNode':
        # Отсекаем служебные атрибуты
        if name.startswith('_'):
            raise AttributeError(name)
        current = self._get_node()
        if name not in current:
            raise AttributeError(f"No event branch: {self.path}.{name}")
        return PathNode(self._parts + [name], self._schema)

    def __eq__(self, other) -> bool:
        if isinstance(other, PathNode):
            return self._parts == other._parts
        if isinstance(other, str):
            return self.path == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.path)

    def __repr__(self) -> str:
        return f"PathNode('{self.path}')"

    def __str__(self) -> str:
        return self.path

    def __contains__(self, other: Union[str, 'PathNode']) -> bool:
        """
        Проверить, что путь other зарегистрирован как событие
        и входит в поддерево текущего узла.
        """
        target = other.path if isinstance(other, PathNode) else other

        # Спускаемся по дереву схемы до текущего узла
        current_value = self._schema
        for part in self._parts:
            current_value = current_value[part]  # гарантированно существует

        # Терминальный узел (значение None) – содержит только сам себя
        if current_value is None:
            return target == self.path

        # Промежуточный узел (словарь) – рекурсивно собираем все терминальные пути
        events: set = set()

        def collect(node: dict, base: str) -> None:
            if node is None:
                events.add(base)
            elif isinstance(node, dict):
                for key, child in node.items():
                    path = f"{base}.{key}" if base else key
                    collect(child, path)

        collect(current_value, self.path)
        return target in events


# ======================================================================================================================
class PathTree:
    """
    Хранит иерархическую схему допустимых путей.
    Позволяет динамически расширять её через merge_schema().
    Доступ к событиям – через атрибуты, возвращающие PathNode.
    """
    def __init__(self, **schemas: Union[list[str | dict], set[str | dict], dict[str, str | set | dict | None]]):
        self._schema: dict[str, dict] = {}
        if schemas:
            self._merge(schemas)

    # ------------------------------------------------------------------
    # Вспомогательные методы
    # ------------------------------------------------------------------
    @staticmethod
    def _normalize(value: Union[Set[str], Dict]) -> dict | None:
        """Преобразует множество или вложенный словарь в унифицированное дерево."""
        if value is None:
            return None  # терминальное событие
        if isinstance(value, set):
            return {item: None for item in value}
        if isinstance(value, dict):
            return {k: PathTree._normalize(v) for k, v in value.items()}
        raise TypeError(f"Schema must be set or dict, got {type(value).__name__}")

    def _deep_merge(self, base: dict, new: dict) -> None:
        """Рекурсивно вливает new в base, модифицируя base на месте."""
        for key, new_val in new.items():
            if key not in base:
                base[key] = new_val
            else:
                old_val = base[key]
                # Если хотя бы один из операндов – словарь, результирующий узел обязан быть словарём
                if isinstance(new_val, dict) or isinstance(old_val, dict):
                    if not isinstance(old_val, dict):
                        base[key] = {}
                    if not isinstance(new_val, dict):
                        new_val = {}
                    self._deep_merge(base[key], new_val)
                # Иначе оба None – ничего не делаем

    def _merge(self, schemas: dict) -> None:
        """Применяет словарь {'ch1': {...}, ...} к текущей схеме."""
        for ch_name, raw_schema in schemas.items():
            norm = self._normalize(raw_schema)
            if ch_name not in self._schema:
                self._schema[ch_name] = norm
            else:
                self._deep_merge(self._schema[ch_name], norm)

    # ------------------------------------------------------------------
    # Публичный API
    # ------------------------------------------------------------------
    def merge_schema(self, **schemas: Union[Set[str], Dict]) -> None:
        """Расширяет текущую схему новыми каналами/событиями."""
        self._merge(schemas)

    def __getattr__(self, name: str) -> PathNode:
        # Стандартные атрибуты (методы) ищутся обычным механизмом, сюда попадают только отсутствующие
        if name.startswith('_'):
            raise AttributeError(name)
        if name in self._schema:
            return PathNode([name], self._schema)
        raise AttributeError(f"No root channel: {name}")


# ======================================================================================================================
def USAGE():
    tree = PathTree(
        ch1={"stderr", "stdin", "stdout"},
        ch2={"startup", "test", "teardown"},
    )

    node = tree.ch1.stdin
    assert node in tree.ch1  # True — событие в канале ch1
    assert tree.ch1.stdout in tree.ch1  # True
    assert "ch1.stderr" in tree.ch1  # True (строка тоже работает)
    assert "ch1.missing" not in tree.ch1  # такого события нет
    assert tree.ch2.test not in tree.ch1  # False — это другой канал

    node = tree.ch1.stdin
    assert node in node  # True
    assert "ch1.stdin" in node  # True
    assert "ch1.stdin.extra" not in node  # True


# =====================================================================================================================
if __name__ == "__main__":
    USAGE()


# =====================================================================================================================

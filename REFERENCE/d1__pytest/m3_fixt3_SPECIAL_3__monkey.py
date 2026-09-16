import pytest


# ======================================================================================================================
# 3. МАНКИ-ПАТЧИНГ (monkeypatch)
# =============================================================================
import os

def get_db_url():
    return os.environ.get("DATABASE_URL", "postgres://prod")

def test_monkeypatch_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    assert get_db_url() == "sqlite:///:memory:"

def test_monkeypatch_attr(monkeypatch):
    # Подмена атрибута класса или модуля
    import json
    fake_dumps = lambda obj, **kw: "mocked_json"
    monkeypatch.setattr(json, "dumps", fake_dumps)
    assert json.dumps({"a": 1}) == "mocked_json"

# -----------------------------------------------------------------------------
# Частая ошибка: забыть, что monkeypatch действует только в рамках теста.
# После выхода из тестовой функции оригинальное окружение восстанавливается.
# -----------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 5. monkeypatch — подмена атрибутов/окружения (function scope)
# ---------------------------------------------------------------------------
def test_env_var(monkeypatch):
    monkeypatch.setenv("APP_MODE", "test")
    assert os.environ["APP_MODE"] == "test"
    # Восстанавливается после выхода из теста.


# ======================================================================================================================

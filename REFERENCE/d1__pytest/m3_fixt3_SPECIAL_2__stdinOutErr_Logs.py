import pytest


# ======================================================================================================================
# 2. ПЕРЕХВАТ ВЫВОДА: stdout, stderr, логи (capsys, caplog)
# =============================================================================
def noisy_function():
    print("Важное сообщение в stdout")
    import logging
    logging.warning("Предупреждение в логах")

def test_capture_stdout_and_logs(capsys, caplog):
    noisy_function()
    captured = capsys.readouterr()
    assert "Важное сообщение" in captured.out

    # Проверка логов (caplog перехватывает логи уровня WARNING и выше по умолчанию)
    assert "Предупреждение" in caplog.text
    assert caplog.records[0].levelname == "WARNING"

# ---------------------------------------------------------------------------
# 3. capsys — захват stdout и stderr (function scope)
# ---------------------------------------------------------------------------
def test_print_something(capsys):
    print("важное сообщение")
    captured = capsys.readouterr()
    assert "важное" in captured.out
    # Нельзя в session-фикстурах: получите ошибку.

# ---------------------------------------------------------------------------
# 4. caplog — захват логов (function scope)
# ---------------------------------------------------------------------------
import logging

def test_log_output(caplog):
    logging.warning("test warning")
    assert "test warning" in caplog.text
    # caplog также function-scoped, не работает в session-фикстурах.


# ======================================================================================================================

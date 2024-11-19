from typing import *

class PROJECT:
    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "testplans"
    KEYWORDS: list[str] = [
        "testplan",
        "testplan structure framework",
        "testplan gui",
        "testplan multy dut",
        "testplan several dut",
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "simple testplan framework for several DUTs"
    DESCRIPTION_LONG: str = """
designed to apply testplan for several DUTs

## ПОНЯТИЯ
    TC - TestCase
    TP - TestPlan
    DUT - Device Under Test - тестируемое устройство

## АРХИТЕКТУРА
- тестплан
    - работает в потоке,
    - может быть остановлен в любой момент terminate(), при этом завершает все запущенные тесткейсы
    - имеет настройки которые принимаются всеми тесткейсами за базовые и могут быть перезаписаны ими для себя
    - имеет списки классов TC и обьектов DUT (генерирует обьекты TC для каждого DUT)
    - для себя не разделяет обьекты тесткейсов, работает строго с классом тесткейса,
    - выполняет все тесткейсы в порядке их следования на списке DUT
    - в один момент времени выполняется только один класс тесткейса
- тесткейсы
    - работают в потоке,
    - может быть остановлен в любой момент terminate(), при этом завершаются безопасно (исполняются все teardown обьектов и глобальный классовый тесткейса), 
    - представляет собой класс инициируемый с входным параметром DUT,
    - выполняются тесткейсы строго по очереди,
    - каждый тесткейс выполняется на всех устройствах либо асинхронно, либо синхронно в зависимости от настройки,
    - работа тесткейса полностью управляется классом тесткейса на серии устройств (возможно выполнение парных тестов с выбором нужных пар внутри тесткейса),
- результаты
    - все результаты находятся в пока в обьекте тесткейса
    - итогового (result)
    - промежуточных результатов (details)
- настройки
    - управление
        - SKIP всех возможных вариантов (полностью тесткейс для всех устройств, полностью DUT для всех TC, отдельный TC на отдельном DUT),
        - выполнение тесткейса синхронно/асинхронно
    - данные для использования в тесткейсах
        - реализовано в файлах JSON
        - для каждого тесткейса и общие для тестплана (кейсовые накладываются на плановые)
- GUI тестплана
    - запуск GUI опциональный,
    - старт/стоп тестплана,
    - отображение текущего тесткейса,
    - отображение результата тескейса на каждом тестируемом устройстве,
    - отображение промежуточных результатов (details)
- API 
    - минимальное API и запуск
"""

    FEATURES: list[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        ["[THREADS]",
            "safe work in independent TCs",
            "safe stop process at any moment by terminate",
         ],
        ["[SKIP]",
            "tc", "tc on dut", "dut"
         ],
        ["[DEVICES__BREEDER_INST]",
            "keep all in one instance",
            "use variants: single device for all duts or list for pairing each dut",
         ],
    ]

    # HISTORY -----------------------------------------------
    VERSION: tuple[int, int, int] = (0, 4, 34)
    TODO: list[str] = [
        "add meta for settings in tcs, it is better then applying in manually in TP!",
        "close all (api_server+tpThreads) on GUI close!",
        "add version for all jsons for future api_server",
        "[RESULTS] try separate",
    ]
    FIXME: list[str] = [
        "TP progress",
        "NEED TESTS!!! TC+TP"
    ]
    NEWS: list[str] = [
        "zero2",
    ]

# =====================================================================================================================

import asyncio
import pytest
from typing import *
from base_aux.aux_eq.m4_eq_valid3_derivatives import *


# ======================================================================================================================
class _TBase:
    PARALLEL: bool = True
    async def _execute_funcs__async(self, func_links: list[Awaitable]) -> list[Any | None | Exception]:
        """
        GOAL
        execute funcs
        eq_valid - if used, apply for values
        """
        # get values
        if self.PARALLEL:
            values = await asyncio.gather(*func_links, return_exceptions=True)
        else:
            values = []
            for func in func_links:
                try:
                    value = await func
                except Exception as exc:
                    value = exc
                values.append(value)

        # final
        return values

    def _validate_values(
            self,
            values: list[Any | None | Exception],
            eq_valid: Base_EqValid | Any,
    ) -> tuple[list[bool | None | Exception], bool]:
        result_final: bool = True
        results: list[bool | None | Exception] = []
        for value in values:
            if value is None:
                result = value
            elif isinstance(value, Exception):
                result = value
                result_final = False
            else:
                result = eq_valid == value
                if not result:
                    result_final = False

            results.append(result)

        return results, result_final


# ======================================================================================================================
class Test0_DevsDetected(_TBase):
    """
    GOAL
    just additionally show who detected
    """
    PARALLEL = True
    def test__1_dc_detected(self, dc):
        assert dc.detected

    def test__2_any_dut_detected(self, dut_list):
        for dut in dut_list:
            if dut.detected:
                return
        assert False


# ======================================================================================================================
class Test1_U(_TBase):
    PARALLEL = True
    @pytest.mark.asyncio
    async def test__1_u(self, dc, dut_list):
        TEST_U: float = 12

        # 0=prepare
        assert await dc.set_u(TEST_U)

        # 1=get links
        func_links = []
        for dut in dut_list:
            func_links.append(dut.mesure_u(TEST_U))

        # 2=get values
        values = await self._execute_funcs__async(func_links)

        # 3=validate
        results, result_final = self._validate_values(values, TEST_U)

        assert result_final, f"{results=} хотя бы один результат отрицателен"


# ======================================================================================================================
class Test2_I(_TBase):
    PARALLEL = False
    @pytest.mark.asyncio
    async def test__1_i(self, dc, dut_list):
        TEST_U: float = 12
        TEST_I: float = 0.5

        # 0=prepare
        assert await dc.set_u(TEST_U)

        results = []
        for dut in dut_list:
            result = dut.set_i(TEST_I)
            if not result:
                results.append(result)

            i = await dc.mesure_i()
            :
                TEST_I



        # 1=get links
        func_links = []
        for dut in dut_list:
            func_links.append()

        # 2=get values
        values = await self._execute_funcs__async(func_links)

        # 3=validate
        results, result_final = self._validate_values(values, TEST_I)

        assert result_final, f"{results=} хотя бы один результат отрицателен"


# ======================================================================================================================

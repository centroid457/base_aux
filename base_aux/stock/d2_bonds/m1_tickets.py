import os
import asyncio
import re
from t_tech.invest import AsyncClient
from t_tech.invest.schemas import InstrumentStatus

TOKEN = os.getenv("TTOKEN")


def is_ofz(ticker: str) -> bool:
    """Определение ОФЗ по тикеру."""
    if re.match(r'^SU\d{5}RMFS\d?$', ticker):
        return True
    if re.match(r'^SU(46|52)\d{3}RMFS\d?$', ticker):
        return True
    return False


async def get_ofz_bonds(token: str) -> dict[str, dict]:
    """
    Получение списка ОФЗ через Tinkoff API.

    Returns:
        dict: key=ticker, value={"name": str}

    Найдено ОФЗ: 87
  SU26242RMFS6: {'name': 'ОФЗ 26242'}
  SU26245RMFS9: {'name': 'ОФЗ 26245'}
  SU29023RMFS7: {'name': 'ОФЗ 29023'}
  SU26241RMFS8: {'name': 'ОФЗ 26241'}
  SU24020RMFS8: {'name': 'ОФЗ 24020'}
  SU46023RMFS6: {'name': 'ОФЗ 46023'}
  SU26239RMFS2: {'name': 'ОФЗ 26239'}
  SU26230RMFS1: {'name': 'ОФЗ 26230'}
  SU46012RMFS9: {'name': 'ОФЗ 46012'}
  SU29028RMFS6: {'name': 'ОФЗ 29028'}
  SU26231RMFS9: {'name': 'Облигации федерального займа с постоянным купонным доходом'}
  SU29021RMFS1: {'name': 'ОФЗ 29021'}
  SU29014RMFS6: {'name': 'ОФЗ 29014'}
  SU26238RMFS4: {'name': 'ОФЗ 26238'}
  SU29015RMFS3: {'name': 'ОФЗ 29015'}
  SU29011RMFS2: {'name': 'ОФЗ 29011'}
  SU29022RMFS9: {'name': 'ОФЗ 29022'}
  SU26247RMFS5: {'name': 'ОФЗ 26247'}
  SU29007RMFS0: {'name': 'ОФЗ 29007'}
  SU26246RMFS7: {'name': 'ОФЗ 26246'}
  SU26212RMFS9: {'name': 'ОФЗ 26212'}
  SU26243RMFS4: {'name': 'ОФЗ 26243'}
  SU29029RMFS4: {'name': 'ОФЗ 29029'}
  SU52003RMFS9: {'name': 'ОФЗ 52003'}
  SU29025RMFS2: {'name': 'ОФЗ 29025'}
  SU29010RMFS4: {'name': 'ОФЗ 29010'}
  SU29020RMFS3: {'name': 'ОФЗ 29020'}
  SU29031RMFS0: {'name': 'ОФЗ 29031'}
  SU26216RMFS0: {'name': 'ОФЗ 26216'}
  SU26252RMFS5: {'name': 'ОФЗ 26252'}
  SU25083RMFS5: {'name': 'ОФЗ 25083'}
  SU26236RMFS8: {'name': 'ОФЗ 26236'}
  SU29024RMFS5: {'name': 'ОФЗ 29024'}
  SU26221RMFS0: {'name': 'ОФЗ 26221'}
  SU26211RMFS1: {'name': 'ОФЗ 26211'}
  SU26237RMFS6: {'name': 'ОФЗ 26237'}
  SU26224RMFS4: {'name': 'ОФЗ 26224'}
  SU29017RMFS9: {'name': 'ОФЗ 29017'}
  SU26218RMFS6: {'name': 'ОФЗ 26218'}
  SU26228RMFS5: {'name': 'ОФЗ 26228'}
  SU29012RMFS0: {'name': 'ОФЗ 29012'}
  SU52004RMFS7: {'name': 'ОФЗ 52004'}
  SU26251RMFS7: {'name': 'ОФЗ 26251'}
  SU29013RMFS8: {'name': 'ОФЗ 29013'}
  SU26232RMFS7: {'name': 'ОФЗ 26232'}
  SU26253RMFS3: {'name': 'ОФЗ 26253'}
  SU29027RMFS8: {'name': 'ОФЗ 29027'}
  SU26244RMFS2: {'name': 'ОФЗ 26244'}
  SU26227RMFS7: {'name': 'ОФЗ 26227'}
  SU26225RMFS1: {'name': 'ОФЗ 26225'}
  SU26234RMFS3: {'name': 'ОФЗ 26234'}
  SU26214RMFS5: {'name': 'ОФЗ 26214'}
  SU29026RMFS0: {'name': 'ОФЗ 29026'}
  SU52002RMFS1: {'name': 'ОФЗ 52002'}
  SU26240RMFS0: {'name': 'ОФЗ 26240'}
  SU26217RMFS8: {'name': 'ОФЗ 26217'}
  SU26249RMFS1: {'name': 'ОФЗ 26249'}
  SU46020RMFS2: {'name': 'ОФЗ 46020'}
  SU26208RMFS7: {'name': 'ОФЗ 26208'}
  SU46022RMFS8: {'name': 'ОФЗ 46022'}
  SU29018RMFS7: {'name': 'ОФЗ 29018'}
  SU26248RMFS3: {'name': 'ОФЗ 26248'}
  SU26254RMFS1: {'name': 'ОФЗ 26254'}
  SU26205RMFS3: {'name': 'ОФЗ 26205'}
  SU26226RMFS9: {'name': 'ОФЗ 26226'}
  SU26235RMFS0: {'name': 'ОФЗ 26235'}
  SU26233RMFS5: {'name': 'ОФЗ 26233'}
  SU52005RMFS4: {'name': 'ОФЗ 52005'}
  SU29009RMFS6: {'name': 'ОФЗ 29009'}
  SU26220RMFS2: {'name': 'ОФЗ 26220'}
  SU29008RMFS8: {'name': 'ОФЗ 29008'}
  SU29016RMFS1: {'name': 'ОФЗ 29016'}
  SU26229RMFS3: {'name': 'ОФЗ 26229'}
  SU29019RMFS5: {'name': 'ОФЗ 29019'}
  SU26219RMFS4: {'name': 'ОФЗ 26219'}
  SU26223RMFS6: {'name': 'ОФЗ 26223'}
  SU26207RMFS9: {'name': 'ОФЗ 26207'}
  SU46011RMFS1: {'name': 'ОФЗ 46011'}
  SU24019RMFS0: {'name': 'ОФЗ 24019'}
  SU29006RMFS2: {'name': 'ОФЗ 29006'}
  SU26250RMFS9: {'name': 'ОФЗ 26250'}
  SU26215RMFS2: {'name': 'ОФЗ 26215'}
  SU26210RMFS3: {'name': 'ОФЗ 26210'}
  SU52001RMFS3: {'name': 'ОФЗ 52001'}
  SU26222RMFS8: {'name': 'ОФЗ 26222'}
  SU26209RMFS5: {'name': 'ОФЗ 26209'}
  SU25084RMFS3: {'name': 'ОФЗ 25084'}
    """
    async with AsyncClient(token) as client:
        response = await client.instruments.bonds(
            instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL
        )

        result: dict[str, dict] = {}
        for bond in response.instruments:
            if is_ofz(bond.ticker):
                result[bond.ticker] = {
                    "name": bond.name,
                }

        return result


async def main():
    ofz_list = await get_ofz_bonds(TOKEN)
    print(f"Найдено ОФЗ: {len(ofz_list)}")
    for ticker, data in ofz_list.items():
        print(f"  {ticker}: {data}")


if __name__ == "__main__":
    asyncio.run(main())


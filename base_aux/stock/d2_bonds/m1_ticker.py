import os
import asyncio
import re
from t_tech.invest import AsyncClient
from t_tech.invest.schemas import InstrumentStatus

from base_aux.base_types.m2_info import *


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
TICKETS_OFZ = {
	SU26242RMFS6: {'name': 'ОФЗ 26242'},
	SU26245RMFS9: {'name': 'ОФЗ 26245'},
	SU29023RMFS7: {'name': 'ОФЗ 29023'},
	SU26241RMFS8: {'name': 'ОФЗ 26241'},
	SU24020RMFS8: {'name': 'ОФЗ 24020'},
	SU46023RMFS6: {'name': 'ОФЗ 46023'},
	SU26239RMFS2: {'name': 'ОФЗ 26239'},
	SU26230RMFS1: {'name': 'ОФЗ 26230'},
	SU46012RMFS9: {'name': 'ОФЗ 46012'},
	SU29028RMFS6: {'name': 'ОФЗ 29028'},
	SU26231RMFS9: {'name': 'Облигации федерального займа с постоянным купонным доходом'},
	SU29021RMFS1: {'name': 'ОФЗ 29021'},
	SU29014RMFS6: {'name': 'ОФЗ 29014'},
	SU26238RMFS4: {'name': 'ОФЗ 26238'},
	SU29015RMFS3: {'name': 'ОФЗ 29015'},
	SU29011RMFS2: {'name': 'ОФЗ 29011'},
	SU29022RMFS9: {'name': 'ОФЗ 29022'},
	SU26247RMFS5: {'name': 'ОФЗ 26247'},
	SU29007RMFS0: {'name': 'ОФЗ 29007'},
	SU26246RMFS7: {'name': 'ОФЗ 26246'},
	SU26212RMFS9: {'name': 'ОФЗ 26212'},
	SU26243RMFS4: {'name': 'ОФЗ 26243'},
	SU29029RMFS4: {'name': 'ОФЗ 29029'},
	SU52003RMFS9: {'name': 'ОФЗ 52003'},
	SU29025RMFS2: {'name': 'ОФЗ 29025'},
	SU29010RMFS4: {'name': 'ОФЗ 29010'},
	SU29020RMFS3: {'name': 'ОФЗ 29020'},
	SU29031RMFS0: {'name': 'ОФЗ 29031'},
	SU26216RMFS0: {'name': 'ОФЗ 26216'},
	SU26252RMFS5: {'name': 'ОФЗ 26252'},
	SU25083RMFS5: {'name': 'ОФЗ 25083'},
	SU26236RMFS8: {'name': 'ОФЗ 26236'},
	SU29024RMFS5: {'name': 'ОФЗ 29024'},
	SU26221RMFS0: {'name': 'ОФЗ 26221'},
	SU26211RMFS1: {'name': 'ОФЗ 26211'},
	SU26237RMFS6: {'name': 'ОФЗ 26237'},
	SU26224RMFS4: {'name': 'ОФЗ 26224'},
	SU29017RMFS9: {'name': 'ОФЗ 29017'},
	SU26218RMFS6: {'name': 'ОФЗ 26218'},
	SU26228RMFS5: {'name': 'ОФЗ 26228'},
	SU29012RMFS0: {'name': 'ОФЗ 29012'},
	SU52004RMFS7: {'name': 'ОФЗ 52004'},
	SU26251RMFS7: {'name': 'ОФЗ 26251'},
	SU29013RMFS8: {'name': 'ОФЗ 29013'},
	SU26232RMFS7: {'name': 'ОФЗ 26232'},
	SU26253RMFS3: {'name': 'ОФЗ 26253'},
	SU29027RMFS8: {'name': 'ОФЗ 29027'},
	SU26244RMFS2: {'name': 'ОФЗ 26244'},
	SU26227RMFS7: {'name': 'ОФЗ 26227'},
	SU26225RMFS1: {'name': 'ОФЗ 26225'},
	SU26234RMFS3: {'name': 'ОФЗ 26234'},
	SU26214RMFS5: {'name': 'ОФЗ 26214'},
	SU29026RMFS0: {'name': 'ОФЗ 29026'},
	SU52002RMFS1: {'name': 'ОФЗ 52002'},
	SU26240RMFS0: {'name': 'ОФЗ 26240'},
	SU26217RMFS8: {'name': 'ОФЗ 26217'},
	SU26249RMFS1: {'name': 'ОФЗ 26249'},
	SU46020RMFS2: {'name': 'ОФЗ 46020'},
	SU26208RMFS7: {'name': 'ОФЗ 26208'},
	SU46022RMFS8: {'name': 'ОФЗ 46022'},
	SU29018RMFS7: {'name': 'ОФЗ 29018'},
	SU26248RMFS3: {'name': 'ОФЗ 26248'},
	SU26254RMFS1: {'name': 'ОФЗ 26254'},
	SU26205RMFS3: {'name': 'ОФЗ 26205'},
	SU26226RMFS9: {'name': 'ОФЗ 26226'},
	SU26235RMFS0: {'name': 'ОФЗ 26235'},
	SU26233RMFS5: {'name': 'ОФЗ 26233'},
	SU52005RMFS4: {'name': 'ОФЗ 52005'},
	SU29009RMFS6: {'name': 'ОФЗ 29009'},
	SU26220RMFS2: {'name': 'ОФЗ 26220'},
	SU29008RMFS8: {'name': 'ОФЗ 29008'},
	SU29016RMFS1: {'name': 'ОФЗ 29016'},
	SU26229RMFS3: {'name': 'ОФЗ 26229'},
	SU29019RMFS5: {'name': 'ОФЗ 29019'},
	SU26219RMFS4: {'name': 'ОФЗ 26219'},
	SU26223RMFS6: {'name': 'ОФЗ 26223'},
	SU26207RMFS9: {'name': 'ОФЗ 26207'},
	SU46011RMFS1: {'name': 'ОФЗ 46011'},
	SU24019RMFS0: {'name': 'ОФЗ 24019'},
	SU29006RMFS2: {'name': 'ОФЗ 29006'},
	SU26250RMFS9: {'name': 'ОФЗ 26250'},
	SU26215RMFS2: {'name': 'ОФЗ 26215'},
	SU26210RMFS3: {'name': 'ОФЗ 26210'},
	SU52001RMFS3: {'name': 'ОФЗ 52001'},
	SU26222RMFS8: {'name': 'ОФЗ 26222'},
	SU26209RMFS5: {'name': 'ОФЗ 26209'},
	SU25084RMFS3: {'name': 'ОФЗ 25084'},
}

TIKER
----------self.HIDE_NAMES__TOUCHED=None-------------------------------------------------------------
self.NAMES_COUNT__ON_START=88
   1:__annotations__
   2:__class__
   3:__dataclass_fields__
   4:__dataclass_params__
   5:__delattr__
   6:__dict__
   7:__dir__
   8:__doc__
   9:__eq__
  10:__format__
  11:__ge__
  12:__getattribute__
  13:__getstate__
  14:__gt__
  15:__hash__
  16:__init__
  17:__init_subclass__
  18:__le__
  19:__lt__
  20:__match_args__
  21:__module__
  22:__ne__
  23:__new__
  24:__reduce__
  25:__reduce_ex__
  26:__repr__
  27:__setattr__
  28:__sizeof__
  29:__str__
  30:__subclasshook__
  31:__weakref__
  32:aci_value
  33:amortization_flag
  34:api_trade_available_flag
  35:asset_uid
  36:blocked_tca_flag
  37:bond_type
  38:brand
  39:buy_available_flag
  40:call_date
  41:class_code
  42:country_of_risk
  43:country_of_risk_name
  44:coupon_quantity_per_year
  45:currency
  46:dlong
  47:dlong_client
  48:dlong_min
  49:dshort
  50:dshort_client
  51:dshort_min
  52:exchange
  53:figi
  54:first_1day_candle_date
  55:first_1min_candle_date
  56:floating_coupon_flag
  57:for_iis_flag
  58:for_qual_investor_flag
  59:initial_nominal
  60:isin
  61:issue_kind
  62:issue_size
  63:issue_size_plan
  64:klong
  65:kshort
  66:liquidity_flag
  67:lot
  68:maturity_date
  69:min_price_increment
  70:name
  71:nominal
  72:otc_flag
  73:perpetual_flag
  74:placement_date
  75:placement_price
  76:position_uid
  77:real_exchange
  78:required_tests
  79:risk_level
  80:sector
  81:sell_available_flag
  82:short_enabled_flag
  83:state_reg_date
  84:subordinated_flag
  85:ticker
  86:trading_status
  87:uid
  88:weekend_flag
self.NAMES_COUNT__ON_FINISH=88
[INFO]self.SOURCE_NAMES_COUNT_WAS_CHANGED=False//88/88
==========================================================================================
----------OBJECTINFO.PRINT--------------------------------------------------------------------------
str(SOURCE)=Bond(figi='TCS80A105RV3', ticker='SU26242RMFS6', class_code='PTOB', isin='RU000A105RV3', lot=1, currency='rub', klong=Quotation(units=0, nano=0), kshort=Quotation(units=0, nano=0), dlong=Quotation(units=0, nano=100000000), dshort=Quotation(units=0, nano=0), dlong_min=Quotation(units=0, nano=100000000), dshort_min=Quotation(units=0, nano=0), short_enabled_flag=False, name='ОФЗ 26242', exchange='unknown', coupon_quantity_per_year=2, maturity_date=datetime.datetime(2029, 8, 29, 0, 0, tzinfo=datetime.timezone.utc), nominal=MoneyValue(currency='rub', units=1000, nano=0), initial_nominal=MoneyValue(currency='rub', units=1000, nano=0), state_reg_date=datetime.datetime(2023, 1, 19, 0, 0, tzinfo=datetime.timezone.utc), placement_date=datetime.datetime(2023, 1, 25, 0, 0, tzinfo=datetime.timezone.utc), placement_price=MoneyValue(currency='', units=0, nano=0), aci_value=MoneyValue(currency='rub', units=12, nano=80000000), country_of_risk='RU', country_of_risk_name='Российская Федерация', sector='government', issue_kind='documentary', issue_size=479356615, issue_size_plan=500000000, trading_status=<SecurityTradingStatus.SECURITY_TRADING_STATUS_NORMAL_TRADING: 5>, otc_flag=False, buy_available_flag=False, sell_available_flag=True, floating_coupon_flag=False, perpetual_flag=False, amortization_flag=False, min_price_increment=Quotation(units=0, nano=100000), api_trade_available_flag=False, uid='dad5316e-70f6-4fb0-aca3-bcd085520a7b', real_exchange=<RealExchange.REAL_EXCHANGE_MOEX: 1>, position_uid='2548df0e-26ce-4efb-b338-e6ae285f718f', asset_uid='ba4fc385-127d-4704-8a3b-e1e92987318e', for_iis_flag=True, for_qual_investor_flag=False, weekend_flag=True, blocked_tca_flag=False, subordinated_flag=False, liquidity_flag=True, first_1min_candle_date=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), first_1day_candle_date=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), risk_level=<RiskLevel.RISK_LEVEL_LOW: 1>, brand=BrandData(logo_name='minfin.png', logo_base_color='#00A651', text_color='#ffffff'), bond_type=<BondType.BOND_TYPE_UNSPECIFIED: 0>, call_date=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), dlong_client=Quotation(units=0, nano=100000000), dshort_client=Quotation(units=0, nano=0), required_tests=[])
repr(SOURCE)=Bond(figi='TCS80A105RV3', ticker='SU26242RMFS6', class_code='PTOB', isin='RU000A105RV3', lot=1, currency='rub', klong=Quotation(units=0, nano=0), kshort=Quotation(units=0, nano=0), dlong=Quotation(units=0, nano=100000000), dshort=Quotation(units=0, nano=0), dlong_min=Quotation(units=0, nano=100000000), dshort_min=Quotation(units=0, nano=0), short_enabled_flag=False, name='ОФЗ 26242', exchange='unknown', coupon_quantity_per_year=2, maturity_date=datetime.datetime(2029, 8, 29, 0, 0, tzinfo=datetime.timezone.utc), nominal=MoneyValue(currency='rub', units=1000, nano=0), initial_nominal=MoneyValue(currency='rub', units=1000, nano=0), state_reg_date=datetime.datetime(2023, 1, 19, 0, 0, tzinfo=datetime.timezone.utc), placement_date=datetime.datetime(2023, 1, 25, 0, 0, tzinfo=datetime.timezone.utc), placement_price=MoneyValue(currency='', units=0, nano=0), aci_value=MoneyValue(currency='rub', units=12, nano=80000000), country_of_risk='RU', country_of_risk_name='Российская Федерация', sector='government', issue_kind='documentary', issue_size=479356615, issue_size_plan=500000000, trading_status=<SecurityTradingStatus.SECURITY_TRADING_STATUS_NORMAL_TRADING: 5>, otc_flag=False, buy_available_flag=False, sell_available_flag=True, floating_coupon_flag=False, perpetual_flag=False, amortization_flag=False, min_price_increment=Quotation(units=0, nano=100000), api_trade_available_flag=False, uid='dad5316e-70f6-4fb0-aca3-bcd085520a7b', real_exchange=<RealExchange.REAL_EXCHANGE_MOEX: 1>, position_uid='2548df0e-26ce-4efb-b338-e6ae285f718f', asset_uid='ba4fc385-127d-4704-8a3b-e1e92987318e', for_iis_flag=True, for_qual_investor_flag=False, weekend_flag=True, blocked_tca_flag=False, subordinated_flag=False, liquidity_flag=True, first_1min_candle_date=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), first_1day_candle_date=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), risk_level=<RiskLevel.RISK_LEVEL_LOW: 1>, brand=BrandData(logo_name='minfin.png', logo_base_color='#00A651', text_color='#ffffff'), bond_type=<BondType.BOND_TYPE_UNSPECIFIED: 0>, call_date=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), dlong_client=Quotation(units=0, nano=100000000), dshort_client=Quotation(units=0, nano=0), required_tests=[])
type(SOURCE)=<class 't_tech.invest.schemas.Bond'>
mro(SOURCE)=['Bond', 'Message', 'object']
----------SETTINGS----------------------------------------------------------------------------------
self.SKIP__BUILD_IN=True
self.NAMES__USE_ONLY_PARTS=[]
self.NAMES__SKIP_FULL=[]
self.NAMES__SKIP_PARTS=['init', 'new', 'create', 'enter', 'install', 'set', 'clone', 'copy', 'move', 'next', 'clear', 'reduce', 'close', 'del', 'exit', 'kill', 'abort', 'commit', 'checkout', 'attach', 'detach', 'connect', 'disconnect', 'exec', 'exec_', 'pyqtConfigure', 'run', 'start', 'wait', 'pause', 'continue', 'join', 'terminate', 'quit', 'stop', 'communicate', 'pop', 'popleft', 'put', 'input', 'extend', 'extendleft', 'append', 'appendleft', 'update', 'add', 'insert', 'reverse', 'rotate', 'sort', 'load', 'reload', 'dump', 'move', 'remove', 'rename', 'remove', 'resize', 'restart', 'reload', 'unpausebreakpointhook', 'hook']
self.MAX_LINE_LEN=100
self.MAX_ITER_ITEMS=5
----------SKIPPED_BUILDIN---------------------------------------------------------------------------
   1:__annotations__
   2:__class__
   3:__dataclass_fields__
   4:__dataclass_params__
   5:__delattr__
   6:__dict__
   7:__dir__
   8:__doc__
   9:__eq__
  10:__format__
  11:__ge__
  12:__getattribute__
  13:__getstate__
  14:__gt__
  15:__hash__
  16:__init__
  17:__init_subclass__
  18:__le__
  19:__lt__
  20:__match_args__
  21:__module__
  22:__ne__
  23:__new__
  24:__reduce__
  25:__reduce_ex__
  26:__repr__
  27:__setattr__
  28:__sizeof__
  29:__str__
  30:__subclasshook__
  31:__weakref__
----------SKIPPED_FULLNAMES-------------------------------------------------------------------------
----------SKIPPED_PARTNAMES-------------------------------------------------------------------------
   1:asset_uid
   2:initial_nominal
----------PROPERTIES__ELEMENTARY_SINGLE-------------------------------------------------------------
amortization_flag   	bool        :False
api_trade_available_flag	bool        :False
blocked_tca_flag    	bool        :False
bond_type           	BondType    :0
buy_available_flag  	bool        :False
class_code          	str         :PTOB
country_of_risk     	str         :RU
country_of_risk_name	str         :Российская Федерация
coupon_quantity_per_year	int         :2
currency            	str         :rub
exchange            	str         :unknown
figi                	str         :TCS80A105RV3
floating_coupon_flag	bool        :False
for_iis_flag        	bool        :True
for_qual_investor_flag	bool        :False
isin                	str         :RU000A105RV3
issue_kind          	str         :documentary
issue_size          	int         :479356615
issue_size_plan     	int         :500000000
liquidity_flag      	bool        :True
lot                 	int         :1
name                	str         :ОФЗ 26242
otc_flag            	bool        :False
perpetual_flag      	bool        :False
position_uid        	str         :2548df0e-26ce-4efb-b338-e6ae285f718f
real_exchange       	RealExchange:1
risk_level          	RiskLevel   :1
sector              	str         :government
sell_available_flag 	bool        :True
short_enabled_flag  	bool        :False
subordinated_flag   	bool        :False
ticker              	str         :SU26242RMFS6
trading_status      	SecurityTradingStatus:5
uid                 	str         :dad5316e-70f6-4fb0-aca3-bcd085520a7b
weekend_flag        	bool        :True
----------PROPERTIES__ELEMENTARY_COLLECTION---------------------------------------------------------
----------PROPERTIES__OBJECTS-----------------------------------------------------------------------
aci_value           	MoneyValue  :MoneyValue(currency='rub', units=12, nano=80000000)
brand               	BrandData   :BrandData(logo_name='minfin.png', logo_base_color='#00A651',...
call_date           	datetime    :1970-01-01 00:00:00+00:00
dlong               	Quotation   :Quotation(units=0, nano=100000000)
dlong_client        	Quotation   :Quotation(units=0, nano=100000000)
dlong_min           	Quotation   :Quotation(units=0, nano=100000000)
dshort              	Quotation   :Quotation(units=0, nano=0)
dshort_client       	Quotation   :Quotation(units=0, nano=0)
dshort_min          	Quotation   :Quotation(units=0, nano=0)
first_1day_candle_date	datetime    :1970-01-01 00:00:00+00:00
first_1min_candle_date	datetime    :1970-01-01 00:00:00+00:00
klong               	Quotation   :Quotation(units=0, nano=0)
kshort              	Quotation   :Quotation(units=0, nano=0)
maturity_date       	datetime    :2029-08-29 00:00:00+00:00
min_price_increment 	Quotation   :Quotation(units=0, nano=100000)
nominal             	MoneyValue  :MoneyValue(currency='rub', units=1000, nano=0)
placement_date      	datetime    :2023-01-25 00:00:00+00:00
placement_price     	MoneyValue  :MoneyValue(currency='', units=0, nano=0)
required_tests      	RepeatedScalarContainer:[]
state_reg_date      	datetime    :2023-01-19 00:00:00+00:00
----------PROPERTIES__EXC---------------------------------------------------------------------------
----------METHODS__ELEMENTARY_SINGLE----------------------------------------------------------------
----------METHODS__ELEMENTARY_COLLECTION------------------------------------------------------------
----------METHODS__OBJECTS--------------------------------------------------------------------------
----------METHODS__EXC------------------------------------------------------------------------------
==========================================================================================
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

        ObjectInfo(bond).print()
        return result


async def main():
    ofz = await get_ofz_bonds(TOKEN)
    print(f"Найдено ОФЗ: {len(ofz)}")
    print("TICKETS_OFZ = {")
    for ticker, data in ofz.items():
        print(f"\t{ticker}: {data},")
    print("}")


if __name__ == "__main__":
    asyncio.run(main())


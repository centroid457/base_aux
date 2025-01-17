from typing import *
from .m2_url_tag import *


# =====================================================================================================================
class Monitor_DonorSvetofor(MonitorUrlTag):
    """
    MONITOR donor svetofor and alert when BloodCenter need your blood group!

    # STRUCTURE to find -------------------------------------
<table class="donor-svetofor-restyle">
    <tbody>
        <tr>
            <th colspan="2">O (I)</th>
            <th colspan="2">A (II)</th>
            <th colspan="2">B (III)</th>
            <th colspan="2">AB (IV)</th>
        </tr>
        <tr>
            <td class="green">Rh +</td>
            <td class="green">Rh –</td>
            <td class="green">Rh +</td>
            <td class="yellow">Rh –</td>
            <td class="green">Rh +</td>
            <td class="yellow">Rh –</td>
            <td class="red">Rh +</td>
            <td class="red">Rh –</td>
        </tr>
    </tbody>
</table>
    """
    # KEEP FIRST!
    DONOR_BLOOD_GROUP: int = 3
    DONOR_BLOOD_RH: str = "+"

    # MAIN -------------------------------
    URL = "https://donor.mos.ru/donoru/donorskij-svetofor/"
    TAG_CHAINS = [
        TagAddressChain("table", {"class": "donor-svetofor-restyle"}, None, 0),
        TagAddressChain("td", {}, f"Rh {DONOR_BLOOD_RH}", DONOR_BLOOD_GROUP - 1),
    ]
    TAG_GET_ATTR = "class"


# =====================================================================================================================
class Monitor_CbrKeyRate(MonitorUrlTag):
    """
    MONITOR CentralBankRussia KeyRate

    # STRUCTURE to find -------------------------------------
<div class="table-wrapper">
  <div class="table-caption gray">% годовых</div>
  <div class="table">
    <table class="data">
      <tr>
        <th>Дата</th>
        <th>Ставка</th>
      </tr>
      <tr>
        <td>17.08.2023</td>
        <td>12,00</td>
      </tr>
      <tr>
        <td>16.08.2023</td>
        <td>12,00</td>
      </tr>
      <tr>
        <td>15.08.2023</td>
        <td>12,00</td>
      </tr>
      <tr>
        <td>14.08.2023</td>
        <td>8,50</td>
      </tr>
      <tr>
        <td>11.08.2023</td>
        <td>8,50</td>
      </tr>
      <tr>
        <td>10.08.2023</td>
        <td>8,50</td>
      </tr>
    </table>
  </div>
  <div class="table-caption">
    <p>
	  Данные доступны с  17.09.2013 по 17.08.2023.
	  </p>
  </div>
</div>
    """
    # OVERWRITING NEXT -------------------------------
    # KEEP FIRST!

    # OVERWRITTEN NOW -------------------------------
    URL = "https://cbr.ru/hd_base/KeyRate/"
    TAG_CHAINS = [
        TagAddressChain("div", {"class": "table-wrapper"}, None, 0),
        TagAddressChain("td", {}, None, 1),
    ]
    TAG_GET_ATTR = None


# =====================================================================================================================
class Monitor_ConquestS23_comments(MonitorUrlTag):
    """
    # STRUCTURE to find -------------------------------------
<div class="table-wrapper">
  <div class="table-caption gray">% годовых</div>
  <div class="table">
    <table class="data">
      <tr>
        <th>Дата</th>
        <th>Ставка</th>
      </tr>
      <tr>
        <td>17.08.2023</td>
        <td>12,00</td>
      </tr>
      <tr>
        <td>16.08.2023</td>
        <td>12,00</td>
      </tr>
      <tr>
        <td>15.08.2023</td>
        <td>12,00</td>
      </tr>
      <tr>
        <td>14.08.2023</td>
        <td>8,50</td>
      </tr>
      <tr>
        <td>11.08.2023</td>
        <td>8,50</td>
      </tr>
      <tr>
        <td>10.08.2023</td>
        <td>8,50</td>
      </tr>
    </table>
  </div>
  <div class="table-caption">
    <p>
	  Данные доступны с  17.09.2013 по 17.08.2023.
	  </p>
  </div>
</div>
    """
    # OVERWRITING NEXT -------------------------------
    # KEEP FIRST!

    # OVERWRITTEN NOW -------------------------------
    URL = "https://exgad.ru/products/conquest-s23"
    TAG_CHAINS = [
        TagAddressChain("div", {"class": "comments-tab__quatity"}, None, 0),
    ]
    TAG_GET_ATTR = None


# =====================================================================================================================
class Monitor_Sportmaster_AdidasSupernova2M(MonitorUrlTag):
    """
    # STRUCTURE to find -------------------------------------
    <span data-selenium="amount" class="sm-amount__value">13 699 ₽</span>
    """
    # TODO: need resolve StatusCode401
    # OVERWRITING NEXT -------------------------------
    # KEEP FIRST!

    # OVERWRITTEN NOW -------------------------------
    URL = "https://www.sportmaster.ru/product/29647730299/"
    TAG_CHAINS = [
        TagAddressChain("span", {"class": "sm-amount__value"}, None, 0),
    ]
    TAG_GET_ATTR = None


# =====================================================================================================================
class Monitor_AcraRaiting_GTLC(MonitorUrlTag):
    """
    NOT WORKING!
[Try send --------------------------------------------------------------------------------
[ALERT]Monitor_AcraRaiting_GTLC
LOST URL SSLError(MaxRetryError("HTTPSConnectionPool(host='www.acra-ratings.ru', port=443): Max retries exceeded with url: /ratings/issuers/50/ (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1002)')))"))[CRITICAL] empty self._source_data=''
2023.09.18 21:02:54
Try send] --------------------------------------------------------------------------------
[READY] send


    # STRUCTURE to find -------------------------------------
<div class="current-emit__actual-table">
    <div class="inner-table green" data-type="ratings">
        <div class="rating-head">
            <div class="item-info" data-type="scale">Шкала</div>
            <div class="item-info" data-type="rate">Рейтинг</div>
            <div class="item-info" data-type="pressRelease">Пресс-релиз</div>
        </div>
        <div class="rating-list">
            <div class="rating-item">
                <div class="item-info dedicated" data-type="scale">Национальная рейтинговая шкала</div>
                <div class="item-info dedicated" data-type="rate">
                    <div class="rating-widget" >
                        <div class="tooltip-ctrl" title="На пересмотре">
                            <svg class="svg status-icon">
                                <use xlink:href="/static/img/icons/symbol/sprite.svg#under-control"></use>
                            </svg>
                        </div>
                        AA-(RU)     На пересмотре (развивающийся)
                    </div>
                </div>
                <a
                    class="item-info dedicated 123123"
                    href="/press-releases/3966/"
                    data-type="pressRelease"
                >
                    18 май 2023
                    <img class="svg" src="/static/img/icons/search/link.svg">
                </a>
            </div>
        </div>
    </div>
    """
    TIMEOUT_REQUEST = 30
    URL = "https://www.acra-ratings.ru/ratings/issuers/50/"
    TAG_CHAINS = [
        TagAddressChain("div", {"class": "current-emit__actual-table"}, None, 0),
        TagAddressChain("div", {"class": "rating-list"}, None, 0),
        TagAddressChain("div", {"class": "rating-item"}, None, 0),
        TagAddressChain("div", {"class": "rating-widget"}, None, 0),
    ]
    TAG_GET_ATTR = None


# =====================================================================================================================


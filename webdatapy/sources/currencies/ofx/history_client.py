from webdatapy.sources.currencies.currency import CurrencyCode
from webdatapy.helpers import enum
import httplib
import json
import datetime
import pytz

OfxPeriod = enum(
    SEVEN_DAYS="week",
    ONE_MONTH="month",
    THREE_MONTHS="3month",
    SIX_MONTHS="6month",
    ONE_YEAR="year",
    THREE_YEARS="3year",
    FIVE_YEARS="5year",
    TEN_YEARS="10year",
    ALL="allTime"
)

OfxFrequency = enum(
    DAILY="daily",
    MONTHLY="monthly",
    YEARLY="yearly"
)


def get_prices(currency, in_currency, period=OfxPeriod.SEVEN_DAYS, frequency=OfxFrequency.DAILY):
    """
    Fetch prices of currency in in_currency
    :param currency : CurrencyCode Currency to check
    :param in_currency : CurrencyCode Currency in which price is calculated
    :param frequency: OfxFrequency Frequency of pricing check
    :param period: OfxPeriod Period of prices
    :return: dict
    """
    c_out = CurrencyCode.from_string[currency]
    c_in = CurrencyCode.from_string[in_currency]

    if c_out == c_in:
        raise ValueError("Currency and in currency have to be different")

    headers = {"Accept": "application/json"}

    url = "/PublicSite.ApiService/SpotRateHistory/%s/%s/%s?DecimalPlaces=6&ReportingInterval=%s" % (
        period, c_out, c_in, frequency)

    conn = httplib.HTTPSConnection("api.ofx.com")
    conn.request(method="GET", url=url, headers=headers)

    resp = conn.getresponse()

    if resp.status != 200:
        raise RuntimeError("Ofx server response error: %s %s" % (resp.status, resp.reason))

    data = resp.read()
    j = json.loads(data)

    result = []

    for historical_point in j['HistoricalPoints']:
        point_in_time = historical_point['PointInTime']
        interbank_rate = historical_point['InterbankRate']

        date = datetime.datetime.fromtimestamp(point_in_time / 1000, pytz.timezone('GMT')).strftime(
            '%Y-%m-%d %H:%M:%S%z')
        rate = "{0:f}".format(interbank_rate)

        result.append({"time": date, "rate": rate, "currency": c_out, "in": c_in})

    return result

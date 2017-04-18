import nose
from webdatapy.sources.currencies.currency import CurrencyCode
from webdatapy.sources.currencies.ofx.history_client import OfxPeriod
from webdatapy.sources.currencies.ofx.history_client import OfxFrequency
from webdatapy.sources.currencies.ofx import history_client as client
import datetime


def test_fetching_last_six_days_of_usd_in_eur():
    result = client.get_prices(CurrencyCode.USD, CurrencyCode.EUR)
    assert len(result) == 6

    ndt = datetime.datetime.now()

    for c in result:
        assert c['currency'] == 'USD'
        assert c['in'] == 'EUR'
        assert float(c['rate']) > 0
        assert c['time'] is not None

        dt = datetime.datetime.strptime(c['time'], '%Y-%m-%d %H:%M:%S+0000')

        assert ndt.year - dt.year <= 1
        assert ndt.month - dt.month <= 1
        assert ndt.day - dt.day <= 6


def test_fetching_last_year_monthly_of_jpy_in_eur():
    result = client.get_prices(CurrencyCode.JPY, CurrencyCode.EUR, OfxPeriod.ONE_YEAR, OfxFrequency.MONTHLY)
    assert len(result) == 12

    ndt = datetime.datetime.now()

    for c in result:
        assert c['currency'] == 'JPY'
        assert c['in'] == 'EUR'
        assert float(c['rate']) > 0
        assert c['time'] is not None

        dt = datetime.datetime.strptime(c['time'], '%Y-%m-%d %H:%M:%S+0000')

        assert ndt.year - dt.year <= 1
        assert ndt.month - dt.month <= 12


argv = [__file__, '-v', '--nocapture']
nose.main(argv=argv)

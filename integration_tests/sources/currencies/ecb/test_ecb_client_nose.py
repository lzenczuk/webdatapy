import nose
from webdatapy.sources.currencies.ecb import client
import datetime


def test_fetching_current_prices():
    result = client.get_prices()
    assert len(result) > 30

    ndt = datetime.datetime.now()

    for c in result:
        assert c['currency'] == 'EUR'
        assert len(c['in']) == 3
        assert float(c['rate']) > 0
        assert c['time'] is not None

        dt = datetime.datetime.strptime(c['time'], '%Y-%m-%d %H:%M:%S+0000')

        assert ndt.year - dt.year <= 1
        assert ndt.month - dt.month <= 1
        assert ndt.day - dt.day <= 1


argv = [__file__, '-v', '--nocapture']
nose.main(argv=argv)

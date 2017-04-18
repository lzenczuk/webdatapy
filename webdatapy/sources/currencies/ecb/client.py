from webdatapy.sources.currencies.currency import CurrencyCode
import httplib
import xml.etree.cElementTree as ET
import datetime
import pytz


def get_prices():
    url = "/stats/eurofxref/eurofxref-daily.xml"

    conn = httplib.HTTPConnection("www.ecb.europa.eu")
    conn.request(method="GET", url=url)

    resp = conn.getresponse()

    if resp.status != 200:
        raise RuntimeError("Ofx server response error: %s %s" % (resp.status, resp.reason))

    data = resp.read()

    root = ET.fromstring(data)

    xml_date = root.findall("./{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube/{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube")[0].get('time')
    rates = root.findall("./{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube/{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube//{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube")

    year = int(xml_date.split("-")[0])
    month = int(xml_date.split("-")[1])
    day = int(xml_date.split("-")[2])

    date = datetime.datetime(year, month, day, tzinfo=pytz.timezone('GMT')).strftime('%Y-%m-%d %H:%M:%S%z')
    c_out = CurrencyCode.from_string['EUR']

    result = []

    for rate in rates:
        r = rate.get('rate')
        c = rate.get('currency')
        c_in = CurrencyCode.from_string[c]

        result.append({"time": date, "rate": r, "currency": c_out, "in": c_in})

    return result


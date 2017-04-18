import httplib


def fetch_page_by_id(page_id):
    print("Getting real url for page "+str(page_id))
    real_url = _get_real_url(page_id)

    if real_url is None:
        print("Real url not found")
        return {"id": page_id, "status": "NOT_FOUND"}

    print("Real url: "+real_url)
    path = real_url.replace("http://www.wykop.pl", "", 1)

    print("Fetching page using path: "+path)
    result = _fetch_page(path)

    result['url'] = real_url
    result['id'] = page_id

    print("Result status: "+result['status'])

    return result


def _get_real_url(page_id):
    path = "/link/" + str(page_id) + "/"
    conn = httplib.HTTPConnection("www.wykop.pl")
    conn.request(method="GET", url=path)

    resp = conn.getresponse()

    if (resp.status > 299) & (resp.status < 400):
        return resp.getheader("Location")

    return None


def _fetch_page(path):
    conn = httplib.HTTPSConnection("www.wykop.pl")
    conn.request(method="GET", url=path)

    resp = conn.getresponse()

    if resp.status == 200:
        content = resp.read()
        return {"content": content, "status": "OK"}

    if resp.status == 404:
        return {"status": "NOT_FOUND"}

    return {"status": "UNKNOWN"}


def fetch_up_votes_by_id(page_id):
    path = "/ajax2/links/Upvoters/" + str(page_id) + "/"

    print("Fetching up votes using path: "+path)

    return _fetch_votes(path)


def fetch_down_votes_by_id(page_id):
    path = "/ajax2/links/downvoters/" + str(page_id) + "/"

    print("Fetching down votes using path: "+path)

    return _fetch_votes(path)


def _fetch_votes(path):
    conn = httplib.HTTPConnection("www.wykop.pl")
    conn.request(method="GET", url=path)
    resp = conn.getresponse()
    if resp.status == 200:
        content = resp.read()
        print("Result status: OK")
        return {"content": content, "status": "OK"}
    if resp.status == 404:
        print("Result status: NOT FOUND")
        return {"status": "NOT_FOUND"}
    print("Result status: UNKNOWN")
    return {"status": "UNKNOWN"}


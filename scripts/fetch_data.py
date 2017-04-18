from webdatapy.sources.wykop.client import fetch_page_by_id
from webdatapy.sources.wykop.client import fetch_up_votes_by_id
from webdatapy.sources.wykop.client import fetch_down_votes_by_id
from webdatapy.sources.wykop.page import WykopPage

import json

p_id = 23456

result = fetch_page_by_id(p_id)

if result['status'] == "OK":
    up_result = fetch_up_votes_by_id(p_id)

    down_result = fetch_down_votes_by_id(p_id)

    page = WykopPage(result['content'], up_result['content'], down_result['content'])

    print(json.dumps(page.to_dict()))

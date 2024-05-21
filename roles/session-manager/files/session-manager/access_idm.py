import os
import requests


def get_swczone(name: str):
    get_swczone_url = os.environ.get("GET_SWCZONE_URL")
    url = get_swczone_url + "/" + name
    headers = {"HTTP_SYSTEMACCOUNT": "SESSION_MANAGER"}

    response = requests.get(url, headers=headers)
    return response.json()

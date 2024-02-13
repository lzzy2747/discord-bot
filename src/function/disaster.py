from os import getenv

from dotenv import load_dotenv

from function.https import get_request

load_dotenv(dotenv_path="../.env")

URL: str = "http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List"
params: dict = {
    "serviceKey": getenv("SERVICE_URL"),
    "pageNo": "1",
    "numOfRows": "1",
    "type": "json",
}


def disaster_content():
    data = get_request(
        url=URL,
        params=params,
    )

    return data["DisasterMsg"][1]["row"][0]["msg"]


def disaster_date():
    data = get_request(
        url=URL,
        params=params,
    )

    return data["DisasterMsg"][1]["row"][0]["create_date"]

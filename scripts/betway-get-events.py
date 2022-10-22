from time import sleep
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import json, jsonpickle

URL = "https://betway.com/en/sports/mkt/10241559/265630937"
API_URL = "https://betway.com/api/Events/v2/GetEventDetails"
QUERY_GAP_SECONDS = 5

class Market: 
    def __init__(self, id, name, outcome_ids):
        self.id = id 
        self.name = name
        self.outcome_ids = outcome_ids


class Outcome:
    def __init__(self, id, bet_name, odds):
        self.id = id
        self.bet_name = bet_name
        self.odds = odds 


def parseEventDetails(bodyString):
    body = json.loads(bodyString)
    for market in body['Markets']:
        if market['Title'] == 'Match Winner':
            market_obj = Market(
                market['Id'],
                "{} - {} vs {}".format(
                    market['Title'], market['Headers'][0], market['Headers'][1]
                ),
                market['Outcomes'][0]
            )
            for outcome in body['Outcomes']:
                if outcome['Id'] in market['Outcomes'][0]:
                    outcome_obj = Outcome(
                        outcome['Id'],
                        outcome['BetName'],
                        outcome['OddsDecimal']
                    )
                    serialized = jsonpickle.encode(outcome_obj)
                    print(json.dumps(json.loads(serialized), indent=2))

            serialized = jsonpickle.encode(market_obj)
            print(json.dumps(json.loads(serialized), indent=2))


def openBrowser(url, api_url, parse_func):
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {
        "performance": "ALL",
        "browser": "ALL"
    }

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        desired_capabilities=desired_capabilities
    )

    driver.get(url)

    while True:
        sleep(QUERY_GAP_SECONDS)

        logs_raw = driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

        def log_filter(log_):
            return (
                log_["method"] == "Network.responseReceived"
                and "json" in log_["params"]["response"]["mimeType"]
            )

        for log in filter(log_filter, logs):
            request_id = log["params"]["requestId"]
            resp_url = log["params"]["response"]["url"]
            if resp_url == api_url:
                body = driver.execute_cdp_cmd(
                    "Network.getResponseBody", {
                        "requestId": request_id
                    }
                )['body']
                parse_func(body)


if __name__ == "__main__":
    openBrowser(URL, API_URL, parseEventDetails)

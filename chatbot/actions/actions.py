# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from bs4 import BeautifulSoup
import requests

import json
import ssl
from urllib.request import urlopen


class ActionCovidNews(Action):

    def name(self) -> Text:
        return "action_covid_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        main_url = "https://newsapi.org/v2/top-headlines?q=covid&country=in&category=health&apiKey=b35e395df2ea4a5e86f4f68e6f1f6ac0"

        res = requests.get(main_url)
        open_page = res.json()

        articles = open_page["articles"]

        text = ""

        for article in articles:
            text += "{0}\n".format(article["title"])
            text += "{0}\n".format(article['description'])
            text += "{0}\n".format("- By {0}".format(article["author"]))
            text += "{0}\n".format("Refer to the full article here: {0}".format(article['url']))
            dispatcher.utter_message(text=text)
            text = ""

        return []


class ActionCovidData(Action):

    def name(self) -> Text:
        return "action_covid_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_place = next(tracker.get_latest_entity_values("place"), None)

        url = "https://data.covid19india.org/v4/min/data.min.json"
        ssl_context = ssl._create_unverified_context()
        reponse = urlopen(url, context=ssl_context)
        data = json.loads(reponse.read())

        text = ""

        if current_place is not None:
            for state, cases in data.items():
                if state == current_place:
                    text += ("Cases in {0}: \n").format(state)
                    if "confirmed" in cases["delta7"].keys():
                        text += "Confirmed Cases for last 7 days: "
                        text += (str(cases["delta7"]["confirmed"]) + "\n")
                    if "deceased" in cases["delta7"].keys():
                        text += "Deceased for last 7 days:"
                        text += (str(cases["delta7"]["deceased"]) + "\n")
                    if "recovered" in cases["delta7"].keys():
                        text += ("Recovered for last 7 days:")
                        text += (str(cases["delta7"]["recovered"]) + "\n")
                    if "tested" in cases["delta7"].keys():
                        text += ("Tested for last 7 days:")
                        text += (str(cases["delta7"]["tested"]) + "\n")
                    if "vaccinated1" in cases["delta7"].keys():
                        text += ("Vaccinated with one dose for last 7 days:")
                        text += (str(cases["delta7"]["vaccinated1"]) + "\n")
                    if "vaccinated2" in cases["delta7"].keys():
                        text += ("Vaccinated with two doses for last 7 days:")
                        text += (str(cases["delta7"]["vaccinated2"]) + "\n")

                    dispatcher.utter_message(text=text)
                    return []

                else:
                    pass

        else:
            #dispatcher.utter_message(text="Invalid state code! Please enter a valid state code")
            dispatcher.utter_message(text=current_place)
            return []

        return []

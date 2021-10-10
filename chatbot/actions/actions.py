# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests

import json
import ssl
from urllib.request import urlopen


class ActionCovidCenters(Action):

    def name(self) -> Text:
        return "action_covid_centers"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pincode = next(tracker.get_latest_entity_values("pincode"), None)

        url = "https://api.mygov.in/get-vaccination-center/?api_key=57076294a5e2ab7fe0000001dd278c47e313412c7de416e536f1992f&pincode=" + pincode

        ssl_context = ssl._create_unverified_context()
        response = urlopen(url, context=ssl_context)

        data = json.loads(response.read())

        text = ""

        for center, details in data.items():
            if center == "center_data":
                for data in details:
                    text += "Center ID: {0}<br />".format(data["center_id"])
                    text += "Name of center: {0}<br />".format(data["name"])
                    text += "Address: {0}<br />".format(data["address"])
                    text += "Minimum age limit: {0}<br />".format(data["min_age_limit"])
                    text += "Next available day: {0}<br />".format(data["next_available_day"])
                    text += "Available capacity: {0}<br />".format(data["available_capacity"])
                    text += "Available dose 1 capacity: {0}<br />".format(data["available_capacity_dose1"])
                    text += "Available dose 2 capacity: {0}<br />".format(data["available_capacity_dose2"])
                    text += "Vaccine name: {0}<br />".format(data["vaccine_name"])
                    text += "Directions: https://www.google.com/maps/search/{0}<br />".format(str(data["name"]).replace(" ", "+"))

                    dispatcher.utter_message(text=text)
                    text = ""
            # else:
            #     dispatcher.utter_message(text="Could not retrieve data")
            #     return []

        return []


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
        i = 0

        for article in articles:
            text += "{0}<br />".format(article["title"])
            text += "{0}<br />".format(article['description'])
            text += "{0}<br />".format("- By {0}".format(article["author"]))
            text += "{0}<br />".format("Refer to the full article here: {0}".format(article['url']))

            dispatcher.utter_message(text=text)

            text = ""
            i+=1

            if i == 3:
                return []

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
                    text += "Cases in {0}: <br />".format(state)
                    if "confirmed" in cases["delta7"].keys():
                        text += "Confirmed Cases for last 7 days: "
                        text += (str(cases["delta7"]["confirmed"]) + "<br />")
                    if "deceased" in cases["delta7"].keys():
                        text += "Deceased for last 7 days: "
                        text += (str(cases["delta7"]["deceased"]) + "<br />")
                    if "recovered" in cases["delta7"].keys():
                        text += "Recovered for last 7 days: "
                        text += (str(cases["delta7"]["recovered"]) + "<br />")
                    if "tested" in cases["delta7"].keys():
                        text += "Tested for last 7 days: "
                        text += (str(cases["delta7"]["tested"]) + "<br />")
                    if "vaccinated1" in cases["delta7"].keys():
                        text += "Vaccinated with one dose for last 7 days: "
                        text += (str(cases["delta7"]["vaccinated1"]) + "<br />")
                    if "vaccinated2" in cases["delta7"].keys():
                        text += "Vaccinated with two doses for last 7 days: "
                        text += (str(cases["delta7"]["vaccinated2"]) + "<br />")

                    dispatcher.utter_message(text=text)
                    return []

                else:
                    pass

        else:
            dispatcher.utter_message(text="Invalid state code! Please enter a valid state code")
            return []

        return []

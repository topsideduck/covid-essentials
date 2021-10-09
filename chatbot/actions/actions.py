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

import newspaper


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")

        return []


class ActionShowMasks(Action):

    def name(self) -> Text:
        return "action_show_masks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        def get_title(soup):
            try:
                title = soup.find("span", attrs={"id": 'productTitle'})
                title_value = title.string
                title_string = title_value.strip()

            except AttributeError:
                title_string = ""

            return title_string

        def get_price(soup):
            try:
                price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip()

            except AttributeError:
                try:
                    # If there is some deal price
                    price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip()

                except:
                    price = ""

            return price

        def get_rating(soup):
            try:
                rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()

            except AttributeError:
                try:
                    rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
                except:
                    rating = ""

            return rating

        def get_review_count(soup):
            try:
                review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()

            except AttributeError:
                review_count = ""

            return review_count

        def get_availability(soup):
            try:
                available = soup.find("div", attrs={'id': 'availability'})
                available = available.find("span").string.strip()

            except AttributeError:
                available = "Not Available"

            return available

        HEADERS = ({'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                    'Accept-Language': 'en-US'})

        URL = "https://www.amazon.com/s?k=face+mask&ref=nb_sb_noss_2"
        webpage = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "lxml")
        links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
        links_list = []

        for link in links:
            links_list.append(link.get('href'))

        for link in links_list:
            new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

            new_soup = BeautifulSoup(new_webpage.content, "lxml")

            text = "Product Title: {0}\nProduct Price: {1}\nProduct Rating: {2}\nNumber of Product Reviews: {3}\n Buy At: {4}".format(
                get_title(new_soup), get_price(new_soup), get_rating(new_soup), get_review_count(new_soup), link)

            # print("Product Title =", get_title(new_soup))
            # print("Product Price =", get_price(new_soup))
            # print("Product Rating =", get_rating(new_soup))
            # print("Number of Product Reviews =", get_review_count(new_soup))
            # print("Availability =", get_availability(new_soup))
            # print()
            # print()

            if get_title(new_soup) != "":
                dispatcher.utter_message(text=text)

        return []


class ActionShowSanitizers(Action):

    def name(self) -> Text:
        return "action_show_sanitizers"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        def get_title(soup):
            try:
                title = soup.find("span", attrs={"id": 'productTitle'})
                title_value = title.string
                title_string = title_value.strip()

            except AttributeError:
                title_string = ""

            return title_string

        def get_price(soup):
            try:
                price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip()

            except AttributeError:
                try:
                    price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip()

                except:
                    price = ""

            return price

        def get_rating(soup):
            try:
                rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()

            except AttributeError:
                try:
                    rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
                except:
                    rating = ""

            return rating

        def get_review_count(soup):
            try:
                review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()

            except AttributeError:
                review_count = ""

            return review_count

        def get_availability(soup):
            try:
                available = soup.find("div", attrs={'id': 'availability'})
                available = available.find("span").string.strip()

            except AttributeError:
                available = "Not Available"

            return available

        HEADERS = ({'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                    'Accept-Language': 'en-US'})

        URL = "https://www.amazon.com/s?k=hand+sanitizers&ref=nb_sb_noss_2"
        webpage = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "lxml")
        links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
        links_list = []

        for link in links:
            links_list.append(link.get('href'))

        for link in links_list:
            new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

            new_soup = BeautifulSoup(new_webpage.content, "lxml")

            text = "Product Title: {0}\nProduct Price: {1}\nProduct Rating: {2}\nNumber of Product Reviews: {3}".format(
                get_title(new_soup), get_price(new_soup), get_rating(new_soup), get_review_count(new_soup))

            # print("Product Title =", get_title(new_soup))
            # print("Product Price =", get_price(new_soup))
            # print("Product Rating =", get_rating(new_soup))
            # print("Number of Product Reviews =", get_review_count(new_soup))
            # print("Availability =", get_availability(new_soup))
            # print()
            # print()

            if get_title(new_soup) != "":
                dispatcher.utter_message(text=text)

        return []


class ActionCovidNews(Action):

    def name(self) -> Text:
        return "action_covid_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cnn_paper = newspaper.build('http://cnn.com')

        # dispatcher.utter_message(text="Hello World!")

        return []

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import AllSlotsReset

from details import get_ticket_status, get_customer_details, get_order_details
from soup import search_weather_details, search_word_meaning, translate_word, search_restaurants


class GetCustomerDetails(Action):
    def name(self):
        return 'action_customer_details'

    def run(self, dispatcher, tracker, domain):
        customer_id = str(tracker.get_slot('iD'))
        id_type = str(tracker.get_slot('idType'))
        if id_type != "None" and customer_id != "None":
            message = get_customer_details(customer_id)
            if message == "None":
                dispatcher.utter_message("Customer not found")
            else:
                dispatcher.utter_message(message)
            return [AllSlotsReset()]
        elif id_type == "None":
            dispatcher.utter_template("utter_ask_IdType", tracker)
        elif customer_id == "None":
            dispatcher.utter_template("utter_ask_Id", tracker)


class GetOrderDetails(Action):
    def name(self):
        return 'action_order_details'

    def run(self, dispatcher, tracker, domain):
        order_id = str(tracker.get_slot('iD'))
        id_type = str(tracker.get_slot('idType'))
        if id_type != "None" and order_id != "None":
            message = get_order_details(order_id)
            if message == "None":
                dispatcher.utter_message("Order ID does not exist")
            else:
                dispatcher.utter_message(message)
            return [AllSlotsReset()]
        elif id_type == "None":
            dispatcher.utter_template("utter_ask_IdType", tracker)
        elif order_id == "None":
            dispatcher.utter_template("utter_ask_Id", tracker)


class GetTicketDetails(Action):
    def name(self):
        return 'action_ticket_details'

    def run(self, dispatcher, tracker, domain):
        ticket_id = str(tracker.get_slot('iD'))
        id_type = str(tracker.get_slot('idType'))
        if id_type != "None" and ticket_id != "None":
            message = get_ticket_status(ticket_id)
            if message == "None":
                dispatcher.utter_message("No ticket exists with that ID")
            else:
                dispatcher.utter_message(message)
            return [AllSlotsReset()]
        elif id_type == "None":
            dispatcher.utter_template("utter_ask_IdType", tracker)
        elif ticket_id == "None":
            dispatcher.utter_template("utter_ask_Id", tracker)


class GetTranslation(Action):
    def name(self):
        return 'action_translate_data'

    def run(self, dispatcher, tracker, domain):
        word = str(tracker.get_slot('searchWord'))
        language = str(tracker.get_slot('language'))
        search_type = str(tracker.get_slot('searchType'))
        if search_type != "None" and word != "None" and language != "None":
            message = translate_word(word, language)
            dispatcher.utter_message(message)
            return [AllSlotsReset()]
        elif search_type == "None":
            dispatcher.utter_template("utter_specific", tracker)
        elif word == "None":
            dispatcher.utter_template("utter_ask_word", tracker)
        elif language == "None":
            dispatcher.utter_template("utter_ask_language", tracker)


class GetWeatherDetails(Action):
    def name(self):
        return 'action_weather_details'

    def run(self, dispatcher, tracker, domain):
        search_type = str(tracker.get_slot('searchType'))
        location = str(tracker.get_slot('GPE'))
        if search_type != "None" and location != "None":
            message = search_weather_details(location)
            dispatcher.utter_message(message)
            return [AllSlotsReset()]
        elif search_type == "None":
            dispatcher.utter_template("utter_specific", tracker)
        elif location == "None":
            dispatcher.utter_template("utter_ask_location", tracker)


class GetWordMeaning(Action):
    def name(self):
        return 'action_word_meaning'

    def run(self, dispatcher, tracker, domain):
        search_type = str(tracker.get_slot('searchType'))
        word = str(tracker.get_slot('searchWord'))
        if search_type != "None" and word != "None":
            message = search_word_meaning(word)
            dispatcher.utter_message(message)
            return [AllSlotsReset()]
        elif search_type == "None":
            dispatcher.utter_template("utter_specific", tracker)
        elif word == "None":
            dispatcher.utter_template("utter_ask_word", tracker)


class GetRestaurant(Action):
    def name(self):
        return 'action_restaurant_details'

    def run(self, dispatcher, tracker, domain):
        area = str(tracker.get_slot('area'))
        cuisine = str(tracker.get_slot('cuisine'))
        response = search_restaurants(area, cuisine)
        dispatcher.utter_message(response)
        return [AllSlotsReset()]

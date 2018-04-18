from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import AllSlotsReset

from soup import search_weather_details, search_word_meaning, translate_word, search_restaurants
from details import get_ticket_status, get_customer_details, get_order_details


class GetCustomerDetails(Action):
    def name(self):
        return 'utter_customer_details'

    def run(self, dispatcher, tracker, domain):
        customer_id = str(tracker.get_slot('iD'))
        message = get_customer_details(customer_id)
        if message == "None":
            dispatcher.utter_message("Customer not found")
        else:
            dispatcher.utter_message(message)
        return [AllSlotsReset()]


class GetOrderDetails(Action):
    def name(self):
        return 'utter_order_details'

    def run(self, dispatcher, tracker, domain):
        order_id = str(tracker.get_slot('iD'))
        message = get_order_details(order_id)
        if message == "None":
            dispatcher.utter_message("Order ID does not exist")
        else:
            dispatcher.utter_message(message)
        return [AllSlotsReset()]


class GetTranslation(Action):
    def name(self):
        return 'utter_translate_data'

    def run(self, dispatcher, tracker, domain):
        word = str(tracker.get_slot('searchWord'))
        language = str(tracker.get_slot('language'))
        message = translate_word(word, language)
        dispatcher.utter_message(message)
        return [AllSlotsReset()]


class GetTicketDetails(Action):
    def name(self):
        return 'utter_ticket_details'

    def run(self, dispatcher, tracker, domain):
        ticket_id = str(tracker.get_slot('iD'))
        message = get_ticket_status(ticket_id)
        if message == "None":
            dispatcher.utter_message("No ticket exists with that ID")
        else:
            dispatcher.utter_message(message)
        return [AllSlotsReset()]


class GetWeatherDetails(Action):
    def name(self):
        return 'utter_weather_details'

    def run(self, dispatcher, tracker, domain):
        location = str(tracker.get_slot('GPE'))
        message = search_weather_details(location)
        dispatcher.utter_message(message)
        return [AllSlotsReset()]


class GetWordMeaning(Action):
    def name(self):
        return 'utter_word_meaning'

    def run(self, dispatcher, tracker, domain):
        word = str(tracker.get_slot('searchWord'))
        message = search_word_meaning(word)
        dispatcher.utter_message(message)
        return [AllSlotsReset()]


class ActionFallback(Action):
    def name(self):
        return "fallback"

    def run(self, dispatcher, tracker, domain):
        from rasa_core.events import UserUtteranceReverted

        dispatcher.utter_message("Sorry, didn't get that. Try again.")
        return [UserUtteranceReverted()]


class GetRestaurant(Action):
    def name(self):
        return 'utter_restaurant_details'

    def run(self, dispatcher, tracker, domain):
        area = str(tracker.get_slot('area'))
        cuisine = str(tracker.get_slot('cuisine'))
        response = search_restaurants(area, cuisine)
        dispatcher.utter_message(response)
        return [AllSlotsReset()]
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import AllSlotsReset

from soup import searchWeatherDetails, searchWordMeaning, translateGoogle
from details import getTicketStatus, getCustomerDetails, getOrderDetails


class GetCustomerDetails(Action):
    def name(self):
        return 'utter_customer_details'

    def run(self, dispatcher, tracker, domain):
        customerId = str(tracker.get_slot('iD'))
        message = getCustomerDetails(customerId)
        if message == "None":
            dispatcher.utter_message("Customer not found")
        else:
            dispatcher.utter_message(message)
        return [AllSlotsReset()]


class GetTicketDetails(Action):
    def name(self):
        return 'utter_ticket_details'

    def run(self, dispatcher, tracker, domain):
        ticketId = str(tracker.get_slot('iD'))
        message = getTicketStatus(ticketId)
        if message == "None":
            dispatcher.utter_message("No ticket exists with that id")
        else:
            dispatcher.utter_message(message)
        return [AllSlotsReset()]


class GetOrderDetails(Action):
    def name(self):
        return 'utter_order_details'

    def run(self, dispatcher, tracker, domain):
        orderId = str(tracker.get_slot('iD'))
        message = getOrderDetails(orderId)
        if message == "None":
            dispatcher.utter_message("Order id does not exist")
        else:
            dispatcher.utter_message(message)
        return [AllSlotsReset()]


class GetWeatherDetails(Action):
    def name(self):
        return 'utter_weather_details'

    def run(self, dispatcher, tracker, domain):
        location = str(tracker.get_slot('GPE'))
        message = searchWeatherDetails(location)
        dispatcher.utter_message(message)
        return [AllSlotsReset()]


class GetWordMeaning(Action):
    def name(self):
        return 'utter_word_meaning'

    def run(self, dispatcher, tracker, domain):
        word = str(tracker.get_slot('searchWord'))
        message = searchWordMeaning(word)
        dispatcher.utter_message(message)
        return [AllSlotsReset()]


class GetTranslation(Action):
    def name(self):
        return 'utter_translate_data'

    def run(self, dispatcher, tracker, domain):
        word = str(tracker.get_slot('searchWord'))
        language = str(tracker.get_slot('language'))
        message = translateGoogle(word, language)
        dispatcher.utter_message(message)
        return [AllSlotsReset()]


class ActionFallback(Action):
    def name(self):
        return "fallback"

    def run(self, dispatcher, tracker, domain):
        from rasa_core.events import UserUtteranceReverted

        dispatcher.utter_message("Sorry, didn't get that. Try again.")
        return [UserUtteranceReverted()]

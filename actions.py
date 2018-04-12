from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from rasa_core.events import AllSlotsReset

from soup import searchWeatherDetails, searchWordMeaning, translateGoogle
from details import getTicketStatus, getCustomerDetails, getOrderDetails
# import time
#
# st = 0
#
#
# class startTime(Action):
#     def name(self):
#         return 'start_time'
#
#     def run(self, dispatcher, tracker, domain):
#         global st
#         st = int(time.time())


class checkTime(Action):
    def name(self):
        return 'check_time'

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]


class GetCustomerDetails(Action):
    def name(self):
        return 'utter_customer_details'

    def run(self, dispatcher, tracker, domain):
        tracker.latest_message()
        customerId = str(tracker.get_slot('iD'))
        message = getCustomerDetails(customerId)
        if message == "None":
            dispatcher.utter_message("Customer not found")
        else:
            dispatcher.utter_message(message)
        return [SlotSet('iD', None), SlotSet('idType', None)]


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
        return [SlotSet('iD', None), SlotSet('idType', None)]


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
        return [SlotSet('iD', None), SlotSet('idType', None)]


class GetWeatherDetails(Action):
    def name(self):
        return 'utter_weather_details'

    def run(self, dispatcher, tracker, domain):
        location = str(tracker.get_slot('GPE'))
        message = searchWeatherDetails(location)
        dispatcher.utter_message(message)
        return [SlotSet('GPE', None), SlotSet('searchType', None)]


class GetWordMeaning(Action):
    def name(self):
        return 'utter_word_meaning'

    def run(self, dispatcher, tracker, domain):
        word = str(tracker.get_slot('searchWord'))
        message = searchWordMeaning(word)
        dispatcher.utter_message(message)
        return [SlotSet('searchWord', None), SlotSet('searchType', None)]


class GetTranslation(Action):
    def name(self):
        return 'utter_translate_data'

    def run(self, dispatcher, tracker, domain):
        word = str(tracker.get_slot('searchWord'))
        language = str(tracker.get_slot('language'))
        message = translateGoogle(word, language)
        dispatcher.utter_message(message)
        return [SlotSet('searchWord', None), SlotSet('searchType', None)]


class ActionFallback(Action):
    def name(self):
        return "fallback"

    def run(self, dispatcher, tracker, domain):
        from rasa_core.events import UserUtteranceReverted

        dispatcher.utter_message("Sorry, didn't get that. Try again.")
        return [UserUtteranceReverted()]


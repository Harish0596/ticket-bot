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
        id_type = str(tracker.get_slot('idType'))
        if id_type != "None" and customer_id != "None":
            message = get_customer_details(customer_id)
            if message == "None":
                dispatcher.utter_message("Customer not found")
            else:
                dispatcher.utter_message(message)
                return [AllSlotsReset()]
        elif id_type == "None":
            tracker.trigger_follow_up_action(domain.action_for_name("utter_ask_IdType"))
        elif customer_id == "None":
            tracker.trigger_follow_up_action(domain.action_for_name("utter_ask_Id"))


class GetOrderDetails(Action):
    def name(self):
        return 'utter_order_details'

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
            tracker.trigger_follow_up_action(domain.action_for_name("utter_ask_IdType"))
        elif order_id == "None":
            tracker.trigger_follow_up_action(domain.action_for_name("utter_ask_Id"))


class GetTicketDetails(Action):
    def name(self):
        return 'utter_ticket_details'

    def run(self, dispatcher, tracker, domain):
        ticket_id = str(tracker.get_slot('iD'))
        id_type = str(tracker.get_slot('idType'))
        if id_type != "None" and ticket_id != "None":
            message = get_ticket_status(ticket_id)
            if message == "None":
                dispatcher.utter_message("No ticket exists with that ID")
                return [AllSlotsReset()]
            else:
                dispatcher.utter_message(message)
                return [AllSlotsReset()]
        elif id_type == "None":
            tracker.trigger_follow_up_action(domain.action_for_name("utter_ask_IdType"))
        elif ticket_id == "None":
            tracker.trigger_follow_up_action(domain.action_for_name("utter_ask_Id"))


class GetTranslation(Action):
    def name(self):
        return 'utter_translate_data'

    def run(self, dispatcher, tracker, domain):
        word = str(tracker.get_slot('searchWord'))
        language = str(tracker.get_slot('language'))
        search_type = str(tracker.get_slot('searchType'))
        if search_type != "None" and word != "None" and language != "None":
            message = translate_word(word, language)
            dispatcher.utter_message(message)
            return [AllSlotsReset()]
        elif search_type == "None":
            tracker.trigger_follow_up_action(domain.action_for_name("utter_specific"))
        elif word == "None":
            tracker.trigger_follow_up_action(domain.action_for_name("utter_ask_word"))
        elif language == "None":
            tracker.trigger_follow_up_action(domain.action_for_name("utter_ask_language"))


class GetWeatherDetails(Action):
    def name(self):
        return 'utter_weather_details'

    def run(self, dispatcher, tracker, domain):
        search_type = str(tracker.get_slot('searchType'))
        location = str(tracker.get_slot('GPE'))
        if search_type != "None" and location != "None":
            message = search_weather_details(location)
            dispatcher.utter_message(message)
            return [AllSlotsReset()]
        elif search_type == "None":
            tracker.trigger_follow_up_action(domain.action_for_name("utter_specific"))
        elif location == "None":
            tracker.trigger_follow_up_action(domain.action_for_name("utter_ask_location"))


class GetWordMeaning(Action):
    def name(self):
        return 'utter_word_meaning'

    def run(self, dispatcher, tracker, domain):
        search_type = str(tracker.get_slot('searchType'))
        word = str(tracker.get_slot('searchWord'))
        if search_type != "None" and word != "None":
            message = search_word_meaning(word)
            dispatcher.utter_message(message)
            return [AllSlotsReset()]
        elif search_type == "None":
            tracker.trigger_follow_up_action(domain.action_for_name("utter_specific"))
        elif word == "None":
            tracker.trigger_follow_up_action(domain.action_for_name("utter_ask_word"))


# class ActionFallbackNLU(Action):
#     def name(self):
#         return "action_fallback_nlu"
#
#     def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_message("Sorry, nlu didn't get that. Try again.")
#         tracker.trigger_follow_up_action(domain.action_for_name("action_listen"))
#
#
# class ActionFallbackCORE(Action):
#     def name(self):
#         return "action_fallback_core"
#
#     def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_message("Sorry, core didn't get that. Try again.")
#         tracker.trigger_follow_up_action(domain.action_for_name("action_listen"))


class GetRestaurant(Action):
    def name(self):
        return 'utter_restaurant_details'

    def run(self, dispatcher, tracker, domain):
        area = str(tracker.get_slot('area'))
        cuisine = str(tracker.get_slot('cuisine'))
        response = search_restaurants(area, cuisine)
        dispatcher.utter_message(response)
        return [AllSlotsReset()]
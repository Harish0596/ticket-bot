import logging

from rasa_core.agent import Agent
from rasa_core.channels.direct import CollectingOutputChannel

logger = logging.getLogger(__name__)


class TrainingData:
    def __init__(self, training_data_dir):
        self.training_data_dir = training_data_dir

    # noinspection PyMethodMayBeStatic
    def format_data(self, nlu_dir, value):
        """Appends the user message to the corresponding nlu training data"""
        text = value.get('text')
        entities = value.get('entities')
        text_split = text.split()
        for entity in entities:
            text_split = [txt.replace(entity.get('entity_value'),
                                      "[{}]({})".format(entity.get('entity_value'), entity.get('entity'))) for txt in
                          text_split]
        value = " ".join(text_split)
        with open(nlu_dir, "a+") as data:
            if data.write("\n- {}".format(value)):
                print("Successfully added {} into {}".format(value, data.name))
            else:
                print("Failed to add {} into {}".format(value, data.name))

    def add_data(self, intent, message):
        """Function which pushes the user message to nlu training data"""
        path = self.training_data_dir+"/"
        self.format_data((path + intent + ".md"), message)


class ConfusedUsers:
    """Creates a list of users who have entered filter_user_message method"""

    def __init__(self):
        self.users = []

    def add_user(self, sender_id, status):
        self.users.append(dict({"sender_id": sender_id, "status": status}))

    def get_user(self, sender_id):
        return [user for user in self.users if user['sender_id'] == sender_id][0]

    def remove_user(self, sender_id):
        self.users = [user for user in self.users if user['sender_id'] != sender_id]

    def update_status(self, sender_id, status, intent_name, data):
        for user in self.users:
            if user.get('sender_id') == sender_id:
                user.update(dict({'sender_id': sender_id, 'status': status, 'intent': intent_name, 'message': data}))

    def get_all_users(self):
        return self.users


class Controller:
    """Controller class which can perform certain custom actions before routing to Rasa Core"""

    def __init__(self, model_directory, interpreter, nlu_training_data_directory):
        self.model_directory = model_directory
        self.interpreter = interpreter
        self.agent = self._create_agent(model_directory, interpreter)
        self.users = ConfusedUsers()
        self.training = TrainingData(nlu_training_data_directory)

    @staticmethod
    def _create_agent(model_directory, interpreter):
        """Creates a Rasa Agent which runs when the server is started"""
        try:
            return Agent.load(model_directory, interpreter)
        except Exception as e:
            logger.warn("Failed to load any agent model. Running "
                        "Rasa Core server with out loaded model now. {}"
                        "".format(e))
            return None

    def user_message_controller(self, message, sender_id):

        """Sends the user message and sender_id to Rasa Core and collects the parsed response and agent response"""

        parse_data = self.agent.start_message_handling(message, sender_id)
        out = CollectingOutputChannel()
        response_data = self.agent.handle_message(message, output_channel=out, sender_id=sender_id)
        return [parse_data, response_data]

    def get_agent_response(self, message, sender_id):

        """Sends the user message and sender_id to Rasa Core and collects the agent response"""

        out = CollectingOutputChannel()
        response = self.agent.handle_message(message, output_channel=out, sender_id=sender_id)
        return response

    def get_agent_parsed_response(self, message, sender_id):

        """Sends the user message and sender_id to Rasa Core and collects the parsed response"""

        response = self.agent.start_message_handling(message, sender_id)
        return response

    def filter_agent_response(self, query, sender_id, parsed_data, respond_data):

        """Filters the response sent by the agent with custom queries and also can add data for nlu training"""

        global intent_to_add, data_to_add
        intent_name = parsed_data.get('tracker').get('latest_message').get('intent').get('name')
        confidence = parsed_data.get('tracker').get('latest_message').get('intent').get('confidence') * 100
        entities = parsed_data.get('tracker').get('latest_message').get('entities')
        try:
            status = self.users.get_user(sender_id).get('status')
        except IndexError:
            self.users.add_user(sender_id, 0)
            status = 0
        if confidence < 20 or (intent_name == "confirmation.yes" and status == 1) or (
                intent_name == "confirmation.no" and status == 1):

            if intent_name == "confirmation.yes" and status == 1:
                self.training.add_data(self.users.get_user(sender_id).get('intent'),
                                       self.users.get_user(sender_id).get('message'))
                logging.info(
                    'Reinforced user responses YES-LOG: User added Intent - "{}" : User added Message "{}" '.format(
                        self.users.get_user(sender_id).get('intent'),
                        self.users.get_user(sender_id).get('message').get('text')))
                self.users.remove_user(sender_id)
                return ["I will keep that in mind. Thank you for your response"]
            elif intent_name == "confirmation.no" and status == 1:
                logging.info(
                    'Reinforced user responses NO-LOG: Bot suggested Intent - "{}" : For User Message "{}" '.format(
                        self.users.get_user(sender_id).get('intent'),
                        self.users.get_user(sender_id).get('message').get('text')))
                self.users.remove_user(sender_id)
                return ["I will let my developers know about it, thank you for your response"]
            else:
                if not respond_data:
                    respond_data.append("Sorry, I couldn't understand you, can you ask me in another way?")
                else:
                    entity_list = []
                    if entities:
                        for entity in entities:
                            entity_list.append({"entity": entity.get("entity"), "entity_value": entity.get("value")})
                    intent_to_add = intent_name
                    data_to_add = {"text": query, "entities": entity_list}
                    respond_data.append("Did i give you the right response?")
                self.users.update_status(sender_id, 1, intent_to_add, data_to_add)
                return respond_data
        else:
            if status == 1:
                self.users.remove_user(sender_id)
            if not respond_data:
                respond_data.append("Sorry, I couldn't understand you, can you ask me in another way?")
            return respond_data

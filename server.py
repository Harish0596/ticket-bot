import logging

from rasa_core.interpreter import RasaNLUInterpreter
import yaml
from flask import json
from klein import Klein

from server_controller import Controller

logger = logging.getLogger(__name__)

checkFirstRequest = 0
logging.basicConfig(filename='klein_server_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def read_yaml():
    global templates
    with open("domain.yml", 'r') as stream:
        try:
            data = yaml.load(stream)
            templates = data.get('templates')
        except yaml.YAMLError as exc:
            print(exc)
    return templates


def request_parameters(request):
    if request.method.decode('utf-8', 'strict') == 'GET':
        return {
            key.decode('utf-8', 'strict'): value[0].decode('utf-8',
                                                           'strict')
            for key, value in request.args.items()}
    else:
        content = request.content.read()
        try:
            return json.loads(content.decode('utf-8', 'strict'))
        except ValueError as e:
            logger.error("Failed to decode json during respond request. "
                         "Error: {}. Request content: "
                         "'{}'".format(e, content))
            raise


class Server(Controller):
    app = Klein()

    def __init__(self, model_directory, interpreter, nlu_training_data_directory):
        super().__init__(model_directory, interpreter, nlu_training_data_directory)

    @app.route("/api/v1/status", methods=['GET'])
    def status(self, request):
        """Check if the server is running and responds with the status."""
        request.setHeader('Access-Control-Allow-Origin', '*')
        return json.dumps({'status': 'OK'})

    @app.route('/api/v1/<sender_id>/parse', methods=['GET', 'POST'])
    def parse(self, request, sender_id):
        request.setHeader('Content-Type', 'application/json')
        request_params = request_parameters(request)

        if 'query' in request_params:
            message = request_params.pop('query')
        elif 'q' in request_params:
            message = request_params.pop('q')
        else:
            request.setResponseCode(400)
            return json.dumps({"error": "Invalid parse parameter specified"})
        try:
            response = self.agent.start_message_handling(message, sender_id)
            request.setResponseCode(200)
            return json.dumps(response)
        except Exception as e:
            request.setResponseCode(500)
            logger.error("Caught an exception during "
                         "parse: {}".format(e), exc_info=1)
            return json.dumps({"error": "{}".format(e)})

    @app.route('/api/v1/<sender_id>/respond', methods=['GET', 'POST'])
    def respond(self, request, sender_id):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')
        request_params = request_parameters(request)
        if 'query' in request_params:
            message = request_params.pop('query')
        elif 'q' in request_params:
            message = request_params.pop('q')
        else:
            request.setResponseCode(400)
            return json.dumps({"error": "Invalid parse parameter specified"})
        try:
            parse_data = self.get_agent_parsed_response(message, sender_id)
            response_data = self.get_agent_response(message, sender_id)
            response = self.filter_agent_response(message, sender_id, parse_data, [response_data[0].get('text')])
            request.setResponseCode(200)
            return json.dumps(response)
        except Exception as e:
            request.setResponseCode(500)
            logger.error("Caught an exception during "
                         "parse: {}".format(e), exc_info=1)
            return json.dumps({"error": "{}".format(e)})


if __name__ == "__main__":
    read_yaml()
    server = Server("models/dialogue/default/dialogue_model", RasaNLUInterpreter("models/nlu/default"
                                                                                 "/nlu_model"), "data/nlu")
    server.app.run("0.0.0.0", 8081)

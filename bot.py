from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.run import serve_application
from rasa_core.utils import AvailableEndpoints

logger = logging.getLogger(__name__)


def run(model_path, interpreter, endpoints):
    agent = Agent.load(model_path, interpreter, action_endpoint=endpoints.action)
    serve_application(agent)


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    nlu_interpreter = RasaNLUInterpreter('models/nlu/default/nlu_model')
    _endpoints = AvailableEndpoints.read_endpoints("./endpoints.yml")
    run(model_path='models/dialogue/dialogue_model', interpreter=nlu_interpreter, endpoints=_endpoints)
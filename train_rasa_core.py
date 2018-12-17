from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.training import interactive

logger = logging.getLogger(__name__)


def train_interactive(stories_file, model_path, interpreter):
    agent = Agent.load(model_path, interpreter)
    interactive.run_interactive_learning(agent, stories_file)


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/nlu_model')
    train_interactive('./data/dialogue/', './models/dialogue/dialogue_model', nlu_interpreter)

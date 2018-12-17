from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core import config
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter

logger = logging.getLogger(__name__)


def train_dialogue_model(domain_file, stories_file, output_path, interpreter, policy_config):
    policies = config.load(policy_config)
    agent = Agent(domain_file, policies=policies, interpreter=interpreter)
    training_data = agent.load_data(stories_file)
    agent.train(training_data)
    agent.persist(output_path)
    return agent


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/nlu_model')
    train_dialogue_model('domain.yml', './data/dialogue/', './models/dialogue/dialogue_model', nlu_interpreter,
                         policy_config='policy_config.yml')

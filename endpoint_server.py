from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from gevent.pywsgi import WSGIServer
from rasa_core_sdk.endpoint import endpoint_app

logger = logging.getLogger(__name__)


def endpoint_server_start(custom_actions):
    logger.info("Starting action endpoint server...")
    edp_app = endpoint_app(action_package_name=custom_actions)

    http_server = WSGIServer(('0.0.0.0', 2655), edp_app)

    http_server.start()
    logger.info("Action endpoint is up and running. on {}"
                "".format(http_server.address))

    http_server.serve_forever()


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    endpoint_server_start("actions")
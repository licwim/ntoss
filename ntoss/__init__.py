# !/usr/bin/env python
# ================================================= #
#                                                   #
#    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    #
#    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    #
#    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    #
#    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    #
#                                                   #
#   __init__.py                                     #
#       By: licwim                                  #
#                                                   #
#   Created: 03-04-2021 21:49:35 by licwim          #
#   Updated: 03-04-2021 21:52:24 by licwim          #
#                                                   #
# ================================================= #

import json
import logging
from ntoss.config import Config

CONFIG_FILE = 'config/devel.json'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

with open(CONFIG_FILE, 'r') as fp:
    config = json.load(fp)
Config.TOKEN = config.get('bot').get('token')
Config.BOT_NAME = config.get('bot').get('name')
Config.BOT_USERNAME = config.get('bot').get('username')
Config.MY_USERNAME = config.get('bot').get('my_username')
Config.MY_USER_ID = config.get('bot').get('my_user_id')
Config.SERVER_HOST = config.get('server').get('host')
Config.HTTP_PORT = config.get('server').get('http_port')
Config.SSH_PORT = config.get('server').get('ssh_port')

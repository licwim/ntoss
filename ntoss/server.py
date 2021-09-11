# ================================================= #
#                                                   #
#    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    #
#    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    #
#    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    #
#    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    #
#                                                   #
#   server.py                                       #
#       By: licwim                                  #
#                                                   #
#   Created: 28-03-2021 03:10:18 by licwim          #
#   Updated: 28-03-2021 03:10:31 by licwim          #
#                                                   #
# ================================================= #

import json
from typing import Any
from pyngrok import ngrok
from http import HTTPStatus
from http.server import (
    ThreadingHTTPServer,
    BaseHTTPRequestHandler,
)
from ntoss.utils.inputlistener import InputListener
from ntoss.bot.telegrambot import TelegramBot
from ntoss.config import Config as c


class RequestHandler(BaseHTTPRequestHandler):

    def _send_response(self, data: Any, code: int = HTTPStatus.OK):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        prepare_data = {}
        if code >= HTTPStatus.BAD_REQUEST:
            prepare_data['error'] = data
        else:
            prepare_data['response'] = data
        prepare_data['code'] = code

        prepare_data = json.dumps(prepare_data).encode('utf8')
        self.wfile.write(prepare_data)

    def do_GET(self):
        try:
            action = self.path.strip('/')

            if not action:
                message = "No action"
                code = HTTPStatus.BAD_REQUEST
            elif action in self.server.action_list:
                print(f"Action: {action}")
                message = self.server.action_list[action]()
                code = HTTPStatus.OK
            else:
                message = "Action not found"
                code = HTTPStatus.NOT_FOUND

            self._send_response(message, code)

        except BaseException as ex:
            self._send_response(ex.args, HTTPStatus.INTERNAL_SERVER_ERROR)

        self._send_response("Post")


class Server(ThreadingHTTPServer):

    SERVER_ADDRESS = (c.SERVER_HOST, c.HTTP_PORT)

    def __init__(self) -> None:
        super().__init__(self.SERVER_ADDRESS, RequestHandler)
        self.params = {}
        self.params['server'] = self
        self.bot = TelegramBot(self.params)
        self.input_listener = InputListener()

        self.action_list = {
            'connect': self.connectTunnel,
            'disconnect': self.disconnectTunnel,
            'ping': self.pong,
        }

    def run(self):
        self.input_listener.add_event('exit', self.stop)
        self.bot.run()
        self.serve_forever()

    def connectTunnel(self):
        ssh_tunnel = ngrok.connect(c.SSH_PORT, "tcp")
        self.params['ssh_tunnel'] = ssh_tunnel
        http_tunnel = ngrok.connect(c.HTTP_PORT, "http")
        self.params['http_tunnel'] = http_tunnel
        self.ssh_tunnel = ssh_tunnel
        self.http_tunnel = http_tunnel

    def disconnectTunnel(self):
        if self.ssh_tunnel:
            ngrok.disconnect(self.ssh_tunnel.public_url)
            self.params.pop('ssh_tunnel')
        if self.http_tunnel:
            ngrok.disconnect(self.http_tunnel.public_url)
            self.params.pop('http_tunnel')

    def pong(self):
        return "pong"

    def handle(self, action: str):
        try:
            self.action_list[action]()
        except KeyError:
            return

    def stop(self):
        self.bot.stop()
        self.shutdown()

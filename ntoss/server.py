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

from pyngrok import ngrok
from http import HTTPStatus
from http.client import HTTPConnection
from http.server import (
    ThreadingHTTPServer,
    BaseHTTPRequestHandler,
)
from ntoss.utils.inputlistener import InputListener
from ntoss.bot.telegrambot import TelegramBot
from ntoss.config import Config as c


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            action = self.headers.get('action')
            self.server.action_list[action](self.server)
        except KeyError:
            pass
        self.send_response(HTTPStatus.ACCEPTED)


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

    def handle(self, action: str):
        try:
            self.action_list[action]()
        except KeyError:
            return

    def stop(self):
        self.bot.stop()
        self.shutdown()

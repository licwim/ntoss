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

from ntoss.utils.inputlistener import InputListener
from ntoss.config import Config as c
import socket
from requests import Response, Request
from ntoss.bot.telegrambot import TelegramBot
from pyngrok import ngrok
from http.server import (
	ThreadingHTTPServer,
	HTTPServer,
	BaseHTTPRequestHandler,
	SimpleHTTPRequestHandler,
)


class Server(ThreadingHTTPServer):

	SERVER_ADDRESS = (c.SERVER_HOST, int(c.HTTP_PORT))

	def __init__(self) -> None:
		super().__init__(self.SERVER_ADDRESS, SimpleHTTPRequestHandler)
		self.params = {}
		self._bot = TelegramBot(self.params)
		self._input_listener = InputListener()

	def run(self):
		self._input_listener.add_event('exit', self.stop)
		self.connectTunnel()
		self._bot.run()
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
		if self.http_tunnel:
			ngrok.disconnect(self.http_tunnel.public_url)

	def stop(self):
		self._bot.stop()
		self.shutdown()

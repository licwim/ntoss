# !/usr/bin/env python

from ntoss.utils.inputlistener import InputListener
from ntoss.config import Config as c
from telegram.ext import Updater
from ntoss.commands.simplecommands import (
	StartCommand,
	GetUrlsCommand,
	ConnectTunnelCommand,
	DisconnectTunnelCommand,
)

class TelegramBot:

	commands_list = {
		'start': StartCommand,
		'geturls': GetUrlsCommand,
		# 'connect': ConnectTunnelCommand,
		# 'disconnect': DisconnectTunnelCommand,
	}

	def __init__(self, params) -> None:
		self.updater = Updater(token=c.TOKEN)
		self.params = params

	def commands_init(self):
		for _name, _class in self.commands_list.items():
			command = _class(self.params)
			self.commands_list[_name] = command
			self.updater.dispatcher.add_handler(command.handler)

	def run(self):
		self.commands_init()
		self.updater.start_polling()

	def stop(self):
		self.updater.stop()

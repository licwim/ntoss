# !/usr/bin/env python

from pyngrok import ngrok
import requests
from telegram.ext import CommandHandler


class BaseCommand:

    def __init__(self, name: str, command: callable, params: dict):
        self.name = name
        self.command = command
        self.params = params
        self.handler = CommandHandler(name, command)

    def execute(self, update, context):
        self.update = update
        self.context = context


class StartCommand(BaseCommand):

    def __init__(self, params: dict):
        super().__init__('start', self.execute, params)

    def execute(self, update, context):
        super().execute(update, context)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Ну дарова!")


class GetUrlsCommand(BaseCommand):

    def __init__(self, params: dict):
        super().__init__('geturls', self.execute, params)

    def execute(self, update, context):
        super().execute(update, context)

        text = 'Public Urls:\n'
        if 'ssh_tunnel' in self.params and self.params['ssh_tunnel']:
            text += f"    SSH      {self.params['ssh_tunnel'].public_url}\n"
        if 'http_tunnel' in self.params and self.params['http_tunnel']:
            text += f"    HTTP    {self.params['http_tunnel'].public_url}\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)


class DisconnectTunnelCommand(BaseCommand):

    def __init__(self, params: dict):
        super().__init__('disconnect', self.execute, params)

    def execute(self, update, context):
        super().execute(update, context)

        self.params['server'].handle('disconnect')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='DISCONNECT OK')


class ConnectTunnelCommand(BaseCommand):

    def __init__(self, params: dict):
        super().__init__('connect', self.execute, params)

    def execute(self, update, context):
        super().execute(update, context)

        self.params['server'].handle('connect')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='CONNECT OK')

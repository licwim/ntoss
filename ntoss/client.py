# ================================================= #
#                                                   #
#    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    #
#    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    #
#    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    #
#    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    #
#                                                   #
#   client_test.py                                  #
#       By: licwim                                  #
#                                                   #
#   Created: 28-03-2021 12:43:11 by licwim          #
#   Updated: 28-03-2021 13:19:39 by licwim          #
#                                                   #
# ================================================= #

import socket

class BaseClient:

	def __init__(self) -> None:
		self.address_to_server = ('localhost', 8686)
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
	def connect(self):
		client = self.client
		client.connect(self.address_to_server)

		client.send(bytes("hello from client number ", encoding='UTF-8'))

		data = client.recv(1024)
		print(str(data))

client = BaseClient()
client.connect()

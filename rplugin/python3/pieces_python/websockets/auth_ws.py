from .base_websocket import BaseWebsocket
from ..settings import Settings
from .._pieces_lib.pieces_os_client import UserProfile,UserApi
import json


class AuthWS(BaseWebsocket):
	def __init__(self,on_message, on_open_callbacks=...):
		self.on_message_callback = on_message
		super().__init__(on_open_callbacks)

	@property
	def url(self):
		return Settings.AUTH_WS_URL

	def on_message(self,ws, message):
		try:
			self.on_message_callback(UserProfile.from_json(message))
		except json.decoder.JSONDecodeError:
			self.on_message_callback(None) # User logged out!

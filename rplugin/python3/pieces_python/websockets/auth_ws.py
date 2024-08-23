from .base_websocket import BaseWebsocket
from ..settings import Settings
from .._pieces_lib.pieces_os_client import UserProfile
from ..auth import Auth
import json


class AuthWS(BaseWebsocket):
	@property
	def url(self):
		return Settings.AUTH_WS_URL

	def on_message(self,ws, message):
		try:
			Auth.on_user_callback(UserProfile.from_json(message))
		except json.decoder.JSONDecodeError:
			Auth.on_user_callback(None) # User logged out!

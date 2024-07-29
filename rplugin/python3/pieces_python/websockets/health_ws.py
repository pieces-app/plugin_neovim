from ..settings import Settings
from .base_websocket import BaseWebsocket

class HealthWS(BaseWebsocket):
	def __init__(self, on_startup,on_open_callbacks=[]):
		self.on_startup = on_startup
		super().__init__(on_open_callbacks)

	@property
	def url(self):
		return Settings.HEALTH_WS_URL

	def on_message(self,ws, message):
		if message == "OK":
			if hasattr(self,"on_startup"):
				self.on_startup()
				delattr(self,"on_startup") # we don't need to run everytime to run the startup every messaage
			Settings.is_loaded = True
		else:
			Settings.is_loaded = False
			Settings.nvim.async_call(Settings.nvim.err_write,"Please make sure Pieces OS is running\n")

	def on_close(self, ws, close_status_code, close_msg):
		Settings.is_loaded = False # the websocket is closed
		Settings.nvim.async_call(Settings.nvim.err_write,"Please make sure Pieces OS is running\n")


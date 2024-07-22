import pynvim
from .settings import Settings
from .api import get_version

@pynvim.plugin
class Pieces:
	api_client = None
	def __init__(self,nvim) -> None:
		self.nvim = nvim
		Settings.nvim = nvim
		Settings.get_application() # Connect to the connector API

	@pynvim.command('PiecesHealth')
	def get_health(self):
		health = "ok" if Settings.get_health() else "failed"
		self.nvim.command(f"echom '{health}'")

	@pynvim.command('PiecesOSVersion')
	def get_version(self):
		self.nvim.command(f"echom '{get_version()}'")
	
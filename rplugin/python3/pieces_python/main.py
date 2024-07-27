import pynvim
from .settings import Settings
from .api import get_version
from .websockets import ask_stream_ws,base_websocket,assets_ws
from ._pieces_lib.pieces_os_client import QGPTStreamInput,QGPTQuestionInput,RelevantQGPTSeeds

from .assets_snapshot import AssetSnapshot


@pynvim.plugin
class Pieces:
	api_client = None
	def __init__(self,nvim) -> None:
		self.nvim = nvim
		Settings.nvim = nvim
		Settings.get_application() # Connect to the connector API

	@pynvim.function("PiecesStartup")
	def startup(self,args):
		""" START THE WEBSOCKETS!"""
		# self.nvim.command(f"echom 'started websockets'")
		base_websocket.BaseWebsocket.start_all()

	@pynvim.command('PiecesHealth')
	def get_health(self):
		health = "ok" if Settings.get_health() else "failed"
		self.nvim.command(f"echom '{health}'")


	@pynvim.command('PiecesOSVersion')
	def get_version(self):
		self.nvim.command(f"echom '{get_version()}'")

	@pynvim.function('PiecesCopilotSendQuestion',sync=True)
	def send_question(self,args):
		query = args[0]
		self.nvim.command(f"echom '{query}'")
		ask_stream_ws.send_message(QGPTStreamInput(
			question=QGPTQuestionInput(
				relevant=RelevantQGPTSeeds(iterable=[]),
				query=query,
				application=Settings.get_application().id,
				model = Settings.model_id
			),
			conversation = ask_stream_ws.conversation_id,
		))
	@pynvim.function('PiecesEditAsset')
	def edit_asset(self,args):
		asset_id,data = args
		AssetSnapshot(asset_id).edit_asset_original_format(data)

	@pynvim.function('PiecesDeleteAsset')
	def delete_asset(self,args):
		asset_id = args[0]
		AssetSnapshot(asset_id).delete()

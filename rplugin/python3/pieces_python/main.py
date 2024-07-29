import pynvim
from .settings import Settings
from .api import get_version,version_check,is_pieces_opened
from .websockets import ask_stream_ws,base_websocket
from ._pieces_lib.pieces_os_client import QGPTStreamInput,QGPTQuestionInput,RelevantQGPTSeeds


@pynvim.plugin
class Pieces:
	api_client = None
	def __init__(self,nvim:pynvim.Nvim) -> None:
		self.nvim = nvim
		Settings.nvim = nvim
		Settings.load_config()

	@pynvim.function("PiecesStartup")
	def startup(self,args):
		"""START THE WEBSOCKETS!"""
		if not Settings.get_health():
			self.nvim.err_write("Please make sure Pieces OS is running\n")
			return
		""" START THE WEBSOCKETS!"""
		# self.nvim.command(f"echom 'started websockets'")
		base_websocket.BaseWebsocket.start_all()

	
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


	@pynvim.function("PiecesVersionCheck", sync=True)
	def version_check(self,args):
		return version_check()[0]

	## PYTHON COMMANDS
	@pynvim.command('PiecesHealth')
	@is_pieces_opened
	def get_health(self):
		health = "ok" if Settings.get_health() else "failed"
		self.nvim.out_write(f"{health}\n")

	@pynvim.command('PiecesOSVersion')
	@is_pieces_opened
	def get_version(self):
		self.nvim.out_write(f"{get_version()}\n")

	## LUA COMMANDS
	@pynvim.command("PiecesSnippets")
	@is_pieces_opened
	def open_snippets(self):
		self.nvim.exec_lua("require('pieces_assets').setup()")


	@pynvim.command("PiecesCopilot")
	@is_pieces_opened
	def open_copilot(self):
		self.nvim.exec_lua("require('pieces_copilot').setup()")




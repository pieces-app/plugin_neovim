import pynvim
from .settings import Settings
from .api import get_version,version_check,is_pieces_opened
from .websockets import ask_stream_ws,base_websocket
from ._pieces_lib.pieces_os_client import (QGPTStreamInput,
											QGPTQuestionInput,
											RelevantQGPTSeeds,
											ConversationMessageApi,
											ConversationsApi)
from .streamed_identifiers.assets_snapshot import AssetSnapshot
from .websockets.health_ws import HealthWS

@pynvim.plugin
class Pieces:
	api_client = None
	def __init__(self,nvim:pynvim.Nvim) -> None:
		self.nvim = nvim
		Settings.nvim = nvim
		Settings.load_config()
		self.api_client = Settings.api_client # Load any host stuff 

	@pynvim.function("PiecesStartup")
	def startup(self,args):
		"""START THE WEBSOCKETS!"""
		self.health_ws = HealthWS(self._startup)
		self.health_ws.start()

	def _startup(self):
		check,plugin = version_check()
		if check:
			Settings.get_application() # Connect to the connector API
			base_websocket.BaseWebsocket.start_all()
		else:
			Settings.is_loaded = False
			self.health_ws.close()
			self.nvim.async_call(self.nvim.err_write,f"Please update {plugin}\n")

	
	@pynvim.function('PiecesCopilotSendQuestion',sync=True)
	def send_question(self,args):
		query = args[0]
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

	@pynvim.function('PiecesGetMessage',sync=True)
	def get_message(self,args):
		message_id = args[0]
		message = ConversationMessageApi(Settings.api_client).message_specific_message_snapshot(message=message_id,transferables=True)
		return f"{{role = '{message.role.value}', raw = [=[{message.fragment.string.raw}]=]}}"

	@pynvim.function("PiecesSetConversation")
	def set_conversation(self,args):
		ask_stream_ws.conversation_id = args[0]

	@pynvim.function("PiecesDeleteConversation")
	def delete_conversation(self,args):
		ConversationsApi(self.api_client).conversations_delete_specific_conversation(args[0])

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

	@pynvim.command("PiecesConversations")
	@is_pieces_opened
	def open_conversations(self):
		self.nvim.exec_lua("require('pieces_copilot.conversations_ui').setup()")




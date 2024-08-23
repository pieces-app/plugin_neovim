import pynvim
from .settings import Settings
from .api import get_version,version_check,is_pieces_opened
from .websockets import ask_stream_ws,base_websocket
from ._pieces_lib.pieces_os_client import (QGPTStreamInput,
											QGPTQuestionInput,
											RelevantQGPTSeeds,
											ConversationMessageApi,
											ConversationsApi,
											FragmentMetadata)
from .streamed_identifiers.assets_snapshot import AssetSnapshot
from .websockets.health_ws import HealthWS
from ._version import __version__
from .auth import Auth
from .file_map import file_map
import semver
file_map_reverse = {v:k for k,v in file_map.items()}


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
		statup()
	
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

	@pynvim.function("PiecesGetModel",sync=True)
	def get_model(self,args):
		return Settings.model_name


	@pynvim.function("PiecesCreateSnippet",sync=False)
	def create_asset(self,args): 
		try: metadata = FragmentMetadata(ext=file_map_reverse.get(self.nvim.api.buf_get_option(0, 'filetype')))
		except: metadata = None
		AssetSnapshot.create(args[0], metadata)
		self.nvim.out_write("Snippet created successfully\n")

	@pynvim.function("PiecesGetModels",sync=True)
	def get_models(self,args):
		return"{" + ", ".join(f'"{value}"' for value in Settings.get_models_ids().keys()) + "}"

	@pynvim.function("PiecesChangeModel",sync=True)
	def change_model(self,args):
		model_name = args[0]
		if model_name in Settings.get_models_ids().keys():
			Settings.model_name = model_name
			return f"Set the current LLM model to {model_name} successfully"
		return "Invalid Model name"

	@pynvim.function("PiecesSetConversation")
	def set_conversation(self,args):
		ask_stream_ws.conversation_id = args[0]

	@pynvim.function("PiecesDeleteConversation")
	def delete_conversation(self,args):
		ConversationsApi(self.api_client).conversations_delete_specific_conversation(args[0])

	@pynvim.function("PiecesVersionCheck", sync=True)
	def version_check(self,args):
		return version_check()[0]
	@pynvim.function("PiecesLogin", sync=True)
	def login_function(self,args):
		"""
			first args if true it will show the ui
		"""
		if args:
			self.auth.login(args[0])

	## PYTHON COMMANDS
	@pynvim.command('PiecesHealth')
	@is_pieces_opened
	def get_health(self):
		health = "OK" if Settings.get_health() else "Failed"
		self.nvim.out_write(f"{health}\n")

	@pynvim.command('PiecesOSVersion')
	@is_pieces_opened
	def get_version(self):
		self.nvim.out_write(f"{get_version()}\n")

	@pynvim.command('PiecesPluginVersion')
	@is_pieces_opened
	def get_plugin_version(self):
		self.nvim.out_write(f"{__version__}\n")

	@pynvim.command('PiecesLogin')
	@is_pieces_opened
	def login(self):
		self.auth.login()

	@pynvim.command('PiecesLogout')
	@is_pieces_opened
	def logout(self):
		self.auth.logout()

	@pynvim.command('PiecesConnectCloud')
	@is_pieces_opened
	def connect(self):
		self.auth.connect()

	@pynvim.command('PiecesDisconnectCloud')
	@is_pieces_opened
	def disconnect(self):
		self.auth.disconnect()

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


	@pynvim.command("PiecesAccount")
	@is_pieces_opened
	def auth_command(self):
		self.nvim.exec_lua("require('pieces_auth').setup()")

	@pynvim.command('PiecesCreateSnippet', range='', nargs='*')
	@is_pieces_opened
	def pieces_create_snippet(self, args, range):
		line1 = range[0]
		line2 = range[1]
		self.nvim.command(f'call luaeval("require(\'pieces_assets.create\').setup({line1}, {line2})")')


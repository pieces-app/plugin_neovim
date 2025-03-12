import webbrowser
import pynvim

from .settings import Settings
from pieces_os_client.wrapper.basic_identifier import BasicAsset,BasicChat,BasicMessage
from pieces_os_client.wrapper.client import PiecesClient
from pieces_os_client.wrapper.websockets import BaseWebsocket
from pieces_os_client.models.fragment_metadata import FragmentMetadata
from pieces_os_client.models.inactive_os_server_applet import InactiveOSServerApplet, OSAppletEnum
from .startup import Startup
from .utils import is_pieces_opened, install_pieces_os
from .auth import Auth

from ._version import __version__
from .file_map import file_map
import os

file_map_reverse = {v:k for k,v in file_map.items()}


@pynvim.plugin
class Pieces:
	api_client:PiecesClient
	def __init__(self,nvim:pynvim.Nvim) -> None:
		self.nvim = nvim
		Settings.nvim = nvim
		Settings.load_config()
		self.api_client = Settings.api_client
		self.auth = Auth()

	@pynvim.function("PiecesStartup")
	def startup(self,args):
		Startup.startup()
	
	@pynvim.function('PiecesCopilotSendQuestion')
	def send_question(self,args):
		if args[0].strip():
			Settings.api_client.copilot.stream_question(args[0])

	@pynvim.function('PiecesEditAsset')
	def edit_asset(self,args):
		asset_id,data = args
		BasicAsset(asset_id).raw_content = data
		Settings.nvim.out_write("You snippet is saved successfully\n")

	@pynvim.function('PiecesDeleteAsset')
	def delete_asset(self,args):
		asset_id = args[0]
		BasicAsset(asset_id).delete()

	@pynvim.function('PiecesGetMessage',sync=True)
	def get_message(self,args):
		message_id = args[0]
		try:
			message = BasicMessage(Settings.api_client,id=message_id)
			return f"{{role = '{message.role}', raw = [=[{message.raw_content}]=]}}"
		except: pass

	@pynvim.function("PiecesGetModel",sync=True)
	def get_model(self,args):
		return Settings.api_client.model_name


	@pynvim.function("PiecesCreateSnippet",sync=False)
	def create_asset(self,args):
		try: metadata = FragmentMetadata(ext=file_map_reverse.get(self.nvim.api.buf_get_option(0, 'filetype')))
		except: metadata = None
		BasicAsset.create(args[0], metadata)
		self.nvim.out_write("Snippet created successfully\n")

	@pynvim.function("PiecesGetModels",sync=True)
	def get_models(self,args):
		return"{" + ", ".join(f'"{value}"' for value in Settings.api_client.models.keys()) + "}"

	@pynvim.function("PiecesChangeModel",sync=True)
	def change_model(self,args):
		model_name = args[0]
		if model_name in self.api_client.available_models_names:
			Settings.set_model_name(model_name)
			return f"Set the current LLM model to {model_name} successfully"
		return "Invalid Model name"

	@pynvim.function("PiecesSetConversation")
	def set_conversation(self,args):
		if args:
			try: conversation = BasicChat(args[0])
			except: conversation = None
		else:
			conversation = None
		Settings.api_client.copilot.chat = conversation

	@pynvim.function("PiecesDeleteConversation")
	def delete_conversation(self,args):
		try:
			BasicChat(args[0]).delete()
		except:
			pass

	@pynvim.function("PiecesLogin", sync=True)
	def login_function(self,args):
		"""first args if true it will show the ui"""
		if args:
			return self.auth.login(args[0])
		self.auth.login()

	@pynvim.function("PiecesAddContext",sync=True)
	def add_context(self,args):
		path,snippet = args
		if path:
			if os.path.exists(path):
				Settings.api_client.copilot.context.paths.append(path) 
				type = "folders" if os.path.isdir(path) else "files"
				Settings.nvim.exec_lua(
				    f"table.insert(require('pieces.copilot.context').context['{type}'], '{path}')"
				)
			else:
				Settings.nvim.err_write("Invalid paths\n")
		if snippet:
			Settings.api_client.copilot.context.assets.append(BasicAsset(snippet))
			Settings.nvim.exec_lua(
				    f"table.insert(require('pieces.copilot.context').context['snippets'], '{snippet}')"
				)
	@pynvim.function("PiecesOpenPiecesOS", sync=True)
	def open_pieces_function(self, args = None):
		if Settings.api_client.is_pos_stream_running: return True
		started = self.api_client.open_pieces_os()
		if started:
			BaseWebsocket.start_all()
		return started

	@pynvim.function('PiecesOpenLink',sync=True)
	def open_link(self,args):
		webbrowser.open(args[0])

	## PYTHON COMMANDS
	@pynvim.command('PiecesHealth')
	def get_health(self):
		health = "OK" if Settings.api_client.is_pieces_running() else "Failed"
		self.nvim.out_write(f"{health}\n")

	@pynvim.command("PiecesOpenPiecesOS")
	def open_pieces(self):
		if self.open_pieces_function():
			return self.nvim.async_call(self.nvim.out_write,"Pieces OS started successfully\n")
		return self.nvim.async_call(self.nvim.err_write,"Could not start Pieces OS\n")

	@pynvim.command("PiecesClosePiecesOS")
	@is_pieces_opened
	def close_pieces_os(self):
		Settings.api_client.os_api.os_terminate()
		return self.nvim.out_write("Closed PiecesOS\n")

	@pynvim.command('PiecesOSVersion')
	@is_pieces_opened
	def get_version(self):
		self.nvim.out_write(f"{Settings.api_client.version}\n")

	@pynvim.command('PiecesPluginVersion')
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

	@pynvim.command("PiecesInstall")
	def install(self):
		install_pieces_os()

	## LUA COMMANDS
	@pynvim.command("PiecesDrive")
	@is_pieces_opened
	def open_snippets(self):
		self.nvim.exec_lua("require('pieces.assets').setup()")


	@pynvim.command("PiecesCopilot")
	@is_pieces_opened
	def open_copilot(self):
		if Settings.get_copilot_mode() == "BROWSER":
			return webbrowser.open(
				"localhost:" + str(Settings.api_client.os_api.os_applet_launch(
					InactiveOSServerApplet(
						type=OSAppletEnum.COPILOT
					)
				).port)
			)
		else:
			self.nvim.exec_lua("require('pieces.copilot').setup()")

	@pynvim.command("PiecesChats")
	@is_pieces_opened
	def open_conversations(self):
		self.nvim.exec_lua("require('pieces.copilot.conversations_ui').setup()")


	@pynvim.command("PiecesAccount")
	@is_pieces_opened
	def auth_command(self):
		self.nvim.exec_lua("require('pieces.auth').setup()")

	@pynvim.command('PiecesCreateMaterial', range='', nargs='*')
	@is_pieces_opened
	def pieces_create_snippet(self, args, range):
		self.nvim.exec_lua(f"require('pieces.assets.create').setup()")


from .settings import Settings
from .auth import Auth
from ._version import __version__
from pieces_os_client.wrapper.websockets import (HealthWS,
	AuthWS,
	AssetsIdentifiersWS,
	ConversationWS,
	BaseWebsocket)
from pieces_os_client.wrapper.basic_identifier import BasicAsset
from pieces_os_client.wrapper.version_compatibility import UpdateEnum, VersionChecker
from pieces_os_client.wrapper.streamed_identifiers import (
	ConversationsSnapshot,
	AssetSnapshot)
from pieces_os_client.models.conversation import Conversation
from pieces_os_client.models.asset import Asset
from .file_map import file_map
from .utils import check_compatibility, on_copilot_message




class Startup:
	@classmethod
	def startup(cls):
		"""START THE WEBSOCKETS!"""
		try:
			latest_version = Settings.get_latest_tag()
			if VersionChecker.compare(latest_version,__version__) == 1:
				Settings.nvim.command('echohl WarningMsg')
				Settings.nvim.command(
					'echomsg "A new update for the Pieces Plugin is now available! Please update to the latest version to enjoy improved functionality and enhanced performance."'
				)
				Settings.nvim.command('echohl None')
		except:  # Internet issues or status code is not 200
			pass
		AuthWS(Settings.api_client, Auth.on_user_callback)
		AssetsIdentifiersWS(Settings.api_client,cls.update_lua_assets,cls.delete_lua_asset)
		ConversationWS(Settings.api_client,cls.update_lua_conversations,cls.delete_lua_conversation)
		health_ws = HealthWS(Settings.api_client, cls.on_message, cls.on_startup,on_close=lambda x,y,z: cls.on_close())
		if Settings.api_client.is_pieces_running():
			health_ws.start()

	@classmethod
	def on_message(cls, message):
		pass

	@staticmethod
	def on_close():
		Settings.api_client.is_pos_stream_running = False

	@classmethod
	def on_startup(cls, ws):
		compatiable = check_compatibility()
		if compatiable:
			if not Settings.load_settings().get("version"):
				Settings.update_settings(version=__version__)

			if Settings.load_settings().get("version") != __version__:
				Settings.nvim.async_call(Settings.nvim.command, 'call PiecesRunRemotePlugins()')
				Settings.update_settings(version = __version__)


			Settings.api_client.model_name = Settings.load_settings().get("model_name","GPT-4o Chat Model")
			BaseWebsocket.start_all()
			Settings.api_client.copilot.ask_stream_ws.on_message_callback = on_copilot_message
			Settings.api_client.copilot._return_on_message = lambda: None
		else:
			BaseWebsocket.close_all()
	

	@classmethod
	def update_lua_assets(cls,asset:Asset):
		asset_wrapper = BasicAsset(asset.id)

		lang = asset_wrapper.classification
		if lang: lang = lang.value
		description = asset_wrapper.description

		lua = f"""
		require("pieces.assets.assets").append_snippets({{
					name = [=[{asset_wrapper.name}]=],
					id = "{asset.id}",
					raw = [=[{asset_wrapper.raw_content}]=],
					language = "{lang}",
					filetype = "{file_map.get(lang,"txt")}",
					annotation = [=[{description}]=]
				}},{str(not AssetSnapshot.first_shot).lower()})
		"""
		Settings.nvim.async_call(Settings.nvim.exec_lua, lua)
		cls.update_list("pieces.assets.ui") # Update the list
	
	@classmethod
	def update_lua_conversations(cls,conversation:Conversation):
		m = "{" + ", ".join(f"['{k}']='{v}'" for k, v in conversation.messages.indices.items()) + "}"
		annotation = " "
		annotations = conversation.annotations
		if annotations and annotations.indices:
			annotation = Settings.api_client.annotation_api.annotation_specific_annotation_snapshot(list(annotations.indices.keys())[0]).text.replace("\n"," ")
		lua = f"""
		require("pieces.copilot.conversations").append_conversations({{
					name = [=[{conversation.name}]=],
					id = "{conversation.id}",
					messages = {m},
					annotation = [=[{annotation}]=],
					update={int(conversation.created.value.timestamp())},
				}},{str(ConversationsSnapshot.first_shot).lower()})
		"""

		Settings.nvim.async_call(Settings.nvim.exec_lua, lua)
		cls.update_list('pieces.copilot.conversations_ui')

	@classmethod
	def delete_lua_asset(cls,asset):
		lua = f"""require("pieces.assets.assets").remove_snippet('{asset.id}')"""
		Settings.nvim.async_call(Settings.nvim.exec_lua, lua)
		cls.update_list("pieces.assets.ui") # Update the list

	@classmethod
	def delete_lua_conversation(cls,conversation):
		lua = f"""require("pieces.copilot.conversations").remove_conversation('{conversation.id}')"""
		Settings.nvim.async_call(Settings.nvim.exec_lua, lua)
		cls.update_list('pieces.copilot.conversations_ui')

	@staticmethod
	def update_list(module):
		Settings.nvim.async_call(Settings.nvim.exec_lua,f"require('{module}').update()")


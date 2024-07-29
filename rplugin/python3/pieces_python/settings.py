from ._pieces_lib import pieces_os_client as pos_client
from typing import Dict
import pynvim
from ._version import __version__


class classproperty(property):
	def __get__(self, owner_self, owner_cls):
		return self.fget(owner_cls)

class Settings:
	# Initialize class variables
	nvim:pynvim.Nvim = None
	application = None
	models = None
	host = ""
	model_name = ""
	_api_client = None
	model_name = "GPT-4o Chat Model" # TODO: be changed later dependends on the user favorite
	is_loaded = False

	@classproperty
	def model_id(cls):
		return cls.get_models_ids()[cls.model_name]

	@classproperty
	def api_client(cls):
		if cls._api_client: return cls._api_client
		cls._api_client = cls._get_api_client()
		return cls._api_client
	
	@classmethod
	def get_health(cls):
		"""
		Retrieves the health status from the WellKnownApi and returns True if the health is 'ok', otherwise returns False.

		Returns:
		bool: True if the health status is 'ok', False otherwise.
		"""
		try:
			health = pos_client.WellKnownApi(cls.api_client).get_well_known_health()
			return health == "ok"
		except:
			return False

	@classmethod
	def get_application(cls)-> pos_client.Application:
		if cls.application:
			return cls.application

		# Decide if it's Windows, Mac, Linux or Web
		api_instance = pos_client.ConnectorApi(cls.api_client)
		seeded_connector_connection = pos_client.SeededConnectorConnection(
			application=pos_client.SeededTrackedApplication(
				name = "VIM",
				platform = cls.os,
				version = __version__))
		api_response = api_instance.connect(seeded_connector_connection=seeded_connector_connection)
		cls.application = api_response.application
		return cls.application

	@classmethod
	def get_models_ids(cls) -> Dict[str, str]:
		if cls.models:
			return cls.models

		api_instance = pos_client.ModelsApi(cls.api_client)

		api_response = api_instance.models_snapshot()
		cls.models = {model.name: model.id for model in api_response.iterable if model.cloud or model.downloaded} # getting the models that are available in the cloud or is downloaded

		return cls.models

	@classmethod
	def load_config(cls) -> None:
		"""
			Load the lua configrations
		"""
		for config in ["os",'host']:
			lua_code = f"""
			local config = require('pieces_config')
			return config.{config}
			"""
			out = cls.nvim.exec_lua(lua_code)

			setattr(cls,config,out)


	@classmethod
	def _get_api_client(cls):
		if not cls.host:
			if 'linux' == cls.os:
				cls.host = "http://127.0.0.1:5323"
			else:
				cls.host = "http://127.0.0.1:1000"

		# Websocket urls
		ws_base_url = cls.host.replace('http','ws')
		cls.ASSETS_IDENTIFIERS_WS_URL = ws_base_url + "/assets/stream/identifiers"
		cls.AUTH_WS_URL = ws_base_url + "/user/stream"
		cls.ASK_STREAM_WS_URL = ws_base_url + "/qgpt/stream"
		cls.CONVERSATION_WS_URL = ws_base_url + "/conversations/stream/identifiers"

		configuration = pos_client.Configuration(host=cls.host)

		cls.api_client = pos_client.ApiClient(configuration)
		return cls.api_client
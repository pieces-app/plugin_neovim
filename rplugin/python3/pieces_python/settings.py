from ._pieces_lib.platformdirs import user_data_dir
from ._pieces_lib.pieces_os_client.wrapper import PiecesClient
from ._pieces_lib.pieces_os_client import SeededConnectorConnection,SeededTrackedApplication
from ._version import __version__
import pynvim
from pathlib import Path
import json
import urllib.request


class classproperty(property):
	def __get__(self, owner_self, owner_cls):
		return self.fget(owner_cls)

class Settings:
	# Initialize class variables
	nvim:pynvim.Nvim = None
	application = None
	models = None
	host = ""
	_api_client = None
	is_loaded = False
	os:str
	pieces_data_dir = user_data_dir(appauthor="pieces", appname="neovim",ensure_exists=True)
	settings_file = Path(pieces_data_dir, "settings.json")

	@classproperty
	def model_name(cls):
		return cls.api_client.model_name

	@model_name.setter
	def model_name(cls,value):
		if value in cls.api_client.available_models_names:
			cls.api_client.model_name = value
			cls.update_settings(model_name=value)
	
	@classmethod
	def get_health(cls):
		"""
		Retrieves the health status from the WellKnownApi and returns True if the health is 'ok', otherwise returns False.

		Returns:
		bool: True if the health status is 'ok', False otherwise.
		"""
		try:
			health = cls.api_client.well_known_api.get_well_known_health()
			return health == "ok"
		except:
			return False


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

		if not cls.host:
			if 'linux' == cls.os:
				cls.host = "http://127.0.0.1:5323"
			else:
				cls.host = "http://127.0.0.1:1000"
		cls.api_client = PiecesClient(cls.host,
			seeded_connector=SeededConnectorConnection(
				application=SeededTrackedApplication(
					name = "VIM",
					platform = cls.os,
					version = __version__)))
		cls.models = cls.api_client.get_models()
		cls.copilot = cls.api_client.copilot
		cls.api_client.model_name = cls.load_settings().get("model_name","GPT-4o Chat Model")


	@classmethod
	def load_settings(cls):
		try:
			with open(cls.settings_file, 'r') as file:
				data = json.load(file)
				return data
		except (json.JSONDecodeError,FileNotFoundError):
			return {}

	@classmethod
	def update_settings(cls,**kwargs):
		data = cls.load_settings()
		data.update(kwargs)

		with open(cls.settings_file, "w") as f:
			json.dump(data, f)

	@staticmethod
	def get_latest_tag():
		with urllib.request.urlopen("https://api.github.com/repos/pieces-app/plugin_neo_vim/tags") as response:
			if response.status == 200:
				data = response.read()
				tags = json.loads(data)

				if tags:
					return tags[0]['name']


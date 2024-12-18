from typing import Optional
from pieces_os_client.wrapper import PiecesClient
from pieces_os_client.models.seeded_connector_connection import SeededConnectorConnection
from pieces_os_client.models.seeded_tracked_application import SeededTrackedApplication
from pieces_os_client.wrapper.version_compatibility import VersionCheckResult
from ._version import __version__
import pynvim
import json
import urllib.request
import os



class Settings:
	# Initialize class variables
	nvim:pynvim.Nvim
	host = ""
	os:str
	
	api_client:PiecesClient
	version_compatibility: Optional[VersionCheckResult] = None

	@classmethod
	def set_model_name(cls,value):
		if value in cls.api_client.available_models_names:
			cls.api_client.model_name = value
			cls.update_settings(model_name=value)


	@classmethod
	def load_config(cls) -> None:
		"""
			Load the lua configrations
		"""
		for config in ["os",'host']:
			lua_code = f"""
			local config = require('pieces.config')
			return config.{config}
			"""
			out = cls.nvim.exec_lua(lua_code)

			setattr(cls,config,out) # Setting up the host and the os

		cls.api_client = PiecesClient(
			seeded_connector=SeededConnectorConnection(
				application=SeededTrackedApplication(
					name = "VIM",
					platform = cls.os,
					version = __version__)),
			connect_websockets=False)

		cls.pieces_data_dir = cls.nvim.call('stdpath', 'data')
		cls.plugin_dir = os.path.join(cls.pieces_data_dir, 'Pieces')
		cls.settings_file = os.path.join(cls.plugin_dir, "settings.json")
		if not os.path.exists(cls.plugin_dir):
			os.makedirs(cls.plugin_dir)



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


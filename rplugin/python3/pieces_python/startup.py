from .settings import Settings
import semver
from .auth import Auth
from ._version import __version__
from ._pieces_lib.pieces_os_client.wrapper.websockets import *
from .api import version_check

def statup():
	"""START THE WEBSOCKETS!"""
	try:
		latest_version = semver.VersionInfo.parse(Settings.get_latest_tag())
		if latest_version > semver.VersionInfo.parse(__version__):
			Settings.nvim.command('echohl WarningMsg')
			Settings.nvim.command(f'echomsg "A new update for the Pieces Plugin is now available! Please update to the latest version to enjoy improved functionality and enhanced performance."')
			Settings.nvim.command('echohl None')
	except: # Internet issues or status code is not 200
		pass
	

	HealthWS(Settings.api_client,on_message,on_startup).start()
def on_message(message):
	if message == "OK":
		Settings.is_loaded = True
	else:
		Settings.is_loaded = False
		Settings.nvim.async_call(Settings.nvim.err_write,"Please make sure Pieces OS is running\n")

def on_startup():
	check,plugin = version_check()
	AuthWS(Settings.api_client,Auth.on_user_callback)
	if check:
		if Settings.load_settings().get("version",__version__) != __version__:
			Settings.update_settings(version=__version__)
			Settings.nvim.async_call(Settings.nvim.command,'call PiecesRunRemotePlugins()')
		BaseWebsocket.start_all()
	else:
		Settings.is_loaded = False
		BaseWebsocket.close_all()
		Settings.nvim.async_call(Settings.nvim.err_write,f"Please update {plugin}\n")

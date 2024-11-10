from ._version import __version__
import pynvim
import types
import sys
pip = f"{sys.executable} -m pip"

outdated_message = f"""Your 'pieces_os_client' package is out of date. 
This may cause issues with the Pieces for Neovim plugin’s functionality. 

To update it, please run the following command in your terminal:

`{pip} install pieces_os_client --upgrade`

Would you like to update it now?
"""

missing_sdks_message = f"""The 'pieces_os_client' package is missing, which is required for the Pieces for Neovim plugin to work. 

To install it, run the following command:

`{pip} install pieces_os_client`

Would you like to install it now?
"""


error_message = missing_sdks_message


try:
	from pieces_os_client import __version__ as pieces_os_client_version

	try: # If there is any issue in the version checker then it is outdated
		from pieces_os_client.wrapper.version_compatibility import VersionChecker
		VersionChecker.compare("1.0.0","1.0.0") # Check also that the compare is working too
	except (AttributeError, ModuleNotFoundError):
		error_message = outdated_message
		raise ModuleNotFoundError

	if VersionChecker.compare(pieces_os_client_version,"4.0.0") < 0: # We need to be above 4.0.0
		error_message = outdated_message
		raise ModuleNotFoundError

	from .main import Pieces
except ModuleNotFoundError: # Seems the sdks is not installed
	@pynvim.plugin
	class Pieces:
		def __init__(self,nvim:pynvim.Nvim) -> None:
			self.nvim = nvim
			commands = nvim.api.get_commands([])
			plugin_commands = [cmd for cmd in commands if cmd.startswith("Pieces")]
			if not plugin_commands: # If no command is registered let's register fake ones. 
				plugin_commands = ['PiecesAccount', 'PiecesConnectCloud',
					'PiecesConversations', 'PiecesCopilot','PiecesCreateSnippet',
					'PiecesDisconnectCloud', 'PiecesHealth', 'PiecesLogin',
					'PiecesLogout', 'PiecesOSVersion', 'PiecesOpenPiecesOS',
					'PiecesPluginVersion', 'PiecesSnippets'] 

			for command_name in plugin_commands:
				setattr(Pieces, command_name, self.create_dynamic_method(command_name))

		def create_dynamic_method(self,command_name):
			def method_body(self, *args, **kwargs):
				self.print_error_message()

			# Create a new function object
			dynamic_method = types.FunctionType(
				method_body.__code__,
				globals(),
				name=command_name
			)

			# Apply the pynvim.command decorator
			dynamic_method = pynvim.command(command_name)(dynamic_method)

			return dynamic_method


		@pynvim.function("PiecesStartup")
		def print_error_message(self,args=None):
			choice = self.nvim.funcs.confirm(error_message, '&Yes\n&No', 1)
			command = f"{pip} install pieces_os_client" if error_message == missing_sdks_message else f"{pip} install pieces_os_client --upgrade"  
			if choice == 1:
				self.nvim.command(f"!{command}")




from ._pieces_lib.pieces_os_client.wrapper.basic_identifier.chat import BasicChat
from ._pieces_lib.pieces_os_client.wrapper.websockets import BaseWebsocket
from .settings import Settings
import concurrent.futures

def convert_to_lua_table(python_dict):
	"""
	Convert a Python dictionary to a Lua table representation.
	Does not support objects and does not support lists except list of strings.
	"""
	def convert_value(value):
		if isinstance(value, dict):
			return convert_to_lua_table(value)
		elif isinstance(value, str):
			return f'[=[{value}]=]'
		elif isinstance(value, bool):
			return "true" if value else "false"
		elif isinstance(value, list):
			return "{" + ", ".join(f'"{val}"' for val in value) + "}"
		elif isinstance(value, (int, float)):
			return str(value)
		else:
			raise TypeError(f"Unsupported data type: {type(value)}")

	out = "{"
	for key, value in python_dict.items():
		lua_key = f'["{key}"]' if isinstance(key, str) else key
		lua_value = convert_value(value)
		out += f"{lua_key} = {lua_value}, "
	return out.rstrip(', ') + "}"


def on_copilot_message(message):
	if message.question:
		answers = message.question.answers.iterable

		for answer in answers:
			if not answer.text:
				continue
			text = answer.text
			if text == "\n":
				Settings.nvim.async_call(Settings.nvim.exec_lua,f"""
					require("pieces.copilot").add_line()""")
				continue
			Settings.nvim.async_call(Settings.nvim.exec_lua,f"""
				require("pieces.copilot").append_to_chat([=[{text}]=],"ASSISTANT")
			""")
	
	if message.status == "COMPLETED":
		Settings.nvim.async_call(Settings.nvim.exec_lua,f"""
			require("pieces.copilot").completed(true)
		""")
		Settings.api_client.copilot.chat = BasicChat(message.conversation)
	elif message.status == "FAILED":
		Settings.nvim.async_call(Settings.nvim.exec_lua,f"""
			require("pieces.copilot").completed(true)
		""")
		return # TODO: Add a better error message

def start_pieces_os(callback_sucess,callback_failed):
	with concurrent.futures.ThreadPoolExecutor() as executor:
		future = executor.submit(Settings.api_client.open_pieces_os)
		started = future.result()
		if started:
			callback_sucess()
		else:
			callback_failed()


def is_pieces_opened(func):
	def wrapper(*args, **kwargs):
		if Settings.is_loaded:
			return func(*args, **kwargs)
		else:
			# Run the health request to check if the server is running
			with concurrent.futures.ThreadPoolExecutor() as executor:
				future = executor.submit(Settings.api_client.is_pieces_running)
				health = future.result()
				if health:
					BaseWebsocket.start_all()
					return func(*args,**kwargs)
				else:
					return Settings.nvim.err_write("Please make sure Pieces OS is running and updated\n")
	return wrapper

from .._pieces_lib.pieces_os_client import QGPTStreamOutput,QGPTStreamInput
from .._pieces_lib.websocket import WebSocketConnectionClosedException

from ..settings import Settings
from .base_websocket import BaseWebsocket

class AskStreamWS(BaseWebsocket):
	def __init__(self) -> None:
		self.conversation_id = None
		super().__init__()

	@property
	def url(self):
		return Settings.ASK_STREAM_WS_URL

	def on_message(self,ws, message):
		message = QGPTStreamOutput.from_json(message)
		if message.question:
			answers = message.question.answers.iterable

			for answer in answers:
				Settings.nvim.async_call(Settings.nvim.exec_lua,f"""
					require("pieces_copilot").append_to_chat([=[{answer.text}]=],"Copilot")
				""")
		
		if message.status == "COMPLETED":
			self.conversation_id = message.conversation
			Settings.nvim.async_call(Settings.nvim.exec_lua,f"""
				require("pieces_copilot").completed(True)
			""")
		elif message.status == "FAILED":
			return # TODO display a failed message

	
	def send_message(self,message:QGPTStreamInput):
		try:
			if not self.ws:
				raise WebSocketConnectionClosedException()
			self.ws.send(message.to_json())
		except WebSocketConnectionClosedException:
			self.on_open = lambda ws:ws.send(message.to_json()) # Send the message on opening
			self.start() # Start a new websocket since we are not connected to any

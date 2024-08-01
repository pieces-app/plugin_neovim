from .._pieces_lib.pieces_os_client import StreamedIdentifiers
from ..settings import Settings
from ..streamed_identifiers.conversations_snapshot import ConversationsSnapshot

from .base_websocket import BaseWebsocket

class ConversationWS(BaseWebsocket):
	@property
	def url(self):
		return Settings.CONVERSATION_WS_URL

	def on_message(self,ws, message):
		ConversationsSnapshot.streamed_identifiers_callback(StreamedIdentifiers.from_json(message))

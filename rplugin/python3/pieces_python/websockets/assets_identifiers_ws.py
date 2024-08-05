from .._pieces_lib.pieces_os_client import StreamedIdentifiers

from ..streamed_identifiers.assets_snapshot import AssetSnapshot
from ..settings import Settings
from .base_websocket import BaseWebsocket

class AssetsIdentifiersWS(BaseWebsocket):
	@property
	def url(self):
		return Settings.ASSETS_IDENTIFIERS_WS_URL

	def on_message(self,ws, message):
		AssetSnapshot.streamed_identifiers_callback(StreamedIdentifiers.from_json(message))


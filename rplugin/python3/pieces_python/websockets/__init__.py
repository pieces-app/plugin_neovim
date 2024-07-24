# Create all webosckets
from .ask_websocket import AskStreamWS
from .assets_identifiers_ws import AssetsIdentifiersWS

ask_stream_ws = AskStreamWS()
assets_ws = AssetsIdentifiersWS()

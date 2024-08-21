# Create all webosckets
from .ask_websocket import AskStreamWS
from .assets_identifiers_ws import AssetsIdentifiersWS
from .health_ws import HealthWS
from .conversation_websocket import ConversationWS
from .auth_ws import AuthWS
from ..auth import Auth

auth_ws = AuthWS(Auth.on_user_callback)
ask_stream_ws = AskStreamWS()
assets_ws = AssetsIdentifiersWS()
conversation_ws = ConversationWS()

from .streamed_identifiers import StreamedIdentifiersCache
from ..settings import Settings
from .._pieces_lib.pieces_os_client import ConversationApi,Conversation

def api_call(id):
	conversation = ConversationApi(Settings.api_client).conversation_get_specific_conversation(id)
	push_to_lua(conversation)
	return conversation

class ConversationsSnapshot(StreamedIdentifiersCache,
	api_call=api_call):
	
	@classmethod
	def sort_first_shot(cls):
		# Sort the dictionary by the "updated" timestamp
		sorted_conversations = sorted(cls.identifiers_snapshot.values(), key=lambda x: x.updated.value, reverse=True)
		cls.identifiers_snapshot = {conversation.id:conversation for conversation in sorted_conversations}

def push_to_lua(conversation:Conversation):
	m = "{" + ", ".join(f"['{k}']='{v}'" for k, v in conversation.messages.indices.items()) + "}"
	# Settings.nvim.async_call(Settings.nvim.out_write,m+'\n')
	lua = f"""
	require("pieces_copilot.conversations").append_conversations({{
				name = [=[{conversation.name if conversation.name else "New Conversation"}]=],
				id = "{conversation.id}",
				messages = {m}
			}},{str(not ConversationsSnapshot.first_shot).lower()})
	"""
	Settings.nvim.async_call(Settings.nvim.exec_lua, lua)

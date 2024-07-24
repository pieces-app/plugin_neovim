from typing import Optional


from .websockets.streamed_identifiers import StreamedIdentifiersCache
from ._pieces_lib.pieces_os_client import (Asset, 
											AssetApi,
											ClassificationSpecificEnum,
											FormatApi,
											ClassificationGenericEnum,
											Annotation)
from .settings import Settings

from .file_map import file_map
def api_call(id):
	asset = AssetApi(Settings.api_client).asset_snapshot(asset = id)
	push_to_lua(asset)
	return asset

class AssetSnapshot(StreamedIdentifiersCache,
	api_call=api_call):
	def __init__(self,asset_id) -> None:
		self._asset_id = asset_id
		self.asset = self.get_asset(asset_id)
		super().__init__()
	
	@classmethod
	def get_asset(cls,asset_id) -> Optional[Asset]:
		return cls.identifiers_snapshot.get(asset_id)

	def original_classification_specific(self) -> Optional[ClassificationSpecificEnum]:
		if self.asset:
			return self.asset.original.reference.classification.specific

	def edit_asset_original_format(self,data) -> None:
		if not self.asset:
			raise AttributeError("Asset not found")
		format_api = FormatApi(Settings.api_client)
		original = format_api.format_snapshot(self.asset.original.id, transferable=True)
		if original.classification.generic == ClassificationGenericEnum.IMAGE:
			# TODO: Ability to edit images
			return

		if original.fragment.string.raw:
			original.fragment.string.raw = data
		elif original.file.string.raw:
			original.file.string.raw = data
		format_api.format_update_value(transferable=False, format=original)

	def get_asset_raw(self) -> Optional[str]:
		if not self.asset:
			return
		asset_reference = self.asset.original.reference
		if asset_reference.fragment:
			return asset_reference.fragment.string.raw
		elif asset_reference.file.string:
			return asset_reference.file.string.raw
	@property
	def name(self) -> Optional[str]:
		return self.asset.name if self.asset else None
	
	@staticmethod
	def sort_first_shot():
		pass

	def get_annotation(self) -> Optional[Annotation]:
		if not self.asset:
			return
		annotations = self.asset.annotations.iterable
		annotations = sorted(annotations, key=lambda x: x.updated.value, reverse=True)
		for annotation in annotations:
			if annotation.type == "DESCRIPTION":
				return annotation

def push_to_lua(asset):
	asset_wrapper = AssetSnapshot(asset.id)
	asset_wrapper.asset = asset # Sometimes it is takes some ms to be cached

	lang = asset_wrapper.original_classification_specific()
	if lang: lang = lang.value
	annotation = asset_wrapper.get_annotation()
	if annotation: annotation = annotation.text

	lua = f"""
	require("pieces_assets.assets").append_snippets({{
				name = [=[{asset_wrapper.name}]=],
				id = "{asset.id}",
				raw = [=[{asset_wrapper.get_asset_raw()}]=],
				language = "{lang}",
				filetype = "{file_map.get(lang,"txt")}",
				annotation = [=[{annotation}]=]
			}})
	"""
	Settings.nvim.async_call(Settings.nvim.exec_lua, lua)
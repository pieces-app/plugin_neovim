from typing import Optional


from .streamed_identifiers import StreamedIdentifiersCache
from .._pieces_lib.pieces_os_client import (Asset, 
											AssetsApi,
											AssetApi,
											ClassificationSpecificEnum,
											FormatApi,
											ClassificationGenericEnum,
											Annotation,
											Format,
											Classification)
from ..settings import Settings

from ..file_map import file_map

from typing import Optional, Union
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
			return Settings.nvim.async_call(Settings.nvim.err_write,"Can't edit an image formated asset")

		if original.fragment.string.raw:
			original.fragment.string.raw = data
		elif original.file.string.raw:
			original.file.string.raw = data
		format_api.format_update_value(transferable=False, format=original)

	def get_asset_raw(self) -> Optional[str]:
		if not self.asset:
			return
		if self.is_image():
			content = self.get_ocr_content()
			if content is None:
				raise Exception('Unable to get OCR content')
			return content
		else:
			return (
				self.asset.original.reference.fragment.string.raw or
				self.asset.preview.base.reference.fragment.string.raw or
				''
			)
	
	def is_image(self) -> bool:
		return (
			self.asset.original.reference.classification.generic ==
			ClassificationGenericEnum.IMAGE
		)

	def get_ocr_content(self) -> Optional[str]:
		if not self.asset:
			return
		format = self.get_ocr_format(self.asset)
		if format is None:
			return
		return self.ocr_from_format(format)
	
	@staticmethod
	def get_ocr_format(src: Asset) -> Optional[Format]:
		image_id = src.original.reference.analysis.image.ocr.raw.id if src.original and src.original.reference and src.original.reference.analysis and src.original.reference.analysis.image and src.original.reference.analysis.image.ocr and src.original.reference.analysis.image.ocr.raw and src.original.reference.analysis.image.ocr.raw.id else None
		if image_id is None:
			return None
		return next((element for element in src.formats.iterable if element.id == image_id), None)
	
	@staticmethod
	def ocr_from_format(src: Optional[Format]) -> Optional[str]:
		if src is None:
			return None
		try:
			return bytes(src.file.bytes.raw).decode('utf-8')
		except Exception as e:
			Settings.nvim.async_call(Settings.nvim.err_write,'Error in getting image code:', e)
			return None

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

	def delete(self):
		delete_instance = AssetsApi(Settings.api_client)
		delete_instance.assets_delete_asset(self._asset_id)

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
			}},{str(not AssetSnapshot.first_shot).lower()})
	"""
	Settings.nvim.async_call(Settings.nvim.exec_lua, lua)
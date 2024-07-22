# coding: utf-8

"""
    Pieces Isomorphic OpenAPI

    Endpoints for Assets, Formats, Users, Asset, Format, User.

    The version of the OpenAPI document: 1.0
    Contact: tsavo@pieces.app
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pieces_python._pieces_lib.pydantic import BaseModel, Field, StrictBool, StrictStr
from pieces_python._pieces_lib.pieces_os_client.models.application import Application
from pieces_python._pieces_lib.pieces_os_client.models.conversation_type_enum import ConversationTypeEnum
from pieces_python._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from pieces_python._pieces_lib.pieces_os_client.models.grouped_timestamp import GroupedTimestamp
from pieces_python._pieces_lib.pieces_os_client.models.qgpt_prompt_pipeline import QGPTPromptPipeline
from pieces_python._pieces_lib.pieces_os_client.models.referenced_model import ReferencedModel
from pieces_python._pieces_lib.pieces_os_client.models.score import Score

class FlattenedConversation(BaseModel):
    """
    This is a flattend version of the Convsersation for DAG-Safety.  This will hold together a conversation. Ie allthe message within a conversation.  All the additional properties on here used on here like(anchors/assets) are used for context that will seed the conversation.  model is a calculated property, and will be the model of the last message sent if applicable.  summaries: on the top level here will simply be used to associate a conversation and a summary(this is not used for grounding), grounding.summaries will be used for this.(TODO)  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    id: StrictStr = Field(...)
    name: Optional[StrictStr] = Field(default=None, description="This is a name that is customized.")
    created: GroupedTimestamp = Field(...)
    updated: GroupedTimestamp = Field(...)
    deleted: Optional[GroupedTimestamp] = None
    favorited: Optional[StrictBool] = None
    application: Optional[Application] = None
    annotations: Optional[FlattenedAnnotations] = None
    messages: FlattenedConversationMessages = Field(...)
    model: Optional[ReferencedModel] = None
    assets: Optional[FlattenedAssets] = None
    websites: Optional[FlattenedWebsites] = None
    anchors: Optional[FlattenedAnchors] = None
    type: ConversationTypeEnum = Field(...)
    grounding: Optional[ConversationGrounding] = None
    score: Optional[Score] = None
    pipeline: Optional[QGPTPromptPipeline] = None
    demo: Optional[StrictBool] = Field(default=None, description="This will let us know if this conversation was generated as a 'demo' conversation")
    summaries: Optional[FlattenedWorkstreamSummaries] = None
    __properties = ["schema", "id", "name", "created", "updated", "deleted", "favorited", "application", "annotations", "messages", "model", "assets", "websites", "anchors", "type", "grounding", "score", "pipeline", "demo", "summaries"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> FlattenedConversation:
        """Create an instance of FlattenedConversation from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of var_schema
        if self.var_schema:
            _dict['schema'] = self.var_schema.to_dict()
        # override the default output from pydantic by calling `to_dict()` of created
        if self.created:
            _dict['created'] = self.created.to_dict()
        # override the default output from pydantic by calling `to_dict()` of updated
        if self.updated:
            _dict['updated'] = self.updated.to_dict()
        # override the default output from pydantic by calling `to_dict()` of deleted
        if self.deleted:
            _dict['deleted'] = self.deleted.to_dict()
        # override the default output from pydantic by calling `to_dict()` of application
        if self.application:
            _dict['application'] = self.application.to_dict()
        # override the default output from pydantic by calling `to_dict()` of annotations
        if self.annotations:
            _dict['annotations'] = self.annotations.to_dict()
        # override the default output from pydantic by calling `to_dict()` of messages
        if self.messages:
            _dict['messages'] = self.messages.to_dict()
        # override the default output from pydantic by calling `to_dict()` of model
        if self.model:
            _dict['model'] = self.model.to_dict()
        # override the default output from pydantic by calling `to_dict()` of assets
        if self.assets:
            _dict['assets'] = self.assets.to_dict()
        # override the default output from pydantic by calling `to_dict()` of websites
        if self.websites:
            _dict['websites'] = self.websites.to_dict()
        # override the default output from pydantic by calling `to_dict()` of anchors
        if self.anchors:
            _dict['anchors'] = self.anchors.to_dict()
        # override the default output from pydantic by calling `to_dict()` of grounding
        if self.grounding:
            _dict['grounding'] = self.grounding.to_dict()
        # override the default output from pydantic by calling `to_dict()` of score
        if self.score:
            _dict['score'] = self.score.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pipeline
        if self.pipeline:
            _dict['pipeline'] = self.pipeline.to_dict()
        # override the default output from pydantic by calling `to_dict()` of summaries
        if self.summaries:
            _dict['summaries'] = self.summaries.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> FlattenedConversation:
        """Create an instance of FlattenedConversation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return FlattenedConversation.parse_obj(obj)

        _obj = FlattenedConversation.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "id": obj.get("id"),
            "name": obj.get("name"),
            "created": GroupedTimestamp.from_dict(obj.get("created")) if obj.get("created") is not None else None,
            "updated": GroupedTimestamp.from_dict(obj.get("updated")) if obj.get("updated") is not None else None,
            "deleted": GroupedTimestamp.from_dict(obj.get("deleted")) if obj.get("deleted") is not None else None,
            "favorited": obj.get("favorited"),
            "application": Application.from_dict(obj.get("application")) if obj.get("application") is not None else None,
            "annotations": FlattenedAnnotations.from_dict(obj.get("annotations")) if obj.get("annotations") is not None else None,
            "messages": FlattenedConversationMessages.from_dict(obj.get("messages")) if obj.get("messages") is not None else None,
            "model": ReferencedModel.from_dict(obj.get("model")) if obj.get("model") is not None else None,
            "assets": FlattenedAssets.from_dict(obj.get("assets")) if obj.get("assets") is not None else None,
            "websites": FlattenedWebsites.from_dict(obj.get("websites")) if obj.get("websites") is not None else None,
            "anchors": FlattenedAnchors.from_dict(obj.get("anchors")) if obj.get("anchors") is not None else None,
            "type": obj.get("type"),
            "grounding": ConversationGrounding.from_dict(obj.get("grounding")) if obj.get("grounding") is not None else None,
            "score": Score.from_dict(obj.get("score")) if obj.get("score") is not None else None,
            "pipeline": QGPTPromptPipeline.from_dict(obj.get("pipeline")) if obj.get("pipeline") is not None else None,
            "demo": obj.get("demo"),
            "summaries": FlattenedWorkstreamSummaries.from_dict(obj.get("summaries")) if obj.get("summaries") is not None else None
        })
        return _obj

from pieces_python._pieces_lib.pieces_os_client.models.conversation_grounding import ConversationGrounding
from pieces_python._pieces_lib.pieces_os_client.models.flattened_anchors import FlattenedAnchors
from pieces_python._pieces_lib.pieces_os_client.models.flattened_annotations import FlattenedAnnotations
from pieces_python._pieces_lib.pieces_os_client.models.flattened_assets import FlattenedAssets
from pieces_python._pieces_lib.pieces_os_client.models.flattened_conversation_messages import FlattenedConversationMessages
from pieces_python._pieces_lib.pieces_os_client.models.flattened_websites import FlattenedWebsites
from pieces_python._pieces_lib.pieces_os_client.models.flattened_workstream_summaries import FlattenedWorkstreamSummaries
FlattenedConversation.update_forward_refs()


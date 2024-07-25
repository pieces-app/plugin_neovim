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
from pieces_python._pieces_lib.pydantic import BaseModel, Field, StrictStr
from pieces_python._pieces_lib.pieces_os_client.models.application import Application
from pieces_python._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from pieces_python._pieces_lib.pieces_os_client.models.referenced_workstream_summary import ReferencedWorkstreamSummary
from pieces_python._pieces_lib.pieces_os_client.models.score import Score
from pieces_python._pieces_lib.pieces_os_client.models.workstream_event_context import WorkstreamEventContext
from pieces_python._pieces_lib.pieces_os_client.models.workstream_event_trigger import WorkstreamEventTrigger

class SeededWorkstreamEvent(BaseModel):
    """
    This is a precreated version of a WorkstreamEvent event, this will be used ingested into PiecesOS and PiecesOS will do all the magic to transform this into relevant data show in the workstream feed.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    score: Optional[Score] = None
    application: Application = Field(...)
    trigger: WorkstreamEventTrigger = Field(...)
    context: Optional[WorkstreamEventContext] = None
    summary: Optional[ReferencedWorkstreamSummary] = None
    internal_identifier: Optional[StrictStr] = Field(default=None, description="This is used to override the event identifier, if this was an event that was originally in the internal events collection.")
    __properties = ["schema", "score", "application", "trigger", "context", "summary", "internal_identifier"]

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
    def from_json(cls, json_str: str) -> SeededWorkstreamEvent:
        """Create an instance of SeededWorkstreamEvent from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of score
        if self.score:
            _dict['score'] = self.score.to_dict()
        # override the default output from pydantic by calling `to_dict()` of application
        if self.application:
            _dict['application'] = self.application.to_dict()
        # override the default output from pydantic by calling `to_dict()` of trigger
        if self.trigger:
            _dict['trigger'] = self.trigger.to_dict()
        # override the default output from pydantic by calling `to_dict()` of context
        if self.context:
            _dict['context'] = self.context.to_dict()
        # override the default output from pydantic by calling `to_dict()` of summary
        if self.summary:
            _dict['summary'] = self.summary.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SeededWorkstreamEvent:
        """Create an instance of SeededWorkstreamEvent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SeededWorkstreamEvent.parse_obj(obj)

        _obj = SeededWorkstreamEvent.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "score": Score.from_dict(obj.get("score")) if obj.get("score") is not None else None,
            "application": Application.from_dict(obj.get("application")) if obj.get("application") is not None else None,
            "trigger": WorkstreamEventTrigger.from_dict(obj.get("trigger")) if obj.get("trigger") is not None else None,
            "context": WorkstreamEventContext.from_dict(obj.get("context")) if obj.get("context") is not None else None,
            "summary": ReferencedWorkstreamSummary.from_dict(obj.get("summary")) if obj.get("summary") is not None else None,
            "internal_identifier": obj.get("internal_identifier")
        })
        return _obj


